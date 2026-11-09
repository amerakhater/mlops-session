from fastapi import FastAPI

app = FastAPI(title="my-project")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
