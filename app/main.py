from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import register, login, employee
from app.utils.file_storage import initialize_metadata
from contextlib import asynccontextmanager
from .loginwithlogging import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_metadata()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(mw_log_request)


app.include_router(register.router, prefix="/api")
app.include_router(login.router, prefix="/api")
app.include_router(employee.router, prefix="/api")

