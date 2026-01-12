from fastapi import FastAPI, HTTPException
from app.agent_brain import get_agent_response
from app.rag_engine import ingest_documents
from app.models import QueryRequest, ResponseFromLLM

app = FastAPI(title="AI Agent API")

# --- Endpoints ---


@app.post("/ask", response_model=ResponseFromLLM)
async def ask_agent(request: QueryRequest):
    try:
        # Run the agent
        result = get_agent_response(request.query)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
async def upload_docs():
    # Endpoint to trigger document indexing manually
    ingest_documents(["docs/it_policy.txt", "docs/hr_policy.txt"])
    # You would typically accept file uploads here
    return {"message": "Indexed the documents successfully."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
