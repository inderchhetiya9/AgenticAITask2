from langchain.tools import tool
from app.rag_engine import get_retriever

retriever = get_retriever()


@tool
def search_company_policy(query: str, limit: int = 10) -> str:
    """Search the company policy database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    results = retriever.invoke(query, top_k=limit)
    res_str = ""

    for doc in results:
        res_str += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
        res_str += f"Content: {doc.page_content}\n\n"

    return res_str


tools = [search_company_policy]
