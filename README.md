**How to install and run ?**

*Download repository, open as python project, create venv for python 3.13, then install requirements:*
```pip install -r requirements.txt```

*After this, just run main.py:*
```python main.py```

**usage in JS:**
```http://localhost:8001//bypass_cors?url=https://www.cors.site```

**example for JS:**

*GET:*
```async function getData() {
  const resp = await fetch(
    "http://localhost:8001//bypass_cors?url=https://www.cors.site/get"
  );
  const data = await resp.json();
  console.log(data);
}
```

*POST:*
```async function postData() {
  const resp = await fetch(
    "http://localhost:8001//bypass_cors?url=https://www.cors.site/post",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hello: "world" })
    }
  );
  const data = await resp.json();
  console.log(data);
}

```
*WITH HEDERS:*
```const resp = await fetch(
  "http://localhost:8001//bypass_cors?url=https://www.cors.site/headers",
  {
    headers: {
      Authorization: "Bearer 123",
      "X-Custom": "abc"
    }
  }
);
```
