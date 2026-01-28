# Microservices DevOps Assignment

A production-grade Kubernetes deployment of a 3-tier Python microservices architecture, featuring optimized multi-stage builds, automated scaling, and centralized monitoring.

## Local Setup Instructions

### Prerequisites
- Minikube installed and running
- kubectl configured
- Docker Desktop

### Deployment Steps
1. **Prepare the Environment:**

   minikube start
   minikube addons enable metrics-server
   kubectl create namespace staging

### Apply Manifests 
kubectl apply -f k8s/1-service-accounts.yaml
kubectl apply -f k8s/1-setup.yaml
kubectl apply -f k8s/2-deployment.yaml
kubectl apply -f k8s/3-networking.yaml
kubectl apply -f k8s/4-configmap.yaml
kubectl apply -f k8s/4-prometheus.yaml

### Access the Application:
kubectl port-forward svc/api-gateway 8080:80 -n staging
Visit http://localhost:8080 to view the Gateway Dashboard.

### Health Check Design
The system implements a multi-layered health check strategy:

Liveness Probes: Each service exposes a /health endpoint. Kubernetes monitors this to automatically restart containers if the Python process freezes or enters a deadlock.

Readiness Probes: Ensures traffic is only routed to pods once the internal Flask server and OpenTelemetry instrumentation are fully initialized.

### Key Infrastructure Choices
1. Docker Multi-Stage Builds (Optimization)
Choice: Utilized a builder stage to compile C++ dependencies for OpenTelemetry, then copied artifacts to a python:3.9-slim base. 
Result: Reduced image size by 88% (from 1.1GB to 130MB), significantly improving deployment speed and reducing storage costs.

2. Least Privilege RBAC
Choice: Created dedicated Service Accounts (gateway-sa, orders-sa, inventory-sa) for each microservice. 
Result: Follows the security principle of "Least Privilege," ensuring that a compromise in one service doesn't provide cluster-wide access.

3. Dual-Scaling Strategy (HPA + VPA)
Choice: - HPA: Configured to scale replicas (1 to 5) based on 50% CPU utilization.

### VPA: Deployed in Recommendation mode to provide data-driven insights for right-sizing resource requests/limits without causing unexpected pod restarts.

4. Observability Stack
Choice: Integrated Prometheus with OpenTelemetry.
Result: Provides full visibility into request latency and system metrics directly from the Kubernetes dashboard.

5. Node Autoscaling (Theoretical)
Choice: Recommended Karpenter for production environments.
Reason: Karpenter provides faster "just-in-time" node provisioning compared to the standard Cluster Autoscaler by interacting directly with the cloud provider's fleet API.

