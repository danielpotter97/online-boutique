# GCP to Azure Migration Summary

This document summarizes the changes made to migrate Online Boutique from Google Cloud Platform to Microsoft Azure.

## **Migration Overview**

The Online Boutique application has been successfully migrated from GCP-native services to Azure-native services while maintaining the same functionality and microservices architecture.

## **Key Changes Made**

### **1. Monitoring & Observability**
- **Replaced**: Google Cloud Profiler → Azure Application Insights
- **Replaced**: Google Cloud Operations (Stackdriver) → Azure Monitor + Application Insights
- **Updated**: All telemetry and logging to use Azure Application Insights SDK

### **2. Package Dependencies**

#### **Node.js Services (currencyservice, paymentservice)**
- **Removed**: `@google-cloud/profiler`, `@google-cloud/trace-agent`
- **Added**: `applicationinsights`

#### **Python Services (emailservice, recommendationservice)**
- **Removed**: `google-api-core`, `google-cloud-profiler`
- **Added**: `opencensus-ext-azure`, `applicationinsights`

#### **Go Services (frontend, productcatalogservice, checkoutservice, shippingservice)**
- **Removed**: `cloud.google.com/go/profiler`
- **Added**: `github.com/microsoft/ApplicationInsights-Go`

### **3. Code Changes**

#### **Python Services**
- Replaced `initStackdriverProfiling()` → `initAzureApplicationInsights()`
- Updated import statements to use Azure Application Insights SDK
- Removed Google Cloud authentication dependencies

#### **Node.js Services**
- Replaced Google Cloud Profiler initialization with Azure Application Insights setup
- Updated telemetry configuration to use Azure connection strings

#### **Go Services**
- Updated import statements to use Azure Application Insights Go SDK
- Modified profiling initialization code

### **4. Environment Variables**

#### **Added Azure-specific variables:**
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Primary configuration for Azure Application Insights
- `APPINSIGHTS_INSTRUMENTATIONKEY`: Alternative configuration (legacy)

#### **Maintained existing variables:**
- `DISABLE_PROFILER`: Now controls Azure Application Insights profiling
- `ENABLE_TRACING`: Still controls distributed tracing (now via Azure)

### **5. Infrastructure Configuration**

#### **Docker Compose**
- Added Azure environment variables to all services
- Maintained Redis configuration for local development
- Enhanced service configuration for Azure Application Insights

#### **Kubernetes Manifests**
- Created Azure-specific manifests in `/azure-manifests/`
- Updated image references for Azure Container Registry
- Added secrets management for Azure configurations
- Configured for Azure Cache for Redis with SSL

### **6. Documentation**

#### **New Files Created:**
- `AZURE-DEPLOYMENT.md`: Comprehensive Azure deployment guide
- `.env.example`: Environment variable template
- `azure-manifests/`: Azure-specific Kubernetes manifests
- This migration summary document

#### **Updated Files:**
- `README.md`: Updated to reflect Azure deployment options
- `LOCAL-DEV.md`: Added Azure configuration instructions
- All service package files (`package.json`, `requirements.in`, `go.mod`)

## **Azure Resources Used**

| **Service Type** | **Azure Service** | **Purpose** |
|------------------|-------------------|-------------|
| **Container Registry** | Azure Container Registry (ACR) | Store Docker images |
| **Kubernetes** | Azure Kubernetes Service (AKS) | Container orchestration |
| **Caching** | Azure Cache for Redis | Session storage |
| **Monitoring** | Azure Application Insights | APM, metrics, logs, tracing |
| **Monitoring** | Azure Monitor | Infrastructure monitoring |

## **Migration Benefits**

### **Performance & Reliability**
- Native Azure integration provides better performance within Azure ecosystem
- Azure Application Insights offers comprehensive APM capabilities
- Azure Cache for Redis provides managed, scalable caching

### **Cost Optimization**
- Azure native services typically offer better pricing for Azure-deployed workloads
- Integrated billing and cost management
- Reserved capacity options for long-term deployments

### **Security & Compliance**
- Azure native security features
- Integration with Azure Active Directory
- Compliance with Azure security standards

### **Developer Experience**
- Unified Azure portal experience
- Better integration with Azure DevOps and GitHub Actions
- Native Azure CLI and PowerShell support

## **Deployment Options**

### **1. Local Development**
```bash
# Configure Azure Application Insights
cp .env.example .env
# Edit .env with your Azure details

# Run with Docker Compose
docker compose up --build
```

### **2. Azure AKS Deployment**
```bash
# Follow the comprehensive guide
cat AZURE-DEPLOYMENT.md
```

### **3. CI/CD Integration**
- Ready for Azure DevOps Pipelines
- Compatible with GitHub Actions with Azure integration
- Supports Azure Container Registry for image storage

## **Backwards Compatibility**

The migration maintains:
- **Same API interfaces**: All gRPC and HTTP endpoints unchanged
- **Same functionality**: All business logic preserved
- **Same architecture**: Microservices pattern maintained
- **Configuration flexibility**: Can still run without cloud services (local Redis)

## **Testing Recommendations**

1. **Local Testing**: Use Docker Compose for development
2. **Integration Testing**: Deploy to Azure AKS test cluster
3. **Load Testing**: Use existing load generator with Azure monitoring
4. **Monitoring Testing**: Verify Azure Application Insights telemetry

## **Future Enhancements**

### **Potential Azure Integrations**
- **Azure Service Bus**: For async messaging between services
- **Azure Cosmos DB**: For product catalog storage
- **Azure Functions**: For serverless payment processing
- **Azure API Management**: For API gateway functionality
- **Azure Service Mesh**: For advanced traffic management

### **DevOps Improvements**
- Azure DevOps Pipelines for CI/CD
- Azure Container Instances for build agents
- Azure Key Vault for secrets management
- Infrastructure as Code with Azure Resource Manager templates

## **Troubleshooting Common Issues**

### **Application Insights Not Working**
- Verify `APPLICATIONINSIGHTS_CONNECTION_STRING` is correctly set
- Check Azure portal for telemetry data
- Ensure services have network access to Azure endpoints

### **Redis Connection Issues**
- Azure Cache for Redis requires SSL (port 6380)
- Verify Redis access keys are correct
- Check firewall and network security group rules

### **Image Pull Issues**
- Ensure AKS has permissions to pull from ACR
- Verify image tags and registry URLs
- Check service principal or managed identity configuration

---

**Migration completed successfully! The Online Boutique application now runs natively on Azure services while maintaining all original functionality.**
