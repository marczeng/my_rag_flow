from src.core.query_knowledge import RetrievalWorkflow

func = RetrievalWorkflow()

if __name__ == "__main__":
    import json
    query = "5G推动了哪些新兴业态展现发展潜力"
    query_traslation = True
    state = func.query_knowledge(
        sessionId="123",query=query,query_translation=query_traslation
        )
    print(json.dumps(state["cache_state"],ensure_ascii=False,indent=4))
    

