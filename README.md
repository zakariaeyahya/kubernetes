

# Kubernetes Project

---

## 📜 Content
1. **What is Kubernetes?**  
   Introduction to Kubernetes, an open-source platform for automating the deployment, scaling, and operation of containerized applications.

2. **Why Kubernetes?**  
   Key benefits of Kubernetes:  
   - Automation and resource optimization.  
   - Scalability and portability.  
   - High availability and security.  
   - Rich ecosystem.

3. **Key Concepts of Kubernetes**  
   - **Pods**: The smallest deployment unit containing one or more containers.  
   - **Services**: Define a logical set of Pods and access policies.  
   - **Deployments**: Manage deployment and updates of Pods.  
   - **ReplicaSets**: Ensure a specified number of Pods are running.  
   - **Namespaces**: Organize resources within a cluster into logical groups.  
   - **ConfigMaps and Secrets**: Manage configurations and sensitive data.

4. **Kubernetes Architecture**  
   Overview of the underlying architecture and core components of Kubernetes.
   ![Uploading image.png…]()


6. **Practical Demonstration**  
   - **Environment Setup and Docker**: Build and pull Docker images for the backend and frontend.  
   - **Minikube Setup and Configuration**:  
     - Create and deploy in a new namespace.  
   - **Service Verification and Access**:  
     - Check running Pods.  
     - Access Pod logs via Minikube.

---

## 🛠️ Prerequisites
- **Docker**: To create and manage containers.  
- **Minikube**: To run Kubernetes locally.  
- **Python**: Ensure Python and `pip` are installed to handle requirements.

---

## 🚀 Quick Start

### 1. Set Up Docker Images
- Navigate to the backend folder and frontend folder to install dependencies and build Docker images:

#### Backend:
```bash
cd backend
pip install -r requirements.txt
docker build -t backend-image .
```

#### Frontend:
```bash
cd frontend
pip install -r requirements.txt
docker build -t frontend-image .
```

### 2. Start Minikube
- Initialize Minikube:
```bash
minikube start
```

- Configure Docker to use Minikube:
```bash
eval $(minikube docker-env)
```

### 3. Deploy on Kubernetes
- Apply the deployment and service YAML files for the backend and frontend:
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
```

- Optionally, create and deploy in a separate namespace:
```bash
kubectl create namespace my-namespace
kubectl apply -n my-namespace -f backend-deployment.yaml
kubectl apply -n my-namespace -f frontend-deployment.yaml
```

### 4. Verify Deployment
- Check running Pods:
```bash
kubectl get pods
```

- Check service availability:
```bash
kubectl get services
```

- Access Pod logs:
```bash
kubectl logs <pod-name>
```

- Open services in Minikube:
```bash
minikube service backend-service
minikube service frontend-service
```

---

## 🎯 Objectives
- Understand the core concepts of Kubernetes.  
- Implement a practical deployment of a containerized application.  
- Explore Kubernetes architecture and advanced features.

---
