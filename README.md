# AgenticAITask2
Agentic AI with basic RAG


docker build -t ai-agent:v2 .
docker tag ai-agent:v2 myaiagentregistry.azurecr.io/ai-agent:v2
docker push myaiagentregistry.azurecr.io/ai-agent:v2

az containerapp update --name ai-agent-app --resource-group ai-agent-rg --yaml containerapp.yaml

