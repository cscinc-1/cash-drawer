# Tilt Development Guide

This guide explains how to use Tilt for local development of the Cash Drawer Reports application with Kubernetes.

## Prerequisites

1. **Install Tilt**: https://docs.tilt.dev/install.html
   ```bash
   # macOS
   brew install tilt-dev/tap/tilt
   
   # Linux
   curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
   
   # Windows
   scoop bucket add tilt-dev https://github.com/tilt-dev/scoop-bucket
   scoop install tilt
   ```

2. **Local Kubernetes Cluster** (one of):
   - Docker Desktop with Kubernetes enabled
   - Minikube: `minikube start`
   - Kind: `kind create cluster`
   - k3s/k3d

3. **kubectl** configured to connect to your cluster

## Quick Start

Just run:
```bash
cd cashdrawer_reports
tilt up
```

Press SPACE to open the Tilt UI in your browser.

**Access the Application**:
- Main app: http://localhost:8000
- NodePort: http://localhost:30080

**First time only**: Click the "copy-db" button in Tilt UI to copy the database to the container.

## Features

### Live Updates
The Tiltfile is configured with live updates for rapid development:
- **Python code changes**: Automatically synced and Django restarted
- **Template changes**: Instantly reflected without rebuild
- **Static files**: Automatically collected when changed

### Tilt UI Resources

The Tilt UI provides several helpful buttons:

| Resource | Description | Usage |
|----------|-------------|-------|
| **migrate** | Run Django migrations | Click when database schema changes |
| **shell** | Open Django shell | Interactive Python shell with Django context |
| **logs** | View application logs | Real-time log streaming |
| **copy-db** | Copy database to container | Initial setup or database refresh |
| **open-browser** | Open app in browser | Quick access to the application |

### Development Workflow

1. **Making Code Changes**:
   - Edit Python files → Automatic restart
   - Edit templates → Instant update
   - Edit static files → Auto-collection

2. **Database Operations**:
   ```bash
   # Run migrations
   tilt trigger migrate
   
   # Access Django shell
   tilt trigger shell
   
   # Copy fresh database
   tilt trigger copy-db
   ```

3. **Debugging**:
   - View logs in Tilt UI
   - Use `kubectl` commands for deeper inspection
   - Port-forward for direct access

## Configuration

### Tiltfile Configuration

The Tiltfile includes these key configurations:

```python
# Namespace for development
namespace = 'cashdrawer-dev'

# Port forwards
port_forwards=['8000:8000']

# Live update paths
sync('./reports/', '/app/reports/')
sync('./cashdrawer_reports/', '/app/cashdrawer_reports/')
```

### Development Values

The `helm/values.dev.yaml` file contains development-specific overrides:
- Single replica for faster updates
- Debug mode enabled
- NodePort service for easy access
- Reduced resource requirements

## Advanced Usage

### Custom Port Forwarding

Add additional port forwards in the Tiltfile:
```python
k8s_resource(
    workload='cashdrawer-reports-dev',
    port_forwards=[
        '8000:8000',  # Django
        '5432:5432',  # Database (if using PostgreSQL)
    ]
)
```

### Environment Variables

Create a `.env` file for local environment variables:
```bash
# .env
SECRET_KEY=your-dev-secret-key
DEBUG=True
DATABASE_URL=sqlite:///data/BullittDrawer.db
```

### Multiple Environments

Create different values files for different scenarios:
```bash
# Use staging values
tilt up -- --values-file=helm/values.staging.yaml
```

### Disable Live Updates

For production-like testing:
```python
# In Tiltfile, comment out live_update section
docker_build(
    'cashdrawer-reports',
    '.',
    dockerfile='./Dockerfile',
    # live_update=[...] # Commented out
)
```

## Troubleshooting

### Pod Not Starting

1. Check Tilt UI for error messages
2. View detailed logs:
   ```bash
   kubectl logs -n cashdrawer-dev deployment/cashdrawer-reports-dev
   ```
3. Describe pod:
   ```bash
   kubectl describe pod -n cashdrawer-dev -l app.kubernetes.io/name=cashdrawer-reports
   ```

### Database Issues

1. Ensure database file exists:
   ```bash
   kubectl exec -n cashdrawer-dev deployment/cashdrawer-reports-dev -- ls -la /data/
   ```
2. Re-copy database:
   - Click "copy-db" in Tilt UI

### Port Already in Use

Change the port in Tiltfile:
```python
port_forwards=['8001:8000']  # Use port 8001 locally
```

### Tilt Not Detecting Changes

1. Check `.tiltignore` file
2. Ensure file paths in `sync()` are correct
3. Restart Tilt: `tilt down && tilt up`

## Best Practices

1. **Use Tilt UI**: The web UI provides excellent visibility into your resources
2. **Check Logs**: Always check logs when something doesn't work
3. **Clean Restart**: Use `tilt down` before `tilt up` for a clean state
4. **Version Control**: Don't commit `.env` or `values.dev.yaml` with secrets

## Commands Reference

```bash
# Start Tilt
tilt up

# Start with specific values
tilt up -- --values-file=custom-values.yaml

# Open UI
tilt up --browser

# Stop Tilt (keeps resources)
Ctrl+C

# Stop and clean up
tilt down

# Trigger a resource manually
tilt trigger <resource-name>

# Get resource status
tilt get <resource-name>

# View logs
tilt logs -f <resource-name>
```

## Integration with IDEs

### VS Code
Install the Tilt extension for VS Code for integrated development.

### IntelliJ/PyCharm
Configure remote debugging to connect to the containerized Django app.

## Performance Tips

1. **Reduce Sync Paths**: Only sync directories you're actively working on
2. **Use `.tiltignore`**: Exclude unnecessary files from Docker builds
3. **Optimize Dockerfile**: Use multi-stage builds and cache dependencies
4. **Resource Limits**: Adjust resource limits based on your machine's capacity

## Next Steps

- Explore [Tilt Extensions](https://github.com/tilt-dev/tilt-extensions)
- Set up [Custom Buttons](https://docs.tilt.dev/buttons.html)
- Configure [Tests in Tilt](https://docs.tilt.dev/example_test.html)
- Add [Metrics and Monitoring](https://docs.tilt.dev/metrics.html)