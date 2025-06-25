import logging
from typing import Dict, Any, Optional,Union,List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.core.knowledge_workflow import UserKnowledgeWorkflow,knowledgeWorkflowState
from src.core.query_knowledge import RetrievalWorkflowState,RetrievalWorkflow

logger = logging.getLogger(__name__)
router = APIRouter()

class ProfileGenerationRequest(BaseModel):
    # 以下字段对应 knowledgeWorkflowState 的部分字段
    sessionId: str = Field(..., description="会话ID")
    input_files: Union[str, List[str]] = Field(...,description="输入文件")
    cache: bool = Field(default=False, description="是否启用缓存")  # 默认 False
    vec_db_category: str = Field(default=None, description="向量数据库类别")
    file_type: str = Field(default='docx', description="文件类型，默认 docx")  # 默认 docx
    file_extension: str = Field(default=None, description="文件扩展名")
    embedding_model_name: str = Field(default=None, description="Embedding 模型名称")

class ProfileResponse(BaseModel):
    """响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(description="响应消息")

class QueryRequest(BaseModel):
    # 以下字段对应 knowledgeWorkflowState 的部分字段
    sessionId: str = Field(..., description="会话ID")
    methods: str = Field(default=None, description="相似度计算方法")
    topk: int  = Field(default=1, description="返回个数")
    question : str = Field(..., description="用户输入的问题")
    query_translation: bool = Field(..., description="是否转述问题")
    vec_db_category: str = Field(default=None, description="向量数据库类别")
    embedding_model_name: str = Field(default=None, description="Embedding 模型名称")
    
class QueryResponse(BaseModel):
    # 以下字段对应 knowledgeWorkflowState 的部分字段
    sessionId: str = Field(..., description="会话ID")
    message: Optional[Any] = Field(
        default=None,
        description="查询操作的结果数据，任意类型"
    )


# 初始化核心组件
workflow_engine = UserKnowledgeWorkflow()

@router.post("/generate", response_model=ProfileResponse)
async def generate_profile(request: ProfileGenerationRequest):
    """
    将 文档 存入知识库
    sessionId: str, input_files: Dict[str, Union[str, list]],cache: bool,
        vec_db_category: str, file_type : str, file_extension : str
    """
    try:
        user_profile = workflow_engine.generate_knowledge_base(
            sessionId = request.sessionId,
            input_files = request.input_files,
            cache = request.cache,
            vec_db_category = request.vec_db_category,
            file_type = request.file_type,
            file_extension = request.file_extension,
            # embedding_model_name = request.embedding_model_name

        )
        return ProfileResponse(
            success=True,
            message="文档导入成功"
        )
    except Exception as e:
        logger.exception(f"导入文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"导入文档失败: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    try:
        retrieval_engine = RetrievalWorkflow()
        query_response = retrieval_engine.query_knowledge(
                sessionId = request.sessionId,
                query = request.question,
                query_translation = request.query_translation

            )
        return QueryResponse(
            sessionId=request.sessionId,
            message=query_response
        )
    except Exception as e:
        logger.exception(f"问题检索失败: {e}")
        raise HTTPException(status_code=500, detail=f"问题检索失败: {str(e)}")



