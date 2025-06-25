# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/6/20 13:57
import json
import logging
from typing import Dict, List, Any, TypedDict, Annotated

from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END

from src.core.models.rewrite_question import ope_question, rewrite_template
from src.core.models.embeddings import Embedding
from src.core.models.search import Search
from src.core.models.reranker import BgeRerank

logger = logging.getLogger(__name__)


class RetrievalWorkflowState(TypedDict):
    """工作流状态定义"""
    sessionId: str
    query: Dict[str, Any]               # 待查询的问题
    query_traslation: bool              # 是否转述问题
    cache_state: Dict[str, Any] 
    error_messages: List[str]
    workflow_status: str
    messages: Annotated[List, add_messages]

class RetrievalWorkflow:
    """用户画像生成工作流"""

    def __init__(self):
        # 构建工作流图
        self.workflow = self._build_workflow()
        self.emb_func = Embedding()
        self.reranker = BgeRerank()
        self.search = Search(self.emb_func)

    def _build_workflow(self) -> CompiledStateGraph:
        """构建工作流图"""
        workflow = StateGraph(RetrievalWorkflowState)
        # 添加节点
        workflow.add_node("validate_input", self._validate_input)
        workflow.add_node("query_translation", self._query_translation)
        workflow.add_node("search_knowledge", self._search_knowledge)
        workflow.add_node("error_handler", self._error_handler)
        workflow.add_node("reranker",self._reranker)

        # 设置入口点
        workflow.set_entry_point("validate_input")

        workflow.add_conditional_edges(
            "validate_input",
            self._should_query_translate,
            {
                "Yes": "query_translation",
                "No": "search_knowledge"
            }
        )
        workflow.add_edge("query_translation", "search_knowledge")
        workflow.add_edge("search_knowledge","reranker")
        workflow.add_conditional_edges(
            "reranker",
            self._should_end_workflow,
            {
                "end": END,
                "error": "error_handler"
            }
        )

        workflow.add_edge("error_handler", END)
        return workflow.compile()

    @staticmethod
    def _should_end_workflow(state: RetrievalWorkflowState) -> str:
        """判断是否结束工作流"""
        if state["workflow_status"] == "completed":
            return "end"
        else:
            return "error"

    def query_knowledge(self, sessionId: str, query: Dict[str, Any], query_translation: bool):
        # 初始化状态
        initial_state = RetrievalWorkflowState(
            sessionId=sessionId,
            query=query,
            query_traslation=query_translation,
            cache_state={},
            error_messages=[],
            workflow_status="running",
            messages=[]
        )
        # 执行工作流
        final_state = self.workflow.invoke(initial_state)
        logger.info(f"工作流执行完成，执行结果：\n {json.dumps(final_state, indent=4, ensure_ascii=False, default=str)}")
        if final_state["workflow_status"] == "completed":
            print("所有流程全部执行完毕！！！")
            return final_state
        else:
            raise Exception(f"Profile generation failed: {final_state['error_messages']}")

    @staticmethod
    def _error_handler(state: RetrievalWorkflowState) -> RetrievalWorkflowState:
        """错误处理"""
        state["workflow_status"] = "error"
        error_summary = "; ".join(state["error_messages"])
        state["messages"].append(AIMessage(content=f"工作流执行失败: {error_summary}"))
        return state

    @staticmethod
    def _validate_input(state: RetrievalWorkflowState) -> RetrievalWorkflowState:
        """验证输入数据"""
        sessionId = state["sessionId"]
        query = state["query"]
        state["messages"].append(HumanMessage(content=f"开始为业务编号为 {sessionId} 的任务生成知识库"))
        if not sessionId:
            state["error_messages"].append("业务编号不能为空！！！")
            state["workflow_status"] = "error"
            return state
        if not query:
            state["error_messages"].append("输入的问题不能为空！！！")
            state["workflow_status"] = "error"
            return state

        state["messages"].append(AIMessage(content="输入数据验证通过"))
        return state

    @staticmethod
    def _should_query_translate(state: RetrievalWorkflowState) -> str:
        """判断是否进行查询翻译"""
        if state["query_traslation"]:
            return "Yes"
        else:
            return "No"

    def debug(self, param=None):
        if param:
            print(json.dumps(param, ensure_ascii=False, indent=4))
        s = input("push to exit ...")
        exit()

    def _query_translation(self, state: RetrievalWorkflowState) -> RetrievalWorkflowState:
        sessionId = state["sessionId"]
        try:
            query = state["query"]
            translate_result = ope_question(rewrite_template, query)
            state["cache_state"]["translated_query"] = translate_result
            state["workflow_status"] = "completed"
            state["messages"].append(AIMessage(content="查询翻译成功"))

        except Exception as e:
            logger.exception(f"文件转换失败：{str(e)}")
            state["error_messages"].append(f"文件转换失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"文件转换出错: {str(e)}"))
            state["workflow_status"] = "error"
        return state

    def filter_repeat(self,params):
        result = []
        dic = {}
        for unit in params:
            cur_chunk = unit["chunks"].replace(" ","")
            if cur_chunk not in dic:
                dic[cur_chunk] = 1
                result.append(unit)
        return result

    def add_score(self,search_result,rerank_result):
        for i,unit in enumerate(search_result):
            unit["score"] = rerank_result[i]
            search_result[i] = unit
        search_result = sorted(search_result, key=lambda x: x["score"], reverse=True)
        return search_result

    def _search_knowledge(self, state: RetrievalWorkflowState) -> RetrievalWorkflowState:
        """
        对问题进行 embeddings
        """
        sessionId = state["sessionId"]
        try:
            query = state["query"]
            sub_cache = []
            cache_state = state["cache_state"]
            if state["query_traslation"]:
                try:
                    query_list = json.loads(cache_state["translated_query"])
                    for sub_query in query_list:
                        bm25_result = self.search.get_bm25_result(sub_query)
                        sub_chunks_result = self.search.get_subchunk_result(sub_query)
                        cur_question_result = bm25_result + sub_chunks_result
                        question_result = self.filter_repeat(cur_question_result)
                        sub_cache.append(
                            {
                                "query": sub_query,
                                "bm25_result": bm25_result,
                                "chunks_result":sub_chunks_result,
                                "search_result":question_result
                            }
                        )
                except:
                    bm25_result = self.search.get_bm25_result(query)
                    sub_chunks_result = self.search.get_subchunk_result(query)
                    cur_question_result = bm25_result + sub_chunks_result
                    question_result = self.filter_repeat(cur_question_result)
                    sub_cache.append(
                        {
                            "query": query,
                            "bm25_result": bm25_result,
                            "chunks_result":sub_chunks_result,
                            "search_result":question_result
                        }
                    )
            else:
                bm25_result = self.search.get_bm25_result(query)
                sub_chunks_result = self.search.get_subchunk_result(query)
                cur_question_result = bm25_result + sub_chunks_result
                question_result = self.filter_repeat(cur_question_result)
                sub_cache.append(
                    {
                        "query": query,
                        "bm25_result": bm25_result,
                        "chunks_result":sub_chunks_result,
                        "search_result":question_result
                    }
                )
    
            state["cache_state"] = sub_cache


            state["messages"].append(AIMessage(content="嵌入向量化成功"))

        except Exception as e:
            logger.exception(f"嵌入向量化失败：{str(e)}")
            state["error_messages"].append(f"嵌入向量化失败: {str(e)}")
            state["messages"].append(AIMessage(content=f"嵌入向量化出错: {str(e)}"))
            state["workflow_status"] = "error"
        return state

    def _reranker(self, state: RetrievalWorkflowState) -> RetrievalWorkflowState:
        sessionId = state["sessionId"]
        try:
            query = state["query"]
            sub_cache = []
            cache_state = state["cache_state"]
            result = {}
            for sub_query_result in cache_state:
                cur_result_score = self.reranker.get_result(sub_query_result["query"],sub_query_result["search_result"])
                cur_result = self.add_score(sub_query_result["search_result"],cur_result_score)
                result[sub_query_result["query"]] = cur_result
            state["cache_state"] = result
            state["workflow_status"] = "completed"
            state["messages"].append(AIMessage(content="检索+召回成功"))

        except Exception as e:
            logger.exception(f"检索+召回成功：{str(e)}")
            state["error_messages"].append(f"检索+召回成功: {str(e)}")
            state["messages"].append(AIMessage(content=f"检索+召回成功: {str(e)}"))
            state["workflow_status"] = "error"
        return state



