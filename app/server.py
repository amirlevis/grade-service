from typing import List

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.config import get_config, Config
from app.middlewares.sqlalchemy import SQLAlchemyMiddleware
from app.models.models import APIResponse
from app.routers import grade_routes


def init_listeners(app_: FastAPI) -> None:
    # Exception handler

    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(APIResponse[str](error=exc.errors())),
        )

    @app_.exception_handler(SQLAlchemyError)
    async def sql_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(APIResponse(error=str(exc))),
        )

    @app_.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(APIResponse(error=str(exc))),
        )


def make_middleware(engine_url: str) -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware,
                   engine_url=engine_url),

    ]
    return middleware


def create_app(configs: Config) -> FastAPI:
    app_ = FastAPI(
        title=configs.TITLE,
        description=configs.DESCRIPTION,
        version=configs.VERSION,
        middleware=make_middleware(engine_url=configs.get_db_url()),
    )
    app_.include_router(grade_routes.router, prefix="/api")
    init_listeners(app_=app_)
    return app_


app = create_app(get_config())
