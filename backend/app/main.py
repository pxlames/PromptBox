from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routes import router as prompt_router


def create_app() -> FastAPI:
    app = FastAPI(title="Prompt Manager API", version="0.1.0")

    # Basic CORS; can be tightened later
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DB init
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(prompt_router)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()


