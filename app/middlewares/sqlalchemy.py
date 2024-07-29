from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.types import Receive, Scope, Send, ASGIApp


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp, engine_url: str):
        self.app = app
        self.engine = create_async_engine(engine_url, echo=True)
        self.async_sessionmaker = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session = self.async_sessionmaker()
        # Everything is the same from here
        scope["session"] = session
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.commit()
            await session.close()
