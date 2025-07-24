# Local Development Guide: Online Boutique

This guide helps you run all core microservices of Online Boutique **locally** with Docker Compose.

---

## 1. **Prerequisites**

- [Docker](https://docs.docker.com/get-docker/) installed (and Docker Compose v2+)
- Clone this repository:
    ```sh
    git clone <your-fork-url>
    cd online-boutique
    ```

---

## 2. **Shopping Assistant Service Overview**

The **Shopping Assistant Service** is an AI-powered interior design assistant that provides personalized product recommendations based on room images and user requests. It uses:

### **What it does:**
- 📷 **Image Analysis**: Analyzes room photos using Google's Gemini Vision API
- 🛋️ **Style Recognition**: Identifies interior design styles and aesthetics
- 🔍 **Vector Search**: Performs semantic search through product catalog using embeddings
- 🤖 **AI Recommendations**: Generates personalized product suggestions
- 📝 **Natural Language**: Provides conversational recommendations with explanations

### **Architecture:**
```
User Request + Room Image → Gemini Vision → Room Style Analysis
                              ↓
Product Vector Database ← Semantic Search ← Style + User Request
                              ↓
Relevant Products → Gemini Pro → Personalized Recommendations
```

---

## 3. **Platform Deployment Options**

### **🚀 Local Development (No Cloud)**
Use the mock service for local development without any cloud dependencies:

```sh
# Use mock service (no AI, but realistic responses)
docker compose -f docker-compose.yml -f docker-compose.mock.yml up
```

The mock service provides realistic responses without requiring cloud credentials.

### **☁️ Google Cloud Platform (GCP)**
For full AI functionality on GCP:

**Required Services:**
- Google Cloud AlloyDB (Vector database)
- Google Secret Manager (Credentials)
- Gemini API access
- Container Registry/Artifact Registry

**Environment Variables:**
```bash
PROJECT_ID=your-gcp-project
REGION=us-central1
ALLOYDB_CLUSTER_NAME=your-cluster
ALLOYDB_INSTANCE_NAME=your-instance
ALLOYDB_DATABASE_NAME=boutique
ALLOYDB_TABLE_NAME=products
ALLOYDB_SECRET_NAME=alloydb-password
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### **🔷 Microsoft Azure**
For Azure deployment with equivalent services:

**Required Services:**
- Azure Database for PostgreSQL with pgvector extension
- Azure Key Vault (Secret management)
- Azure OpenAI Service (Alternative to Gemini)
- Azure Container Registry

**Modifications needed:**
- Replace `langchain_google_genai` with `langchain_openai` 
- Replace `langchain_google_alloydb_pg` with `langchain_postgres`
- Replace Google Secret Manager with Azure Key Vault
- Update authentication to use Azure identity

### **🏢 On-Premises**
For on-premises deployment:

**Required Infrastructure:**
- PostgreSQL with pgvector extension
- OpenAI API access or local LLM (Ollama, etc.)
- Container orchestration (Kubernetes/Docker Swarm)

**Modifications needed:**
- Replace cloud secret management with environment variables/config files
- Use local PostgreSQL with pgvector
- Configure local or API-based LLM providers

### **🌐 AWS**
For AWS deployment:

**Required Services:**
- Amazon RDS PostgreSQL with pgvector
- AWS Secrets Manager
- Amazon Bedrock (for AI models)
- Amazon ECR

**Modifications needed:**
- Replace AlloyDB with RDS PostgreSQL
- Replace Google Secret Manager with AWS Secrets Manager  
- Replace Gemini with Amazon Bedrock models
- Update authentication to use AWS IAM

---

## 4. **Configure Cloud Services (Optional)**

### **For Google Cloud (Full AI Features):**

1. **Set up AlloyDB and populate with product vectors**:
   ```sh
   # Create AlloyDB cluster with AI extensions enabled
   gcloud alloydb clusters create boutique-cluster \
     --region=us-central1 \
     --enable-ai
   ```

2. **Configure environment variables**:
   ```sh
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your GCP credentials and AlloyDB details
   # PROJECT_ID="your-gcp-project"
   # REGION="us-central1"
   # ALLOYDB_CLUSTER_NAME="boutique-cluster"
   # etc.
   ```

### **For Azure (Alternative AI Setup):**

1. **Create Azure OpenAI resource**:
   ```sh
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name online-boutique-dev --location eastus
   
   # Create Azure OpenAI service
   az cognitiveservices account create \
     --name online-boutique-openai \
     --resource-group online-boutique-dev \
     --kind OpenAI \
     --sku s0 \
     --location eastus
   ```

2. **Set up PostgreSQL with pgvector**:
   ```sh
   # Create PostgreSQL server with pgvector support
   az postgres flexible-server create \
     --name online-boutique-db \
     --resource-group online-boutique-dev \
     --location eastus \
     --admin-user boutique_admin \
     --sku-name Standard_B1ms \
     --storage-size 32 \
     --version 14
   ```

---

## 5. **Build & Run All Services**

### **🚀 Quick Start (Mock Mode - No Cloud Required):**
```sh
# Run with mock AI service (recommended for local development)
docker compose -f docker-compose.yml -f docker-compose.mock.yml up --build
```

### **☁️ Full AI Mode (Requires Cloud Setup):**
```sh
# Run with full AI capabilities (requires GCP/Azure setup)
docker compose up --build
```

### **🔧 Individual Service Testing:**
```sh
# Test just the shopping assistant service
docker compose up --build shoppingassistantservice

# Test with mock service
docker build -t shopping-assistant-mock -f src/shoppingassistantservice/Dockerfile.mock src/shoppingassistantservice/
docker run -p 8080:8080 shopping-assistant-mock
```

---

## 6. **API Usage Examples**

### **Shopping Assistant API:**

**Endpoint:** `POST http://localhost:8080/`

**Request Format:**
```json
{
  "message": "I need something cozy for my living room",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```

**Response Format:**
```json
{
  "content": "Based on your beautiful modern living room, I recommend these cozy items:\n\n1. **Candle Set** - Aromatic candles to create a cozy atmosphere\n2. **Bamboo Glass Jar** - Stylish storage that adds warmth\n3. **Salt & Pepper Shakers** - Elegant dining accessories\n\n[0PUK6V6EV0], [9SIQT8TOJO], [LS4PSXUNUM]"
}
```

### **Testing with curl:**
```sh
# Test health endpoint
curl http://localhost:8080/health

# Test recommendation (with mock service)
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to redecorate my bedroom",
    "image": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
  }'
```

---

## 7. **Development Notes**

### **Service Dependencies:**
- **Mock Mode**: No external dependencies, runs completely offline
- **Full AI Mode**: Requires vector database, AI API keys, and cloud authentication

### **Port Mapping:**
- Shopping Assistant Service: `localhost:8080`
- Frontend: `localhost:8080` (when full stack is running)
- Other services: See docker-compose.yml for complete port mapping

### **Environment Variables:**
```bash
# For GCP full mode
PROJECT_ID=your-project
REGION=us-central1
ALLOYDB_CLUSTER_NAME=your-cluster
ALLOYDB_INSTANCE_NAME=your-instance
ALLOYDB_DATABASE_NAME=boutique
ALLOYDB_TABLE_NAME=products
ALLOYDB_SECRET_NAME=your-password-secret

# For Azure alternative
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
POSTGRES_CONNECTION_STRING=postgresql://user:pass@host:5432/db
```

This setup provides flexibility to run the Shopping Assistant Service across any platform while maintaining the same functionality and API interface.
