#!/bin/bash

# Cash Drawer Reports Helm Deployment Script

set -e

CHART_NAME="cashdrawer-reports"
RELEASE_NAME="cashdrawer-reports"
NAMESPACE="cashdrawer"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed. Please install Helm 3.0+"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl"
    exit 1
fi

print_status "Starting Cash Drawer Reports deployment..."

# Create namespace if it doesn't exist
print_status "Creating namespace ${NAMESPACE}..."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Validate the chart
print_status "Validating Helm chart..."
helm lint ./${CHART_NAME}/

# Check if release already exists
if helm list -n ${NAMESPACE} | grep -q ${RELEASE_NAME}; then
    print_warning "Release ${RELEASE_NAME} already exists. Upgrading..."
    helm upgrade ${RELEASE_NAME} ./${CHART_NAME}/ \
        --namespace ${NAMESPACE} \
        --wait \
        --timeout 10m
    print_success "Upgrade completed successfully!"
else
    print_status "Installing new release ${RELEASE_NAME}..."
    helm install ${RELEASE_NAME} ./${CHART_NAME}/ \
        --namespace ${NAMESPACE} \
        --wait \
        --timeout 10m \
        --create-namespace
    print_success "Installation completed successfully!"
fi

# Display deployment status
print_status "Deployment status:"
kubectl get pods -n ${NAMESPACE} -l app.kubernetes.io/name=${CHART_NAME}

print_status "Services:"
kubectl get svc -n ${NAMESPACE}

# Get access information
print_status "Access information:"
SERVICE_TYPE=$(kubectl get svc ${RELEASE_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.type}')

if [ "$SERVICE_TYPE" = "NodePort" ]; then
    NODE_PORT=$(kubectl get svc ${RELEASE_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.ports[0].nodePort}')
    print_success "Application available at: http://<node-ip>:${NODE_PORT}"
elif [ "$SERVICE_TYPE" = "LoadBalancer" ]; then
    print_success "Waiting for LoadBalancer IP..."
    kubectl get svc ${RELEASE_NAME} -n ${NAMESPACE} --watch
else
    print_success "Use port-forward to access: kubectl port-forward svc/${RELEASE_NAME} 8080:80 -n ${NAMESPACE}"
    print_success "Then access at: http://localhost:8080"
fi

print_success "Cash Drawer Reports deployed successfully!"
print_status "To check logs: kubectl logs -f deployment/${RELEASE_NAME} -n ${NAMESPACE}"
print_status "To uninstall: helm uninstall ${RELEASE_NAME} -n ${NAMESPACE}"