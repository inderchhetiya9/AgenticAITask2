from pydantic import BaseModel, Field


class ResponseFromLLM(BaseModel):
    "Give the details of your response and its source."

    response: str = Field(description="The detailed answer to the user's query.")
    source: list[str] = Field(
        description="The list of source document or reference for the information provided. If not using any documents only then return ['General Knowledge']."
    )


# --- Data Models ---
class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None
