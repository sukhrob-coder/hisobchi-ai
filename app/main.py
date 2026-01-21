from fastapi import FastAPI

from .api import auth, user
from .core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hisobchi.ai API")

app.include_router(auth.router)
app.include_router(user.router)
