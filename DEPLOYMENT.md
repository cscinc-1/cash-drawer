# Cash Drawer Reports - Deployment Guide

## Docker Deployment

### Building the Docker Image

```bash
# Build the Docker image
docker build -t cashdrawer-reports:latest .
```

### Running with Docker Compose (Local Testing)

```bash
# Start the application
docker-compose up

# Or run in background
docker-compose up -d

# Stop the application
docker-compose down
```

Access the application at: http://localhost:8000

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, Docker Desktop K8s, or cloud provider)
- kubectl configured
- Database file (BullittDrawer.db) available

### Step 1: Prepare the Database

Copy your `BullittDrawer.db` file to the host machine's `/mnt/data/cashdrawer/` directory:

```bash
# Create directory on the host
sudo mkdir -p /mnt/data/cashdrawer

# Copy database file
sudo cp ../BullittDrawer.db /mnt/data/cashdrawer/
```

### Step 2: Build and Load Docker Image

For local Kubernetes (minikube/Docker Desktop):

```bash
# Build the image
docker build -t cashdrawer-reports:latest .

# For minikube, load the image
minikube image load cashdrawer-reports:latest

# For Docker Desktop, the image is already available
```

For cloud deployment, push to a registry:

```bash
# Tag the image
docker tag cashdrawer-reports:latest your-registry/cashdrawer-reports:latest

# Push to registry
docker push your-registry/cashdrawer-reports:latest
```

### Step 3: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Create ConfigMap and Secret
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml

# Create PersistentVolume and PersistentVolumeClaim
kubectl apply -f kubernetes/pv-pvc.yaml

# Deploy the application
kubectl apply -f kubernetes/deployment.yaml

# Create services
kubectl apply -f kubernetes/service.yaml

# Optional: Create Ingress (requires Ingress controller)
kubectl apply -f kubernetes/ingress.yaml
```

### Step 4: Verify Deployment

```bash
# Check pod status
kubectl get pods -n cashdrawer

# Check services
kubectl get svc -n cashdrawer

# View logs
kubectl logs -n cashdrawer deployment/cashdrawer-deployment

# Get service URL (for NodePort)
kubectl get svc -n cashdrawer cashdrawer-nodeport
```

### Accessing the Application

#### Option 1: NodePort (Default)
Access at: http://<node-ip>:30080

For minikube:
```bash
minikube service cashdrawer-nodeport -n cashdrawer --url
```

#### Option 2: LoadBalancer
```bash
kubectl get svc -n cashdrawer cashdrawer-service
```
Access at the EXTERNAL-IP shown

#### Option 3: Ingress
Add to `/etc/hosts`:
```
<ingress-controller-ip> cashdrawer.local
```
Access at: http://cashdrawer.local

### Scaling

```bash
# Scale deployment
kubectl scale deployment cashdrawer-deployment -n cashdrawer --replicas=3

# Enable autoscaling
kubectl autoscale deployment cashdrawer-deployment -n cashdrawer --min=2 --max=5 --cpu-percent=80
```

### Updating the Application

```bash
# Build new image
docker build -t cashdrawer-reports:v2 .

# Update deployment
kubectl set image deployment/cashdrawer-deployment cashdrawer=cashdrawer-reports:v2 -n cashdrawer

# Check rollout status
kubectl rollout status deployment/cashdrawer-deployment -n cashdrawer
```

### Cleanup

```bash
# Delete all resources
kubectl delete namespace cashdrawer

# Or delete individual resources
kubectl delete -f kubernetes/
```

## Production Considerations

1. **Secret Management**: Use Kubernetes Secrets management tools (Sealed Secrets, External Secrets)
2. **Database**: Consider using a managed database service
3. **Monitoring**: Add Prometheus/Grafana for monitoring
4. **Logging**: Use ELK stack or cloud logging solutions
5. **Backup**: Implement regular database backups
6. **SSL/TLS**: Configure HTTPS with cert-manager
7. **Security**: 
   - Change the SECRET_KEY in production
   - Use network policies
   - Implement RBAC
   - Scan images for vulnerabilities

## Troubleshooting

### Pod not starting
```bash
kubectl describe pod <pod-name> -n cashdrawer
kubectl logs <pod-name> -n cashdrawer
```

### Database connection issues
- Verify PersistentVolume is bound
- Check database file exists in mounted volume
- Verify DATABASE_PATH environment variable

### Service not accessible
- Check service endpoints: `kubectl get endpoints -n cashdrawer`
- Verify firewall rules
- Check NodePort range (30000-32767)