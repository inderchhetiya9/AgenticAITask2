# 🤖 Intelligent AI Agent with RAG & Azure Deployment

A production-ready AI Agent capable of intelligently routing queries between general knowledge (LLM) and specific internal knowledge (Retrieval-Augmented Generation). Built with **FastAPI**, **LangChain**, and **OpenAI**, and fully containerized for deployment on **Azure Container Apps**.

---

## 🏗️ Architecture Overview

The system follows a modular "Router-Retriever" architecture:

1. **API Layer (FastAPI):** Exposes a RESTful endpoint (`POST /ask`) to accept user queries.
2. **Agent Brain (LangChain):** Uses an LLM to analyze the intent of the query.
* *General Query?* → Answers directly using GPT-4o-mini.
* *Specific Query?* → Calls the **Retriever Tool**.


3. **RAG Engine:**
* **Ingestion:** Converts PDFs/Text docs into vector embeddings.
* **Storage:** Stores embeddings in a local **FAISS** vector store.
* **Retrieval:** Fetches relevant context chunks for the agent.


4. **Infrastructure:** Dockerized application running on Azure Container Apps with secure secret management.

```mermaid
graph TD
    User[User] -->|POST /ask| API[FastAPI Backend]
    API --> Agent[Agent Brain (LangChain)]
    Agent -->|Router Logic| Decision{Context Needed?}
    Decision -- No --> LLM[GPT-4o-mini Direct Answer]
    Decision -- Yes --> Tool[Retriever Tool]
    Tool -->|Search| DB[(FAISS Vector DB)]
    DB -->|Context| Tool
    Tool -->|Context + Query| LLM
    LLM -->|Final Response| API

```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| --- | --- | --- |
| **Language** | Python 3.11 | Core logic and scripting. |
| **Framework** | FastAPI | High-performance async API backend. |
| **Orchestration** | LangChain | Agent logic, tool calling, and chain management. |
| **LLM** | OpenAI (GPT-4o-mini) | Reasoning and response generation. |
| **Vector DB** | FAISS | Local efficient similarity search for RAG. |
| **Deployment** | Docker | Containerization for consistent runtime. |
| **Cloud** | Azure Container Apps | Serverless container hosting. |

---

## 🚀 Setup Instructions

### 1. Prerequisites

* Python 3.11+
* Docker Desktop
* Azure CLI (`az`)
* An OpenAI API Key

### 2. Local Installation

**Clone the repository:**

```bash
git clone https://github.com/inderchhetiya9/AgenticAITask2.git
cd AgenticAITask2

```

**Set up environment variables:**
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-proj-your-key-here
ACR_PASSWORD=your-azure-registry-password
ENVIRONMENT_ID=/subscriptions/.../managedEnvironments/ai-agent-env

```

**Install dependencies:**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

**Run the application:**

```bash
uvicorn main:app --reload

```

* Visit Swagger UI: `http://127.0.0.1:8000/docs`

---

### 3. Azure Deployment

This project uses **Infrastructure as Code (IaC)** via a YAML configuration for reproducible deployments.

#### **Step 1: Build & Push Docker Image**

```bash
# Build the image
docker build -t ai-agent:v1 .

# Tag for Azure Container Registry
docker tag ai-agent:v1 myaiagentregistry.azurecr.io/ai-agent:v1

# Push to Azure
docker push myaiagentregistry.azurecr.io/ai-agent:v1

```

#### **Step 2: Deploy Config (Securely)**

**Windows (PowerShell):**

```powershell
# Load secrets from .env and inject them into the template
Get-Content .env | ForEach-Object {
    if ($_ -match '=') {
        $key, $value = $_ -split '=', 2
        Set-Variable -Name $key -Value $value
    }
}

$yaml = Get-Content containerapp.template.yaml -Raw
$yaml = $yaml.Replace('$ACR_PASSWORD', $ACR_PASSWORD)
$yaml = $yaml.Replace('$OPENAI_API_KEY', $OPENAI_API_KEY)
$yaml = $yaml.Replace('$ENVIRONMENT_ID', $ENVIRONMENT_ID)
$yaml | Set-Content containerapp_temp.yaml

# Deploy
az containerapp update --name ai-agent-app --resource-group ai-agent-rg --yaml containerapp_temp.yaml

# Cleanup
Remove-Item containerapp_temp.yaml

```

**Linux / Mac (Bash):**

```bash
# Export variables and deploy using envsubst
set -a && source .env && set +a
envsubst < containerapp.template.yaml | az containerapp update \
  --name ai-agent-app \
  --resource-group ai-agent-rg \
  --yaml -

```

---

## 💡 Design Decisions

* **Hybrid File Structure:** Originally, the project separated `app/` and root files strictly. I moved to a flat structure in the container (copying everything to `/app`) to resolve Python's relative import issues while keeping the local development folder clean.
* **Agent vs. Chain:** Instead of a simple RAG chain, I implemented an **Agent**. This allows the system to scale—we can easily add tools like "Google Search" or "Calculator" later without rewriting the core logic.
* **FAISS (Local) vs. Pinecone:** For this assignment, I chose FAISS (CPU) for simplicity and zero-cost deployment. It runs entirely inside the container, removing the need for external database connections.
* **YAML-based Deployment:** Instead of running long CLI commands, I used a parameterized YAML file (`containerapp.template.yaml`). This treats infrastructure as code and prevents secret leakage in git commits.

---

## ⚠️ Limitations & Future Improvements

1. **Memory Persistence:**
* *Current:* The FAISS index is static and baked into the Docker image. New documents uploaded via API are lost on restart.
* *Future:* Switch to **Azure AI Search** or **Pinecone** for persistent, scalable vector storage.


2. **Session History:**
* *Current:* Basic session handling.
* *Future:* Integrate Redis (Azure Cache for Redis) to store conversation history for stateful multi-turn chats.


3. **Security:**
* *Current:* Basic API Key protection.
* *Future:* Implement OAuth2 (Azure AD) for endpoint protection.



---

### **Project Structure**

```text
/
├── app/                 # Source code (moved to root in Docker)
│   ├── agent_brain.py   # LangChain agent definition
│   ├── rag_engine.py    # Vector store & retrieval logic
│   └── tools.py         # Custom tool definitions
├── docs/                # Knowledge base documents (PDFs)
├── faiss_index/         # Pre-computed vector embeddings
├── containerapp.template.yaml  # Deployment config template
├── Dockerfile           # Container definition
├── main.py              # FastAPI entry point
└── requirements.txt     # Python dependencies

```