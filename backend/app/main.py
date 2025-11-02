from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .db import Base, engine
from .routes import router as prompt_router, resume_router, okr_router, interview_router, opinion_router
from .assistant_routes import assistant_router


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

    # 挂载静态文件目录
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

    # Routers
    app.include_router(prompt_router)
    app.include_router(resume_router)
    app.include_router(okr_router)
    app.include_router(interview_router)
    app.include_router(opinion_router)
    app.include_router(assistant_router)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()


