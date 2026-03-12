"""FastAPI application factory + lifespan."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.v1 import v1_router
from .db.engine import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="AgentWeave Hub",
        description=(
            "Self-hosted collaboration server for AgentWeave agents. "
            "Provides REST + SSE + MCP interfaces for messages, tasks, and human interaction."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(v1_router)
    return app


app = create_app()


def run() -> None:
    """Entry point for `agentweave-hub` CLI command."""
    import uvicorn
    from .config import settings

    uvicorn.run("hub.main:app", host="0.0.0.0", port=settings.aw_port, reload=False)


if __name__ == "__main__":
    run()
