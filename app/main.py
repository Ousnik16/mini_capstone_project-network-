from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.admin_controller import router as admin_router
from app.controllers.assignment_controller import router as assignment_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.network_controller import router as network_router
from app.controllers.ticket_controller import router as ticket_router
from app.core.database import close_mongo_connection, connect_to_mongo
from app.exceptions.exception_handlers import register_exception_handlers
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title="Telecom Fault Management API", version="1.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:3000",       # Alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)

register_exception_handlers(app)

@app.get("/")
def main_function():
    return {"message": "Welcome to the Telecom Fault Management API!"}

app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(assignment_router)
app.include_router(network_router)
app.include_router(admin_router)
