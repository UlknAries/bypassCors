import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from urllib.parse import urlparse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HOP_BY_HOP_HEADERS = {
    "connection","keep-alive","proxy-authenticate","proxy-authorization",
    "te","trailers","transfer-encoding","upgrade","content-length",
}
SAFE_REQ_HEADERS = {
    "accept","accept-language","content-type","range",
    "if-none-match","if-modified-since","cache-control",
    "authorization","user-agent",
}








def _validate_url(u: str):
    p = urlparse(u)
    if p.scheme not in ("http","https") or not p.netloc:
        raise HTTPException(status_code=400, detail="Invalid or unsupported URL scheme")

def _filter_req(h: dict) -> dict:
    out = {}
    for k, v in h.items():
        lk = k.lower()
        if lk in HOP_BY_HOP_HEADERS: continue
        if lk in ("origin","referer"): continue
        if lk in SAFE_REQ_HEADERS or lk.startswith("x-"):
            out[k] = v
    return out

def _filter_resp(h: dict) -> dict:
    out = {}
    for k, v in h.items():
        if k.lower() in HOP_BY_HOP_HEADERS or k.lower() == "set-cookie":
            continue
        out[k] = v
    out.pop("Content-Length", None)
    return out

@app.api_route("/bypass_cors", methods=["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS"])
async def bypass_cors_query(request: Request):
    target = request.query_params.get("url")
    if not target:
        raise HTTPException(status_code=400, detail="Missing 'url' query parameter")
    _validate_url(target)

    if request.method == "OPTIONS":
        return Response(status_code=204)

    body = await request.body()
    headers = _filter_req(dict(request.headers))

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target,
                headers=headers,
                content=body if body else None,
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Upstream request error: {e}")

    media_type = upstream.headers.get("content-type", "application/octet-stream")
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=media_type,
        headers=_filter_resp(dict(upstream.headers)),
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)