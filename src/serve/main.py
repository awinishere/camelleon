from fastapi import FastAPI

from serve.database import Base, engine
from serve.features.authentication.routes import router as authentication_router

app = FastAPI()

app.include_router(authentication_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "serve.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )