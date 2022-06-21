import uvicorn
from untapped.api.resources import app


@app.get("/")
def example():
  return {"hello": "world"}


if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=8000, debug=True)
