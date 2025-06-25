import logging

import uvicorn
from fastapi import FastAPI
import sys
import os
sys.path.append(os.getcwd())

from src.api import knowledge_endpoints



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="知识库问答系统 API",
    description="基于LangChain和LangGraph的Rag智能问答系统",
    version="1.0.0",
    docs_url="/docs",
)

# 包含路由
app.include_router(knowledge_endpoints.router, prefix="/api/v1/knowledge", tags=["RAG系统"])


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )
