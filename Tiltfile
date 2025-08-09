# -*- mode: Python -*-
# Tiltfile for Cash Drawer Reports development

# Allow k8s_resource to be updated
update_settings(max_parallel_updates=3)

# Set default registry for local development (comment out if not using local registry)
# default_registry('localhost:5000', single_name='cashdrawer')

# Load environment variables from .env if it exists (optional)
# load('ext://dotenv', 'dotenv')
# dotenv()

# Configuration
namespace = 'cashdrawer-dev'
release_name = 'cashdrawer-reports-dev'
chart_path = './helm/cashdrawer-reports'
values_file = './helm/values.dev.yaml'

# Ensure namespace exists
k8s_yaml(encode_yaml({
    'apiVersion': 'v1',
    'kind': 'Namespace',
    'metadata': {
        'name': namespace
    }
}))

# Build the Docker image with live updates
docker_build(
    'cashdrawer-reports',
    '.',
    dockerfile='./Dockerfile',
    live_update=[
        # Sync Python source code
        sync('./reports/', '/app/reports/'),
        sync('./cashdrawer_reports/', '/app/cashdrawer_reports/'),
        
        # Sync templates - Django will auto-reload these
        sync('./reports/templates/', '/app/reports/templates/'),
        
        # Sync static files if they exist
        sync('./reports/static/', '/app/reports/static/'),
        
        # Django development server will auto-reload for both templates and Python files
    ],
    ignore=[
        '.git',
        '*.pyc',
        '__pycache__',
        '.pytest_cache',
        'helm/',
        'kubernetes/',
        '*.md',
        '.tiltignore',
        'Tiltfile',
        'debugging/',
    ]
)

# Deploy using Helm
k8s_yaml(
    helm(
        chart_path,
        name=release_name,
        namespace=namespace,
        values=[values_file] if os.path.exists(values_file) else [],
        set=[
            'image.repository=cashdrawer-reports',
            'image.tag=latest',
            'image.pullPolicy=Always',
            'django.debug=true',
            'env.ENV=development',
            'service.type=NodePort',
            'nodePort.enabled=true',
            'nodePort.port=30081',
            'persistence.enabled=false',
            'autoscaling.enabled=false',
            'replicaCount=1',
        ]
    )
)

# Configure k8s resources
k8s_resource(
    workload='cashdrawer-reports-dev',
    port_forwards=[
        '8000:8000',  # Django app
    ],
    resource_deps=['namespace'],
    labels=['django'],
    auto_init=True,
    trigger_mode=TRIGGER_MODE_AUTO
)

# PVC removed - using read-only SQLite for now

# Add buttons for common tasks
local_resource(
    'migrate',
    cmd='kubectl exec -it deployment/cashdrawer-reports-dev -n %s -- python manage.py migrate' % namespace,
    labels=['django'],
    auto_init=False,
)

local_resource(
    'shell',
    cmd='kubectl exec -it deployment/cashdrawer-reports-dev -n %s -- python manage.py shell' % namespace,
    labels=['django'],
    auto_init=False,
)

local_resource(
    'logs',
    cmd='kubectl logs -f deployment/cashdrawer-reports-dev -n %s' % namespace,
    labels=['django'],
    auto_init=False,
)

local_resource(
    'copy-db',
    cmd='kubectl cp ../BullittDrawer.db %s/deployment/cashdrawer-reports-dev:/data/BullittDrawer.db' % namespace,
    labels=['storage'],
    auto_init=False,
)

# Create a button to open the app in browser
local_resource(
    'open-browser',
    cmd='open http://localhost:8000 || xdg-open http://localhost:8000 || start http://localhost:8000',
    labels=['django'],
    auto_init=False,
)

# Print helpful information
print("""
🚀 Cash Drawer Reports Development Environment

Available endpoints:
  - Application: http://localhost:8000
  - NodePort:    http://localhost:30081

Useful commands:
  - tilt up        : Start development environment
  - tilt down      : Stop and clean up
  - tilt trigger   : Manually trigger resource updates
  
In Tilt UI:
  - Click 'migrate' to run database migrations
  - Click 'shell' to open Django shell
  - Click 'logs' to view application logs
  - Click 'copy-db' to copy database to container
  - Click 'open-browser' to open the app

Press SPACE to open Tilt UI in browser
""")