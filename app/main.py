from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import servicios


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="API de Reservas",
    description="Sistema de reservas para una barbería: servicios y citas.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(servicios.router)


@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API de reservas funcionando", "documentacion": "/docs"}