# Cash Drawer Reports

A Django web application for viewing and reporting on cash drawer transactions from the Bullitt County Sheriff's office.

## Quick Start

**Prerequisites**: Make sure you have everything installed as described in [INSTALL.md](./INSTALL.md).

### 1. Start the Development Environment

```bash
cd cashdrawer_reports
tilt up
```

Press **SPACE** to open the Tilt UI in your browser.

### 2. Initialize the Database (First Time Only)

In the Tilt UI, click the **"copy-db"** button to copy the SQLite database into the container.

### 3. Access the Application

- **Main Application**: http://localhost:8000
- **Alternative Access**: http://localhost:30081 (NodePort)

## Development Workflow

### Making Changes

The development environment supports **live reloading**:

- **Template changes** (`.html` files) → Instant refresh in browser
- **Python code changes** (`.py` files) → Automatic server restart
- **Static files** → Auto-collection

Simply save your files and refresh your browser - no manual restarts needed!

### Useful Tilt UI Buttons

| Button | Purpose |
|--------|---------|
| **migrate** | Run Django database migrations |
| **shell** | Open Django shell for debugging |
| **logs** | View real-time application logs |
| **copy-db** | Refresh database from source |
| **open-browser** | Quick link to open the app |

### Common Tasks

```bash
# Run database migrations
tilt trigger migrate

# Open Django shell
tilt trigger shell

# View logs
tilt logs -f cashdrawer-reports-dev

# Stop everything
tilt down
```

## Application Features

- **Daily Transactions Report** - View transactions by date and drawer
- **Accounts Report** - Summary of account activities  
- **Print-Optimized Views** - Clean, professional printed reports
- **Multi-Drawer Support** - Separate reporting by cash drawer

## Project Structure

```
cashdrawer_reports/
├── reports/                    # Django app
│   ├── templates/             # HTML templates
│   ├── views.py              # View logic
│   ├── models.py             # Database models
│   └── urls.py               # URL routing
├── helm/                      # Kubernetes deployment
│   ├── cashdrawer-reports/   # Helm chart
│   └── values.dev.yaml       # Development values
├── Tiltfile                   # Development orchestration
├── Dockerfile                 # Container definition
└── README.md                  # This file
```

## Troubleshooting

### Application Not Loading?

1. Check the Tilt UI for error messages
2. Ensure database was copied: click **"copy-db"** button
3. Check logs: click **"logs"** button in Tilt UI

### Changes Not Appearing?

1. Verify the Django development server is running (check Tilt UI logs)
2. Hard refresh your browser (Cmd/Ctrl + Shift + R)
3. If still not working: `tilt down` then `tilt up`

### Need to Reset?

```bash
tilt down
tilt up
# Click "copy-db" in Tilt UI
```

## More Information

- **[INSTALL.md](./INSTALL.md)** - Complete installation and setup guide
- **[Tilt Documentation](https://docs.tilt.dev/)** - Learn more about Tilt
- **[Django Documentation](https://docs.djangoproject.com/)** - Django framework docs

## Development Notes

This project uses:
- **Django** - Web framework
- **SQLite** - Database (read-only copy of BullittDrawer.db)
- **Tilt** - Development environment orchestration
- **Kubernetes** - Container orchestration (via Docker Desktop or similar)
- **Helm** - Kubernetes application packaging

The development setup automatically runs Django in development mode with debug enabled and template auto-reloading active.