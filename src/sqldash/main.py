from sqldash.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from sqldash.sqlgen import InputError, generate, TABLES

app = FastAPI()
app.include_router(ops_router, prefix="/v1")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/generate")
def post_generate(body: dict):
    try:
        return generate(body.get("question"))
    except InputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/templates")
def templates():
    return {"templates": [{"name": name, "sql": sql} for name, sql in TABLES.items()], "executed": False}
