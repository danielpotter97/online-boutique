# Development Guide 

This doc explains how to build and run the Online Boutique source code locally using the `skaffold` command-line tool.  

## Prerequisites

- [Docker for Desktop](https://www.docker.com/products/docker-desktop)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) 
- [skaffold **2.0.2+**](https://skaffold.dev/docs/install/) (latest version recommended), a tool that builds and deploys Docker images in bulk. 
- Clone the repository.
    ```sh
    git clone https://github.com/your-org/microservices-demo
    cd microservices-demo/
    ```
- A Kubernetes cluster (cloud-based or local)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (optional for local cluster)
- [Kind](https://kind.sigs.k8s.io/) (optional for local cluster)

## Option 1: Cloud Kubernetes (Multi-Platform)

> 💡 Recommended if you're using any cloud provider (GCP, AWS, Azure) and want to try it on
> a realistic cluster. **Note**: Configure your cloud provider's container registry accordingly.

1.  Create a Kubernetes cluster on your preferred cloud platform and make sure `kubectl` is pointing
    to the cluster.

    ```sh
    # For GCP (if using Google Cloud)
    gcloud services enable container.googleapis.com
    
    # For AWS (if using Amazon EKS)
    # aws eks update-kubeconfig --region region-code --name cluster_name
    
    # For Azure (if using Azure AKS) 
    # az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
    ```

    ```sh
    # Example for GCP (replace with your cloud provider's commands)
    gcloud container clusters create-auto demo --region=us-central1
    
    # For AWS EKS:
    # eksctl create cluster --name demo --region us-west-2
    
    # For Azure AKS:
    # az aks create --resource-group myResourceGroup --name demo --node-count 3
    ```

    ```
    kubectl get nodes
    ```

2.  Enable container registry on your cloud platform and configure the
    `docker` CLI to authenticate:

    ```sh
    # For GCP Artifact Registry:
    gcloud services enable artifactregistry.googleapis.com
    gcloud artifacts repositories create microservices-demo \
      --repository-format=docker \
      --location=us \
    gcloud auth configure-docker -q
    
    # For AWS ECR:
    # aws ecr create-repository --repository-name microservices-demo
    # aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-west-2.amazonaws.com
    
    # For Azure ACR:
    # az acr create --resource-group myResourceGroup --name myregistry --sku Basic
    # az acr login --name myregistry
    ```

3.  In the root of this repository, run `skaffold run --default-repo=YOUR_REGISTRY`,
    where YOUR_REGISTRY is your container registry URL:

    ```sh
    # For GCP: --default-repo=us-docker.pkg.dev/[PROJECT_ID]/microservices-demo
    # For AWS: --default-repo=[ACCOUNT].dkr.ecr.us-west-2.amazonaws.com/microservices-demo  
    # For Azure: --default-repo=myregistry.azurecr.io/microservices-demo
    ```

    This command:

    - builds the container images
    - pushes them to your container registry
    - applies the `./kubernetes-manifests` deploying the application to
      Kubernetes.

    **Troubleshooting:** If you get "No space left on device" error, you can build the images using cloud build services:
    
    - **GCP**: [Enable the Cloud Build API](https://console.cloud.google.com/flows/enableapi?apiid=cloudbuild.googleapis.com), then run `skaffold run -p gcb --default-repo=us-docker.pkg.dev/[PROJECT_ID]/microservices-demo`
    - **AWS**: Use CodeBuild for large image builds
    - **Azure**: Use Azure Container Registry Build tasks for efficient building

4.  Find the IP address of your application, then visit the application on your
    browser to confirm installation.

        kubectl get service frontend-external

5.  Navigate to `http://EXTERNAL-IP` to access the web frontend.

## Option 2 - Local Cluster 

1. Launch a local Kubernetes cluster with one of the following tools:

    - To launch **Minikube** (tested with Ubuntu Linux). Please, ensure that the
       local Kubernetes cluster has at least:
        - 4 CPUs
        - 4.0 GiB memory
        - 32 GB disk space

      ```shell
      minikube start --cpus=4 --memory 4096 --disk-size 32g
      ```

    - To launch **Docker for Desktop** (tested with Mac/Windows). Go to Preferences:
        - choose “Enable Kubernetes”,
        - set CPUs to at least 3, and Memory to at least 6.0 GiB
        - on the "Disk" tab, set at least 32 GB disk space

    - To launch a **Kind** cluster:

      ```shell
      kind create cluster
      ```

2. Run `kubectl get nodes` to verify you're connected to the respective control plane.

3. Run `skaffold run` (first time will be slow, it can take ~20 minutes).
   This will build and deploy the application. If you need to rebuild the images
   automatically as you refactor the code, run `skaffold dev` command.

4. Run `kubectl get pods` to verify the Pods are ready and running.

5. Run `kubectl port-forward deployment/frontend 8080:8080` to forward a port to the frontend service.

6. Navigate to `localhost:8080` to access the web frontend.


## Cleanup

If you've deployed the application with `skaffold run` command, you can run
`skaffold delete` to clean up the deployed resources.
