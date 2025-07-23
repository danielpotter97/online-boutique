# Azure Deployment Guide: Online Boutique

This guide helps you deploy Online Boutique on Azure using Azure Kubernetes Service (AKS) and Azure native services.

---

## **Prerequisites**

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed and authenticated
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [Helm 3](https://helm.sh/docs/intro/install/) installed
- Docker installed (for local development)
- An Azure subscription with appropriate permissions

---

## **1. Azure Resources Setup**

### **1.1 Create Resource Group**
```bash
export RESOURCE_GROUP="online-boutique-rg"
export LOCATION="eastus"
export CLUSTER_NAME="online-boutique-aks"

az group create --name $RESOURCE_GROUP --location $LOCATION
```

### **1.2 Create Azure Container Registry (ACR)**
```bash
export ACR_NAME="onlineboutiqueacr$(date +%s)"
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --location $LOCATION
```

### **1.3 Create AKS Cluster**
```bash
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count 3 \
  --enable-addons monitoring \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys \
  --location $LOCATION
```

### **1.4 Get AKS Credentials**
```bash
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME
```

### **1.5 Create Azure Cache for Redis**
```bash
export REDIS_NAME="onlineboutique-redis-$(date +%s)"
az redis create \
  --resource-group $RESOURCE_GROUP \
  --name $REDIS_NAME \
  --location $LOCATION \
  --sku Basic \
  --vm-size c0
```

### **1.6 Create Application Insights**
```bash
export APP_INSIGHTS_NAME="onlineboutique-insights"
az monitor app-insights component create \
  --app $APP_INSIGHTS_NAME \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --kind web

# Get the connection string
export APPINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
  --app $APP_INSIGHTS_NAME \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)
```

---

## **2. Build and Push Container Images**

### **2.1 Build and Push All Services**
```bash
# Login to ACR
az acr login --name $ACR_NAME

# Get ACR login server
export ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer -o tsv)

# Build and push each service
services=("adservice" "cartservice/src" "checkoutservice" "currencyservice" "emailservice" "frontend" "loadgenerator" "paymentservice" "productcatalogservice" "recommendationservice" "shippingservice" "shoppingassistantservice")

for service in "${services[@]}"; do
  service_name=$(basename $service)
  echo "Building and pushing $service_name..."
  
  docker build -t $ACR_LOGIN_SERVER/onlineboutique/$service_name:latest src/$service
  docker push $ACR_LOGIN_SERVER/onlineboutique/$service_name:latest
done
```

---

## **3. Deploy to AKS**

### **3.1 Create Kubernetes Secrets**
```bash
kubectl create secret generic azure-config \
  --from-literal=APPLICATIONINSIGHTS_CONNECTION_STRING="$APPINSIGHTS_CONNECTION_STRING"

# Get Redis connection details
export REDIS_HOST=$(az redis show --name $REDIS_NAME --resource-group $RESOURCE_GROUP --query hostName -o tsv)
export REDIS_KEY=$(az redis list-keys --name $REDIS_NAME --resource-group $RESOURCE_GROUP --query primaryKey -o tsv)

kubectl create secret generic redis-config \
  --from-literal=REDIS_ADDR="$REDIS_HOST:6380" \
  --from-literal=REDIS_PASSWORD="$REDIS_KEY"
```

### **3.2 Update Kubernetes Manifests**
Update the Kubernetes manifests in `./kubernetes-manifests/` to:
- Use your ACR images (`$ACR_LOGIN_SERVER/onlineboutique/servicename:latest`)
- Reference the Azure secrets created above
- Configure Azure-specific environment variables

### **3.3 Deploy Services**
```bash
kubectl apply -f ./kubernetes-manifests/
```

### **3.4 Verify Deployment**
```bash
kubectl get pods
kubectl get services
```

---

## **4. Local Development with Azure Services**

### **4.1 Set Environment Variables**
```bash
export APPLICATIONINSIGHTS_CONNECTION_STRING="your-app-insights-connection-string"
export DISABLE_PROFILER=""  # Leave empty to enable Azure Application Insights
```

### **4.2 Run with Docker Compose**
```bash
docker compose up --build
```

---

## **5. Monitoring and Observability**

### **5.1 Application Insights Dashboard**
- Navigate to the Azure portal
- Go to Application Insights → $APP_INSIGHTS_NAME
- Explore metrics, logs, and distributed tracing

### **5.2 AKS Monitoring**
- Use Azure Monitor for containers
- View cluster and pod metrics in the Azure portal

---

## **6. Cleanup**

### **6.1 Delete AKS Resources**
```bash
kubectl delete -f ./kubernetes-manifests/
```

### **6.2 Delete Azure Resources**
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

## **Key Changes from GCP Version**

| **Component** | **GCP** | **Azure** |
|---------------|---------|-----------|
| **Container Registry** | Google Container Registry/Artifact Registry | Azure Container Registry |
| **Kubernetes** | Google Kubernetes Engine (GKE) | Azure Kubernetes Service (AKS) |
| **Monitoring** | Google Cloud Operations (Stackdriver) | Azure Application Insights |
| **Profiling** | Google Cloud Profiler | Azure Application Insights Profiler |
| **Cache/Database** | Memorystore for Redis | Azure Cache for Redis |
| **Service Mesh** | Istio on GKE | Istio on AKS or Azure Service Mesh |

---

## **Environment Variables**

| **Variable** | **Description** |
|--------------|-----------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Azure Application Insights connection string |
| `APPINSIGHTS_INSTRUMENTATIONKEY` | Alternative to connection string (legacy) |
| `DISABLE_PROFILER` | Set to disable Azure Application Insights profiling |
| `ENABLE_TRACING` | Set to "1" to enable distributed tracing |
| `REDIS_ADDR` | Redis connection address with SSL port (6380) |
| `REDIS_PASSWORD` | Redis authentication key |

---

## **Troubleshooting**

### **Common Issues:**
1. **ACR Authentication**: Ensure AKS has permissions to pull from ACR
2. **Redis SSL**: Azure Cache for Redis requires SSL (port 6380)
3. **Application Insights**: Verify connection string is correctly set
4. **Resource Limits**: Ensure AKS nodes have sufficient resources

### **Debug Commands:**
```bash
# Check pod logs
kubectl logs <pod-name>

# Check Application Insights telemetry
az monitor app-insights events show --app $APP_INSIGHTS_NAME --resource-group $RESOURCE_GROUP

# Test Redis connectivity
kubectl run redis-test --image=redis:7 --rm -it -- redis-cli -h $REDIS_HOST -p 6380 -a $REDIS_KEY --tls
```
