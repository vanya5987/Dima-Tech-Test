from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError

from src.api.webhook_api import router as webhook_router
from src.api.auth_api import router as auth_router
from src.api.user_api import router as user_router
from src.api.admin_api import router as admin_router
from src.api.test_router import router as test_router

from src.server.server_runner import ServerRunner

app = FastAPI()

app.include_router(webhook_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(test_router)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    if isinstance(exc, OperationalError):
        detail = "Database is unavailable. Please try again later."
    elif isinstance(exc, ProgrammingError):
        detail = "Database schema error."
    else:
        detail = "Unexpected database error."

    return JSONResponse(status_code=503, content={"detail": detail},)

if __name__ == "__main__":
    ServerRunner.create_and_run_server(reflection_name="src.main:app", port=8888, host="0.0.0.0", reload=False)