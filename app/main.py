from fastapi import FastAPI
from .database import engine
from .models import user
from .routers import user as user_route

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=user_route.router, prefix="/users", tags=["users"])


