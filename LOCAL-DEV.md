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

---

## 8. **Azure Production Deployment**

### **🏗️ Architecture Overview**
```
GitHub Repository → GitHub Actions → Azure Container Registry (ACR)
                                          ↓
Terraform Infrastructure → Azure Kubernetes Service (AKS) ← Helm Charts
                                          ↓
Azure Services: PostgreSQL, OpenAI, Key Vault, Application Insights
```

### **📋 Prerequisites for Azure Deployment**

1. **Azure CLI & Tools**:
   ```bash
   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLI | sudo bash
   
   # Install kubectl
   az aks install-cli
   
   # Install Helm
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

2. **Azure Subscription & Login**:
   ```bash
   az login
   az account set --subscription "your-subscription-id"
   ```

### **🏛️ Terraform Infrastructure Setup**

Create a separate terraform repository with these resources:

**`terraform/main.tf`**:
```hcl
# Resource Group
resource "azurerm_resource_group" "online_boutique" {
  name     = "rg-online-boutique-${var.environment}"
  location = var.location
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "acronlineboutique${var.environment}"
  resource_group_name = azurerm_resource_group.online_boutique.name
  location           = azurerm_resource_group.online_boutique.location
  sku                = "Standard"
  admin_enabled      = true
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-online-boutique-${var.environment}"
  location           = azurerm_resource_group.online_boutique.location
  resource_group_name = azurerm_resource_group.online_boutique.name
  dns_prefix         = "aks-online-boutique-${var.environment}"
  
  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }
  
  identity {
    type = "SystemAssigned"
  }
}

# PostgreSQL for Shopping Assistant (with pgvector)
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                = "psql-online-boutique-${var.environment}"
  resource_group_name = azurerm_resource_group.online_boutique.name
  location           = azurerm_resource_group.online_boutique.location
  
  administrator_login    = "boutique_admin"
  administrator_password = var.postgres_admin_password
  
  sku_name   = "B_Standard_B1ms"
  storage_mb = 32768
  version    = "14"
  
  backup_retention_days = 7
}

# Enable pgvector extension
resource "azurerm_postgresql_flexible_server_configuration" "pgvector" {
  name      = "shared_preload_libraries"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  value     = "vector"
}

# Azure OpenAI Service
resource "azurerm_cognitive_account" "openai" {
  name                = "openai-online-boutique-${var.environment}"
  location           = "East US"  # OpenAI availability
  resource_group_name = azurerm_resource_group.online_boutique.name
  kind               = "OpenAI"
  sku_name           = "S0"
}

# Key Vault for secrets
resource "azurerm_key_vault" "kv" {
  name                = "kv-online-boutique-${var.environment}"
  location           = azurerm_resource_group.online_boutique.location
  resource_group_name = azurerm_resource_group.online_boutique.name
  tenant_id          = data.azurerm_client_config.current.tenant_id
  sku_name           = "standard"
  
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
    
    secret_permissions = ["Get", "List"]
  }
}

# Application Insights
resource "azurerm_application_insights" "appinsights" {
  name                = "ai-online-boutique-${var.environment}"
  location           = azurerm_resource_group.online_boutique.location
  resource_group_name = azurerm_resource_group.online_boutique.name
  application_type   = "web"
}
```

### **🚀 GitHub Actions Workflow**

**`.github/workflows/azure-deploy.yml`**:
```yaml
name: Build and Deploy to Azure

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AZURE_RESOURCE_GROUP: rg-online-boutique-prod
  AKS_CLUSTER_NAME: aks-online-boutique-prod
  ACR_NAME: acronlineboutiqueprod

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - adservice
          - cartservice
          - checkoutservice
          - currencyservice
          - emailservice
          - frontend
          - loadgenerator
          - paymentservice
          - productcatalogservice
          - recommendationservice
          - shippingservice
          - shoppingassistantservice
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Login to ACR
      run: |
        az acr login --name ${{ env.ACR_NAME }}
    
    - name: Build and Push Docker Image
      run: |
        SERVICE=${{ matrix.service }}
        IMAGE_TAG="${{ env.ACR_NAME }}.azurecr.io/$SERVICE:${{ github.sha }}"
        
        # Special handling for services with different Dockerfile locations
        if [ "$SERVICE" = "cartservice" ]; then
          docker build -t $IMAGE_TAG src/cartservice/src/
        elif [ "$SERVICE" = "shoppingassistantservice" ]; then
          # Use mock version for demo, or full version if secrets are configured  
          docker build -t $IMAGE_TAG -f src/shoppingassistantservice/Dockerfile.mock src/shoppingassistantservice/
        else
          docker build -t $IMAGE_TAG src/$SERVICE/
        fi
        
        docker push $IMAGE_TAG
  
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Get AKS credentials
      run: |
        az aks get-credentials --resource-group ${{ env.AZURE_RESOURCE_GROUP }} --name ${{ env.AKS_CLUSTER_NAME }}
    
    - name: Install Helm
      uses: azure/setup-helm@v3
    
    - name: Deploy with Helm
      run: |
        helm upgrade --install online-boutique ./helm-chart \
          --set global.imageRegistry="${{ env.ACR_NAME }}.azurecr.io" \
          --set global.imageTag="${{ github.sha }}" \
          --set shoppingassistantservice.enabled=true \
          --set shoppingassistantservice.azureOpenAI.enabled=true \
          --set global.azure.enabled=true \
          --namespace online-boutique \
          --create-namespace \
          --wait
```

### **🛠️ Helm Chart Modifications for Azure**

**`helm-chart/values-azure.yaml`**:
```yaml
global:
  imageRegistry: "your-acr-name.azurecr.io"
  imageTag: "latest"
  azure:
    enabled: true
    resourceGroup: "rg-online-boutique-prod"
    keyVault: "kv-online-boutique-prod"
    applicationInsights:
      connectionString: "your-connection-string"

# Override shopping assistant for Azure
shoppingassistantservice:
  enabled: true
  image:
    repository: shoppingassistantservice
    tag: latest
  env:
    - name: AZURE_OPENAI_ENDPOINT
      valueFrom:
        secretKeyRef:
          name: azure-openai-secret
          key: endpoint
    - name: AZURE_OPENAI_API_KEY
      valueFrom:
        secretKeyRef:
          name: azure-openai-secret
          key: api-key
    - name: POSTGRES_CONNECTION_STRING
      valueFrom:
        secretKeyRef:
          name: postgres-secret
          key: connection-string

# Redis for cart service (Azure Cache for Redis)
redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: false
```

### **📝 Required GitHub Secrets**

Set these in your GitHub repository secrets:

```bash
# Azure Service Principal (created via: az ad sp create-for-rbac)
AZURE_CREDENTIALS='{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret", 
  "subscriptionId": "your-subscription-id",
  "tenantId": "your-tenant-id"
}'

# Optional: Custom values
ACR_NAME="your-acr-name"
RESOURCE_GROUP="your-resource-group"
AKS_CLUSTER="your-aks-cluster"
```

### **🔧 Service-Specific Azure Adaptations**

**Shopping Assistant Service** (Azure OpenAI version):
```python
# Replace in shoppingassistantservice.py for Azure
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Azure OpenAI setup
llm = ChatOpenAI(
    model="gpt-4-vision-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01"
)

# PostgreSQL with pgvector (instead of AlloyDB)
from langchain_postgres import PGVector
vectorstore = PGVector(
    connection_string=os.environ["POSTGRES_CONNECTION_STRING"],
    embedding_function=OpenAIEmbeddings()
)
```

### **🚀 Deployment Commands**

```bash
# 1. Deploy infrastructure with Terraform
cd terraform/
terraform init
terraform plan -var="environment=prod"
terraform apply

# 2. Configure kubectl for AKS
az aks get-credentials --resource-group rg-online-boutique-prod --name aks-online-boutique-prod

# 3. Deploy application with Helm
helm upgrade --install online-boutique ./helm-chart \
  --values helm-chart/values-azure.yaml \
  --namespace online-boutique \
  --create-namespace

# 4. Get external IP
kubectl get services -n online-boutique
```

### **📊 Monitoring & Observability**

```yaml
# Add to helm-chart/values-azure.yaml
monitoring:
  applicationInsights:
    enabled: true
    connectionString: "your-app-insights-connection-string"
  
  prometheus:
    enabled: true
  
  grafana:
    enabled: true
```

This setup gives you:
- ✅ **CI/CD Pipeline**: Automated builds and deployments
- ✅ **Infrastructure as Code**: Terraform for reproducible infrastructure  
- ✅ **Container Registry**: Secure image storage in ACR
- ✅ **Kubernetes**: Scalable container orchestration with AKS
- ✅ **AI Services**: Azure OpenAI for shopping assistant
- ✅ **Monitoring**: Application Insights integration
- ✅ **Security**: Azure Key Vault for secrets management
