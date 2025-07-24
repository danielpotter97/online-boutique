# Platform-Independent Deployment Guide

The Online Boutique microservices have been made completely **platform-independent** and can run on **any cloud provider** (GCP, Azure, AWS) or **on-premises** infrastructure.

## 🎯 Key Changes for Platform Independence

### Removed Cloud-Specific Dependencies

#### Google Cloud Dependencies Removed:
- ❌ `cloud.google.com/go/profiler` - Google Cloud Profiler
- ❌ `cloud.google.com/go/compute/metadata` - GCP metadata service
- ❌ `@google-cloud/profiler` - Node.js Google Cloud Profiler
- ❌ `google-cloud-profiler` - Python Google Cloud Profiler
- ❌ GCP-specific metadata detection
- ❌ Stackdriver profiler initialization

#### Replaced With:
- ✅ **Platform-agnostic OpenTelemetry** distributed tracing
- ✅ **Jaeger** for observability (runs anywhere)
- ✅ **Environment variables** for deployment configuration
- ✅ **Docker Compose** orchestration (cloud-agnostic)

## 🌐 Deployment Flexibility

### Supported Platforms:
- **Google Cloud Platform (GCP)** - Kubernetes, Cloud Run
- **Amazon Web Services (AWS)** - EKS, ECS, EC2
- **Microsoft Azure** - AKS, Container Instances, VMs
- **On-Premises** - Kubernetes, Docker Swarm, bare metal
- **Local Development** - Docker Compose

## 🔧 Environment Variables for Platform Independence

### Core Configuration:
```bash
# Platform Detection (optional)
ENV_PLATFORM=local|gcp|aws|azure|onprem

# Deployment Information (replaces GCP metadata)
CLUSTER_NAME=your-cluster-name
DEPLOYMENT_ZONE=your-deployment-zone

# Observability
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
COLLECTOR_SERVICE_ADDR=jaeger:4317
ENABLE_TRACING=1
DISABLE_PROFILER=1  # Platform-independent profiling disabled by default

# Service Discovery
PRODUCT_CATALOG_SERVICE_ADDR=productcatalogservice:3550
CURRENCY_SERVICE_ADDR=currencyservice:7000
CART_SERVICE_ADDR=cartservice:7070
RECOMMENDATION_SERVICE_ADDR=recommendationservice:8080
SHIPPING_SERVICE_ADDR=shippingservice:50051
CHECKOUT_SERVICE_ADDR=checkoutservice:5050
AD_SERVICE_ADDR=adservice:9555
EMAIL_SERVICE_ADDR=emailservice:8080
PAYMENT_SERVICE_ADDR=paymentservice:50051
```

### Platform-Specific Examples:

#### AWS EKS:
```bash
ENV_PLATFORM=aws
CLUSTER_NAME=online-boutique-eks
DEPLOYMENT_ZONE=us-west-2a
```

#### Azure AKS:
```bash
ENV_PLATFORM=azure
CLUSTER_NAME=online-boutique-aks
DEPLOYMENT_ZONE=eastus-1
```

#### GCP GKE:
```bash
ENV_PLATFORM=gcp
CLUSTER_NAME=online-boutique-gke
DEPLOYMENT_ZONE=us-central1-a
```

#### On-Premises:
```bash
ENV_PLATFORM=onprem
CLUSTER_NAME=datacenter-k8s
DEPLOYMENT_ZONE=datacenter-rack-1
```

## 🚀 Quick Start for Any Platform

### 1. Docker Compose (Universal):
```bash
git clone <repo>
cd online-boutique
docker-compose up -d
```

### 2. Kubernetes (Any Cloud):
```bash
kubectl apply -f kubernetes-manifests/
```

### 3. Helm Chart (Any Cloud):
```bash
helm install online-boutique ./helm-chart
```

## 📊 Observability Stack

### Jaeger Distributed Tracing:
- **UI**: http://localhost:16686
- **Collector**: http://localhost:14268
- **Works everywhere**: No cloud vendor lock-in

### Service Mesh Compatible:
- **Istio** (any cloud)
- **Linkerd** (any cloud)
- **Consul Connect** (any platform)

## 🔄 Migration Path

### From GCP-Native:
1. Remove `cloud.google.com` dependencies
2. Set environment variables instead of metadata queries
3. Use Jaeger instead of Stackdriver
4. Deploy anywhere

### From Azure-Native:
1. Remove Azure Application Insights dependencies
2. Switch to OpenTelemetry + Jaeger
3. Use environment variables for configuration
4. Deploy anywhere

### From AWS-Native:
1. Remove AWS X-Ray dependencies
2. Switch to OpenTelemetry + Jaeger
3. Use standard service discovery
4. Deploy anywhere

## 🎖️ Benefits of Platform Independence

### Business Benefits:
- ✅ **No vendor lock-in**
- ✅ **Multi-cloud strategy support**
- ✅ **Cost optimization flexibility**
- ✅ **Disaster recovery across clouds**

### Technical Benefits:
- ✅ **Consistent development/production**
- ✅ **Easier testing on local machines**
- ✅ **Simplified CI/CD pipelines**
- ✅ **Standard observability stack**

### Operational Benefits:
- ✅ **Same tools across all environments**
- ✅ **Reduced learning curve**
- ✅ **Unified monitoring and alerting**
- ✅ **Simplified troubleshooting**

## 🏗️ Architecture Principles

### Cloud-Native Patterns:
- **12-Factor App compliance**
- **Containerized microservices**
- **Service discovery via environment variables**
- **Stateless application design**
- **External configuration management**

### Observability Standards:
- **OpenTelemetry for tracing**
- **Prometheus metrics (compatible)**
- **Structured JSON logging**
- **Health check endpoints**

## 🎯 Next Steps

1. **Choose your deployment platform**
2. **Set appropriate environment variables**
3. **Deploy using your preferred method**
4. **Access Jaeger UI for observability**
5. **Scale and monitor as needed**

The Online Boutique is now **truly portable** and can run anywhere Docker containers are supported! 🎉
