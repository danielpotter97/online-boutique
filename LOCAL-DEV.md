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

## 2. **Configure Azure Services (Optional)**

For full observability with Azure Application Insights:

1. **Create Azure Application Insights resource** (if you haven't already):
   ```sh
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name online-boutique-dev --location eastus
   
   # Create Application Insights
   az monitor app-insights component create \
     --app online-boutique-dev \
     --location eastus \
     --resource-group online-boutique-dev \
     --kind web
   
   # Get connection string
   az monitor app-insights component show \
     --app online-boutique-dev \
     --resource-group online-boutique-dev \
     --query connectionString -o tsv
   ```

2. **Configure environment variables**:
   ```sh
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Application Insights connection string
   # APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string-here"
   ```

---

## 3. **Build & Run All Services**

```sh
docker compose up --build
```

This will start all services with Azure Application Insights integration enabled (if configured).
