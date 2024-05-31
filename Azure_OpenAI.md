# Create and deploy an Azure OpenAI Service resource

Follow below steps to create a resource and deploy a model:

* Create an Azure OpenAI resource and Deploy models refere Microsoft documentation -<https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal>

## Here are the requirements for Azure OpenAI models

### Embeddings model used for kafka.py

- Model name: text-embedding-ada-002
- Model version: 2
- Deployment type: Standard
- Content Filter: medical-filter
- Tokens per Minute Rate Limit (thousands): 1000
- Rate limit (Tokens per minute): 1000000
- Rate limit (Requests per minute): 6000

### Chat model used for chat_app.py

- Model name: gpt-35-turbo-16k
- Model version: 0613
- Deployment type: Standard
- Content Filter: medical-filter
- Tokens per Minute Rate Limit (thousands): 240
- Rate limit (Tokens per minute): 240000
- Rate limit (Requests per minute): 1440
