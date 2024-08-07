import uvicorn

from app.config import get_config


def main():
    uvicorn.run(
        app="app.server:app",
        host=get_config().APP_HOST,
        port=8000,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    main()
