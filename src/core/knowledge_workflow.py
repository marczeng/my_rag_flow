import os
import json
import logging
from typing import Dict, List, Any, TypedDict, Annotated,Union

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph


from src.core.docx_parser.docx_process import ParserDocx
from src.core.docx_parser.doc2docx import convert_doc_to_docx
from src.core.docx_parser.docx_helper import return_file_name
from src.core.docx_parser.docx_helper import merge_sub_chunck as merge
from src.core.pdf_parser.pdf_process import ParserPDF
from src.core.models.embeddings import Embedding
from src.core.save_to_cache.insert2mo import insert2mo 


logger = logging.getLogger(__name__)

class knowledgeWorkflowState(TypedDict):
    """工作流状态定义"""
    sessionId:str
    input_files: Dict[str, Union[str, list]]      # 新增文档
    error_messages: List[str]
    cache: bool                     # 是否缓存
    cache_states : Dict[str, Any] 
    vec_db_category:str             # 向量数据库类别
    workflow_status: str
    file_type : str                 # 文件类别
    file_extension : str            # 文件扩展名
    embedding_model_name: str       # embedding 模型名称
    messages: Annotated[List, add_messages]

class UserKnowledgeWorkflow:
    """
    为生成知识库搭建工作流
    """

    def __init__(self):
        self.docx_processor = ParserDocx()
        self.pdf_processor = ParserPDF()

        # 构建工作流
        self.workflow = self._build_workflow()
        self.embedding = Embedding()

    def _build_workflow(self) -> CompiledStateGraph:
        """构建工作流图"""
        workflow = StateGraph(knowledgeWorkflowState)

        # 添加节点
        workflow.add_node("validate_input", self._validate_input)

        # 为AF、AT、AW、AY、AZ等文件类型及扩展添加节点
        workflow.add_node("parser_docx",self._parser_docx)
        workflow.add_node("parser_pdf",self._parser_pdf)

        # 将doc文件转换成docx文件
        workflow.add_node("doc2docx",self._doc2docx)
        workflow.add_node("return_file_name",self._return_file_name)
        workflow.add_node("merge_sub_chuncks",self._merge_sub_chuncks)
        # embedding服务
        workflow.add_node("save_to_cache",self._save_to_cache)
        workflow.add_node("error_handler",self._error_handler)

        # 设置入口点
        workflow.set_entry_point("validate_input")
        # 添加条件边
        workflow.add_conditional_edges(
            "validate_input",
            self._route_by_category_and_extension,  # 统一判断函数
            {
                # AF 类别 + 文件类型
                "AF_doc": "doc2docx",
                "AF_docx": "parser_docx",
                "AF_pdf": "parser_pdf",

                # AZ 类别 + 文件类型
                "AZ_doc": "doc2docx",
                "AZ_docx": "parser_docx",
                "AZ_pdf": "parser_pdf",

                # AY 类别 + 文件类型
                "AY_doc": "doc2docx",
                "AY_docx": "parser_docx",
                "AY_pdf": "parser_pdf",

                # AW 类别 + 文件类型
                "AW_doc": "doc2docx",
                "AW_docx": "parser_docx",
                "AW_pdf": "parser_pdf",

                # AT 类别 + 文件类型
                "AT_doc": "doc2docx",
                "AT_docx": "parser_docx",
                "AT_pdf": "parser_pdf",

                # 错误处理
                "error": "error_handler"
            }
        )

        workflow.add_edge("doc2docx","parser_docx")
        workflow.add_edge("parser_docx","return_file_name")
        workflow.add_edge("return_file_name","merge_sub_chuncks")

        workflow.add_edge("merge_sub_chuncks", "save_to_cache")
        # workflow.add_edge("parser_pdf", "save_to_cache")
        
        workflow.add_conditional_edges(
            "save_to_cache",
            self._should_end_workflow,
            {
                "end": END,
                "error": "error_handler"
            }
        )
        workflow.add_edge("error_handler", END)
        return workflow.compile()

    @staticmethod
    def _should_end_workflow(state: knowledgeWorkflowState) -> str:
        """判断是否结束工作流"""
        if state["workflow_status"] == "completed":
            return "end"
        else:
            return "error"

    @staticmethod
    def _validate_input(state: knowledgeWorkflowState) -> knowledgeWorkflowState:
        """验证输入数据"""
        sessionId = state["sessionId"]
        input_files = state["input_files"]

        state["messages"].append(HumanMessage(content=f"开始为业务编号为 {sessionId} 的任务生成知识库"))

        if not sessionId:
            state["error_messages"].append("业务编号不能为空！！！")
            state["workflow_status"] = "error"
            return state

        if not input_files:
            state["error_messages"].append("输入文件不能为空！！！")
            state["workflow_status"] = "error"
            return state

        state["messages"].append(AIMessage(content="输入数据验证通过"))
        return state

    def generate_knowledge_base(
        self, sessionId: str, input_files: Dict[str, Union[str, list]],cache: bool,
        vec_db_category: str, file_type : str, file_extension : str
        ):# -> UserProfile:
        """
        开始入口
        """
        initial_state = knowledgeWorkflowState(
            sessionId=sessionId,
            input_files=input_files,
            cache=cache,
            vec_db_category=vec_db_category,
            file_type = file_type,
            file_extension = file_extension,
            error_messages=[],
            workflow_status="running",
            messages=[]
        )
        # 执行工作流
        final_state = self.workflow.invoke(initial_state)
        logger.info(f"工作流执行完成，执行结果：\n {json.dumps(final_state, indent=4, ensure_ascii=False, default=str)}")
        if final_state["workflow_status"] == "completed":
            print("所有流程全部执行完毕！！！")

        else:
            raise Exception(f"Profile generation failed: {final_state['error_messages']}")

    @staticmethod
    def _error_handler(state: knowledgeWorkflowState) -> knowledgeWorkflowState:
        """错误处理"""
        state["workflow_status"] = "error"
        error_summary = "; ".join(state["error_messages"])
        state["messages"].append(AIMessage(content=f"工作流执行失败: {error_summary}"))
        return state

    @staticmethod
    def _route_by_category(state: knowledgeWorkflowState) -> str:
        """
        根据文档类别（AF/AZ/AY等）
        """
        category = state.get("file_type")  # 如 AF/AZ/AY
        if not category or category not in ["AF", "AZ", "AY", "AW", "AT"]:
            return "error"
        return category

    @staticmethod
    def _route_by_category_and_extension(state: knowledgeWorkflowState) -> str:
        """
        根据文档类别（AF/AZ/AY等）和文件扩展名（.doc/.docx/.pdf）决定路由。
        返回值格式为 "{category}_{ext}"，如 "AF_docx"。
        """

        category = state.get("file_type")  # 如 AF/AZ/AY
        ext = state.get("file_extension")  # 如 .doc/.docx/.pdf

        if not category or category not in ["AF", "AZ", "AY", "AW", "AT"]:
            return "error"

        if ext == "doc":
            return f"{category}_doc"
        elif ext == "docx":
            return f"{category}_docx"
        elif ext == "pdf":
            return f"{category}_pdf"
        else:
            return "error"

    def _doc2docx(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始进行文件类型（doc -> docx）转换")
        sessionId = state["sessionId"]
        try:
            tags =  self._route_by_category(state)
            input_files = state["input_files"]
            if tags != "error":
                file_root = os.path.join("data","docx","{}-folder".format(tags))
                if isinstance(input_files,str):
                    target_path = convert_doc_to_docx(input_files,file_root)
                    state["input_files"] = target_path
                    os.remove(input_files)
                else:
                    temp = []
                    for cur_file in input_files:
                        target_path = convert_doc_to_docx(cur_file,file_root)
                        temp.append(target_path)
                        os.remove(cur_file)
                    state["input_files"] = temp
                state["messages"].append(AIMessage(content="文件类型（doc -> docx）转换完毕~"))
            else:
                state["error_messages"].append(f"文件转换失败: {str(e)}")
                state["messages"].append(AIMessage(content=f"文件转换出错: {str(e)}"))

        except Exception as e:
            logger.exception(f"文件转换失败：{str(e)}")
            state["error_messages"].append(f"文件转换失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"文件转换出错: {str(e)}"))

        return state

    def _parser_pdf(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始解析 PDF 文件 ......")
        try:
            cache_result = self.pdf_processor.main(state)
            state["cache_states"] = cache_result
            state["messages"].append(AIMessage(content="PDF 文件解析完毕~"))
        except Exception as e:
            logger.exception(f"PDF 文件解析失败：{str(e)}")
            state["error_messages"].append(f"PDF 文件解析失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"PDF 文件解析出错: {str(e)}"))
            state["workflow_status"] = "error"
        return state

    def _parser_docx(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始解析 docx 文件 ......")
        sessionId = state["sessionId"]
        try:
            cache_result = self.docx_processor.main(state)
            state["cache_states"] = cache_result
            state["messages"].append(AIMessage(content="docx 文件解析完毕~"))

        except Exception as e:
            logger.exception(f"docx 文件解析失败：{str(e)}")
            state["error_messages"].append(f"docx 文件解析失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"docx 文件解析出错: {str(e)}"))
        return state

    def _return_file_name(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始识别文件题目 ......")
        sessionId = state["sessionId"]
        try:
            cache_states = state["cache_states"]
            for file,details in cache_states.items():
                filename,index = return_file_name(details,file)
                data = {
                        "file_name":filename,
                        "index":index,
                        "details":details
                    }
                cache_states[file] = data
            state["cache_states"] = cache_states
            state["messages"].append(AIMessage(content=f"文件题目解析完毕~"))
        except Exception as e:
            logger.exception(f"文件题目解析失败：{str(e)}")
            state["error_messages"].append(f"文件题目解析失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"文件题目解析出错: {str(e)}"))
        return state

    def _merge_sub_chuncks(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始合并段落 ......")
        sessionId = state["sessionId"]
        try:
            cache_states = state["cache_states"]
            for file,details in cache_states.items():
                index = details["index"]
                cur_details = details["details"]
                cur_chunks_result,cur_table_result = merge(file,index,cur_details)
                details["details"] = cur_chunks_result
                details["table"] = cur_table_result
                cache_states[file] = details
            state["cache_states"] = cache_states
            state["messages"].append(AIMessage(content=f"分页的段落合并完毕~"))
            
        except Exception as e:
            logger.exception(f"段落合并失败：{str(e)}")
            state["error_messages"].append(f"文件题目解析失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"文件题目解析出错: {str(e)}"))
        return state
        
    def _save_to_cache(self,state:knowledgeWorkflowState) -> knowledgeWorkflowState:
        logger.info("开始对文本进行embeddings ......")
        sessionId = state["sessionId"]
        try:
            cache_states = state["cache_states"]
            file_type = state["file_type"]
   
            for file,details in cache_states.items():
                file_name = details["file_name"]
                cur_file_details = details["details"]
                cur_table_details = details["table"]
                insert2mo[file_type](file,file_name,cur_table_details,cur_file_details,self.embedding)
            state["messages"].append(AIMessage(content=f"文件 {file} 已经成功插入向量数据库中...."))
            state["workflow_status"] = "completed"
            
        except Exception as e:
            logger.exception(f"段落插入向量数据库失败：{str(e)}")
            state["error_messages"].append(f"段落插入向量数据库失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"段落插入向量数据库出错: {str(e)}"))
        return state

    