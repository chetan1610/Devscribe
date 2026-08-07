from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.posts import router as posts_router
from app.routers.follows import router as follow_router
from app.routers.comments import router as comment_Router
from app.routers.likes import router as likes_router

app=FastAPI(title="devscribe")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(follow_router)
app.include_router(comment_Router)
app.include_router(likes_router)