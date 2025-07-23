# Azure-specific Kubernetes manifests for Online Boutique
# This directory contains Kubernetes manifests updated for Azure native services

## Usage

1. Update the image references in each manifest to point to your Azure Container Registry:
   ```
   image: your-acr-name.azurecr.io/onlineboutique/servicename:latest
   ```

2. Create the necessary secrets:
   ```bash
   kubectl create secret generic azure-config \
     --from-literal=APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string"
   
   kubectl create secret generic redis-config \
     --from-literal=REDIS_ADDR="your-redis-cache.redis.cache.windows.net:6380" \
     --from-literal=REDIS_PASSWORD="your-redis-key"
   ```

3. Apply the manifests:
   ```bash
   kubectl apply -f ./azure-manifests/
   ```

## Key Changes from Original Manifests

- **Image repositories**: Updated to use Azure Container Registry
- **Environment variables**: Added Azure Application Insights configuration
- **Redis configuration**: Updated for Azure Cache for Redis with SSL
- **Secrets**: Uses Kubernetes secrets for sensitive Azure configuration
