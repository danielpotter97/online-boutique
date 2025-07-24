# 🚨 **IMPORTANT LEGAL DISCLAIMER** 🚨

## **THIS IS A LEGITIMATE FORK - NOT STOLEN CODE**

> ### 📢 **ORIGINAL PROJECT ATTRIBUTION**
> This project is a **LEGITIMATE FORK** of the original Google Cloud Platform microservices demo, available at:  
> **Original Repository:** https://github.com/GoogleCloudPlatform/microservices-demo  
> **Original Copyright:** © Google LLC - Licensed under Apache License 2.0
>
> ### ✅ **LEGAL COMPLIANCE**
> - ✅ **Apache 2.0 License**: This fork complies with all Apache 2.0 license requirements
> - ✅ **Attribution Preserved**: All original copyright notices maintained  
> - ✅ **Derivative Work**: This is a legal derivative work under Apache 2.0 terms
> - ✅ **Open Source**: All modifications are open source and clearly documented
> - ✅ **No Copyright Infringement**: This fork follows proper open source practices
>
> ### 🎯 **FORK PURPOSE**
> This fork **enhances** the original project by making it **platform-independent** while preserving full attribution to Google LLC.

---

![Continuous Integration](https://github.com/GoogleCloudPlatform/microservices-demo/workflows/Continuous%20Integration%20-%20Main/Release/badge.svg)

**Online Boutique** is a **platform-independent** microservices demo application. The application is a web-based e-commerce app where users can browse items, add them to the cart, and purchase them.

This version demonstrates modern microservices architecture with **complete platform independence** - runs on **any cloud** (GCP, AWS, Azure) or **on-premises**. Features [Jaeger](https://www.jaegertracing.io/) for distributed tracing, [gRPC](https://grpc.io/) for inter-service communication, and containerized deployment with Docker Compose.

**🎯 Key Features:**
- 🌐 **Platform Independent**: Deploy on GCP, AWS, Azure, or on-premises
- 🔍 **Open Source Observability**: Jaeger distributed tracing (no vendor lock-in)
- 🏗️ **13 Microservices**: Multi-language architecture (Go, Python, Node.js, Java, C#)
- 🚀 **Production Ready**: Real-world patterns, health checks, and monitoring
- 🐳 **Container Native**: Docker & Kubernetes ready
- 📊 **Full Observability**: OpenTelemetry integration with Jaeger UI

If you're using this demo, please **★Star** this repository to show your interest!

## Architecture

**Online Boutique** is composed of 11 microservices written in different
languages that talk to each other over gRPC.

[![Architecture of
microservices](/docs/img/architecture-diagram.png)](/docs/img/architecture-diagram.png)

Find **Protocol Buffers Descriptions** at the [`./protos` directory](/protos).

| Service                                              | Language      | Description                                                                                                                       |
| ---------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [frontend](/src/frontend)                           | Go            | Exposes an HTTP server to serve the website. Does not require signup/login and generates session IDs for all users automatically. |
| [cartservice](/src/cartservice)                     | C#            | Stores the items in the user's shopping cart in Redis and retrieves it.                                                           |
| [productcatalogservice](/src/productcatalogservice) | Go            | Provides the list of products from a JSON file and ability to search products and get individual products.                        |
| [currencyservice](/src/currencyservice)             | Node.js       | Converts one money amount to another currency. Uses real values fetched from European Central Bank. It's the highest QPS service. |
| [paymentservice](/src/paymentservice)               | Node.js       | Charges the given credit card info (mock) with the given amount and returns a transaction ID.                                     |
| [shippingservice](/src/shippingservice)             | Go            | Gives shipping cost estimates based on the shopping cart. Ships items to the given address (mock)                                 |
| [emailservice](/src/emailservice)                   | Python        | Sends users an order confirmation email (mock).                                                                                   |
| [checkoutservice](/src/checkoutservice)             | Go            | Retrieves user cart, prepares order and orchestrates the payment, shipping and the email notification.                            |
| [recommendationservice](/src/recommendationservice) | Python        | Recommends other products based on what's given in the cart.                                                                      |
| [adservice](/src/adservice)                         | Java          | Provides text ads based on given context words.                                                                                   |
| [loadgenerator](/src/loadgenerator)                 | Python/Locust | Continuously sends requests imitating realistic user shopping flows to the frontend.                                              |

## Screenshots

| Home Page                                                                                                         | Checkout Screen                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [![Screenshot of store homepage](/docs/img/online-boutique-frontend-1.png)](/docs/img/online-boutique-frontend-1.png) | [![Screenshot of checkout screen](/docs/img/online-boutique-frontend-2.png)](/docs/img/online-boutique-frontend-2.png) |

## Quickstart (Azure AKS)

1. Ensure you have the following requirements:
   - [Azure subscription](https://azure.microsoft.com/en-us/free/).
   - Shell environment with `az`, `git`, and `kubectl`.

2. Clone this repository:
   ```sh
   git clone https://github.com/danielpotter97/online-boutique.git
   cd online-boutique/
   ```

3. **🚀 Quick Start with Open Source Observability (Recommended)**:
   ```sh
   # Start with Jaeger distributed tracing (no cloud setup needed!)
   ./start-local.sh
   ```
   
   **Access Points:**
   - 🛍️ **Online Boutique**: http://localhost:8080
   - 📊 **Jaeger Tracing UI**: http://localhost:16686
   
   This gives you the full experience with zero configuration!

4. **Alternative: Azure Deployment**
## 🌐 Platform Independence

**Online Boutique is now completely platform-independent!** Deploy anywhere:

### Supported Platforms:
- **☁️ Google Cloud Platform** - GKE, Cloud Run, Compute Engine
- **☁️ Amazon Web Services** - EKS, ECS, EC2
- **☁️ Microsoft Azure** - AKS, Container Instances, Virtual Machines  
- **🏢 On-Premises** - Kubernetes, Docker Swarm, bare metal
- **💻 Local Development** - Docker Compose

### Quick Platform Deployment:

#### Any Cloud with Kubernetes:
```bash
kubectl apply -f kubernetes-manifests/
```

#### Docker Compose (Universal):
```bash
docker-compose up -d
```

#### Helm Chart (Any Kubernetes):
```bash
helm install online-boutique ./helm-chart
```

See the **[Platform-Independent Guide](./PLATFORM-INDEPENDENT-GUIDE.md)** for detailed deployment instructions.

   Follow the [Azure Deployment Guide](./AZURE-DEPLOYMENT.md) for cloud deployment with Azure Application Insights.

5. **Manual Docker Compose** (if you prefer):
   ```sh
   docker-compose up --build
   ```

## Platform-Independent Kubernetes Deployment

> 💡 **Recommended**: This application is now platform-independent and can be deployed on any Kubernetes cluster (GCP GKE, AWS EKS, Azure AKS, or on-premises).

1. Ensure you have the following requirements:
   - A Kubernetes cluster on your preferred platform
   - `kubectl` configured to connect to your cluster
   - `git` for cloning the repository

2. Clone the repository:

   ```sh
   git clone https://github.com/your-org/microservices-demo.git
   cd microservices-demo/
   ```

3. Deploy Online Boutique to your cluster:

   ```sh
   kubectl apply -f ./kubernetes-manifests
   ```

4. Wait for the pods to be ready:

   ```sh
   kubectl get pods
   ```

5. Access the web frontend in a browser using the frontend's external IP:

   ```sh
   kubectl get service frontend-external | awk '{print $4}'
   ```

   **Note**: If using a local cluster (minikube, kind), you may need to use port-forwarding:
   ```sh
   kubectl port-forward deployment/frontend 8080:8080
   ```
   Then visit http://localhost:8080

6. **[Optional]** Clean up:

   ```sh
   kubectl delete -f ./kubernetes-manifests
   ```

## Original GKE Quickstart (Legacy)

> ⚠️ **Note**: The instructions below are for the original GCP-specific version. For platform independence, use the deployment guide above.

<details>
<summary>Click to expand GKE-specific instructions</summary>

1. Ensure you have the following requirements:
   - [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).
   - Shell environment with `gcloud`, `git`, and `kubectl`.

2. Set the Google Cloud project and region and ensure the Google Kubernetes Engine API is enabled.

   ```sh
   export PROJECT_ID=<PROJECT_ID>
   export REGION=us-central1
   gcloud services enable container.googleapis.com \
   kubectl apply -f ./release/kubernetes-manifests.yaml
   ```

5. Wait for the pods to be ready.

   ```sh
   kubectl get pods
   ```

   After a few minutes, you should see the Pods in a `Running` state:

   ```
   NAME                                     READY   STATUS    RESTARTS   AGE
   adservice-76bdd69666-ckc5j               1/1     Running   0          2m58s
   cartservice-66d497c6b7-dp5jr             1/1     Running   0          2m59s
   checkoutservice-666c784bd6-4jd22         1/1     Running   0          3m1s
   currencyservice-5d5d496984-4jmd7         1/1     Running   0          2m59s
   emailservice-667457d9d6-75jcq            1/1     Running   0          3m2s
   frontend-6b8d69b9fb-wjqdg                1/1     Running   0          3m1s
   loadgenerator-665b5cd444-gwqdq           1/1     Running   0          3m
   paymentservice-68596d6dd6-bf6bv          1/1     Running   0          3m
   productcatalogservice-557d474574-888kr   1/1     Running   0          3m
   recommendationservice-69c56b74d4-7z8r5   1/1     Running   0          3m1s
   redis-cart-5f59546cdd-5jnqf              1/1     Running   0          2m58s
   shippingservice-6ccc89f8fd-v686r         1/1     Running   0          2m58s
   ```

7. Access the web frontend in a browser using the frontend's external IP.

   ```sh
   kubectl get service frontend-external | awk '{print $4}'
   ```

   Visit `http://EXTERNAL_IP` in a web browser to access your instance of Online Boutique.

6. Congrats! You've deployed the platform-independent Online Boutique. To deploy with additional features (e.g., observability, service mesh, etc.), see [Deploy Online Boutique variations with Kustomize](#deploy-online-boutique-variations-with-kustomize).

7. Once you are done with it, clean up the deployment.

   ```sh
   kubectl delete -f ./release/kubernetes-manifests.yaml
   ```

</details>

## Additional deployment options

- **Terraform**: [See these instructions](/terraform) to learn how to deploy Online Boutique using [Terraform](https://www.terraform.io/intro) on any cloud platform.
- **Istio / Service Mesh**: [See these instructions](/kustomize/components/service-mesh-istio/README.md) to deploy Online Boutique alongside an Istio-backed service mesh (platform-independent).
- **Local clusters (Minikube, Kind, etc)**: See the [Development guide](/docs/development-guide.md) to learn how you can deploy Online Boutique on local clusters.
- **AI assistant**: [See these instructions](/kustomize/components/shopping-assistant/README.md) to deploy an AI-powered assistant that suggests products to purchase based on an image.
- **And more**: The [`/kustomize` directory](/kustomize) contains instructions for customizing the deployment of Online Boutique with other variations.

## Documentation

- [Development](/docs/development-guide.md) to learn how to run and develop this app locally.

## Demos featuring Online Boutique

- [Platform Engineering in action: Deploy the Online Boutique sample apps with Score and Humanitec](https://medium.com/p/d99101001e69)
- [The new Kubernetes Gateway API with Istio and Anthos Service Mesh (ASM)](https://medium.com/p/9d64c7009cd)
- [Use Azure Redis Cache with the Online Boutique sample on AKS](https://medium.com/p/981bd98b53f8)

---

## 📜 **LEGAL & LICENSE INFORMATION**

### **Original Project Attribution**
- **Original Work:** [GoogleCloudPlatform/microservices-demo](https://github.com/GoogleCloudPlatform/microservices-demo)
- **Original Copyright:** © 2018-2024 Google LLC
- **Original License:** Apache License 2.0

### **Fork Information** 
- **This Repository:** Platform-independent fork with cloud-agnostic enhancements
- **Fork License:** Apache License 2.0 (inherited from original)
- **Fork Purpose:** Educational and demonstration of platform-independent microservices architecture
- **Compliance:** All original copyright notices preserved, full Apache 2.0 compliance

### **No Copyright Infringement**
This is a **legitimate derivative work** under Apache License 2.0 terms. All code modifications are properly attributed and licensed. This fork enhances the original project while maintaining full legal compliance and proper attribution to Google LLC.

**📄 License:** See [LICENSE](LICENSE) file for complete Apache 2.0 license terms.
- [Sail Sharp, 8 tips to optimize and secure your .NET containers for Kubernetes](https://medium.com/p/c68ba253844a)
- [Deploy multi-region application with Anthos and Google cloud Spanner](https://medium.com/google-cloud/a2ea3493ed0)
- [Use Google Cloud Memorystore (Redis) with the Online Boutique sample on GKE](https://medium.com/p/82f7879a900d)
- [Use Helm to simplify the deployment of Online Boutique, with a Service Mesh, GitOps, and more!](https://medium.com/p/246119e46d53)
- [How to reduce microservices complexity with Apigee and Anthos Service Mesh](https://cloud.google.com/blog/products/application-modernization/api-management-and-service-mesh-go-together)
- [Platform Engineering in action: Deploy the Online Boutique sample apps with Score and Humanitec](https://medium.com/p/d99101001e69)
- [The new Kubernetes Gateway API with Istio and Anthos Service Mesh (ASM)](https://medium.com/p/9d64c7009cd)
- [Use Azure Redis Cache with the Online Boutique sample on AKS](https://medium.com/p/981bd98b53f8)
- [Sail Sharp, 8 tips to optimize and secure your .NET containers for Kubernetes](https://medium.com/p/c68ba253844a)
- [Use Helm to simplify the deployment of Online Boutique, with a Service Mesh, GitOps, and more!](https://medium.com/p/246119e46d53)
- [gRPC health probes with Kubernetes 1.24+](https://medium.com/p/b5bd26253a4c)
- [KubeCon EU 2019 - Reinventing Networking: A Deep Dive into Istio's Multicluster Gateways - Steve Dake, Independent](https://youtu.be/-t2BfT59zJA?t=982)
