# Cash Drawer Reports Helm Chart

A Helm chart for deploying the Cash Drawer Reports Django application to Kubernetes.

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+
- A container registry with the `cashdrawer-reports` image

## Installation

### 1. Build and Push Docker Image

First, build and push the Docker image to your container registry:

```bash
# Build the image
docker build -t your-registry/cashdrawer-reports:latest .

# Push to registry
docker push your-registry/cashdrawer-reports:latest
```

### 2. Prepare the Database

Copy your `BullittDrawer.db` file to the host machine:

```bash
# Create directory on each node
sudo mkdir -p /mnt/data/cashdrawer

# Copy database file
sudo cp ../BullittDrawer.db /mnt/data/cashdrawer/
```

### 3. Install the Chart

```bash
# Add the chart repository (if using a remote repo)
helm repo add cashdrawer-reports https://your-helm-repo.com

# Install with default values
helm install cashdrawer-reports ./helm/cashdrawer-reports

# Or install with custom values
helm install cashdrawer-reports ./helm/cashdrawer-reports -f my-values.yaml
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `2` |
| `image.repository` | Image repository | `cashdrawer-reports` |
| `image.tag` | Image tag | `"latest"` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Container port | `8000` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.hosts[0].host` | Hostname | `cashdrawer.local` |
| `resources.limits.cpu` | CPU limit | `500m` |
| `resources.limits.memory` | Memory limit | `512Mi` |
| `resources.requests.cpu` | CPU request | `250m` |
| `resources.requests.memory` | Memory request | `256Mi` |
| `django.debug` | Django DEBUG setting | `false` |
| `django.secretKey` | Django SECRET_KEY | `"django-production-secret-key-change-this"` |
| `django.allowedHosts` | Django ALLOWED_HOSTS | `"*"` |
| `django.databasePath` | Path to SQLite database | `"/data/BullittDrawer.db"` |
| `persistence.enabled` | Enable persistence | `true` |
| `persistence.size` | PVC size | `1Gi` |
| `persistence.hostPath` | Host path for database | `"/mnt/data/cashdrawer"` |
| `autoscaling.enabled` | Enable HPA | `false` |
| `nodePort.enabled` | Enable NodePort service | `false` |
| `nodePort.port` | NodePort port | `30080` |

## Examples

### Basic Installation

```bash
helm install cashdrawer-reports ./helm/cashdrawer-reports
```

### With Custom Image

```yaml
# values.yaml
image:
  repository: my-registry/cashdrawer-reports
  tag: "v1.0.0"

django:
  secretKey: "your-production-secret-key"
  allowedHosts: "cashdrawer.example.com,localhost"
```

```bash
helm install cashdrawer-reports ./helm/cashdrawer-reports -f values.yaml
```

### With Ingress

```yaml
# values.yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: cashdrawer.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: cashdrawer-tls
      hosts:
        - cashdrawer.example.com
```

### With NodePort

```yaml
# values.yaml
service:
  type: NodePort

nodePort:
  enabled: true
  port: 30080
```

### With Autoscaling

```yaml
# values.yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Accessing the Application

### ClusterIP (Default)
```bash
kubectl port-forward svc/cashdrawer-reports 8080:80
# Access at http://localhost:8080
```

### NodePort
```bash
kubectl get svc cashdrawer-reports-nodeport
# Access at http://<node-ip>:<nodeport>
```

### Ingress
Access at the configured hostname (e.g., http://cashdrawer.example.com)

## Upgrading

```bash
helm upgrade cashdrawer-reports ./helm/cashdrawer-reports -f values.yaml
```

## Uninstallation

```bash
helm uninstall cashdrawer-reports
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -l app.kubernetes.io/name=cashdrawer-reports
```

### View Pod Logs
```bash
kubectl logs -l app.kubernetes.io/name=cashdrawer-reports
```

### Check PVC Status
```bash
kubectl get pvc
```

### Verify Database Mount
```bash
kubectl exec -it deployment/cashdrawer-reports -- ls -la /data/
```

## Security Considerations

1. **Change the Secret Key**: Always change `django.secretKey` in production
2. **Limit Allowed Hosts**: Set `django.allowedHosts` to specific domains
3. **Use TLS**: Enable TLS for ingress in production
4. **Resource Limits**: Set appropriate resource limits
5. **Network Policies**: Consider implementing network policies
6. **Image Security**: Scan images for vulnerabilities

## Support

For issues and questions, please contact the Cash Drawer Team at admin@bullittcounty.gov