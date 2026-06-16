#!/bin/bash
# TSC-CRM Docker Test Script
# Usage: ./test-docker.sh [command]

set -e

COMPOSE="docker compose"
DB_NAME="tsc_crm"

case "${1:-help}" in
  up)
    echo "Starting TSC-CRM environment..."
    $COMPOSE up -d
    echo "Waiting for Odoo to be ready..."
    sleep 10
    echo "Odoo is running at http://localhost:8069"
    echo "Database: $DB_NAME | User: odoo | Password: odoo"
    ;;

  down)
    echo "Stopping TSC-CRM environment..."
    $COMPOSE down
    ;;

  install)
    echo "Installing TSC-CRM modules..."
    $COMPOSE exec odoo odoo -d $DB_NAME -i tsc_crm,tsc_crm_auth,tsc_crm_service,tsc_crm_workflow,tsc_crm_commission,tsc_crm_integration --stop-after-init
    echo "Modules installed successfully!"
    ;;

  update)
    echo "Updating TSC-CRM modules..."
    $COMPOSE exec odoo odoo -d $DB_NAME -u tsc_crm,tsc_crm_auth,tsc_crm_service,tsc_crm_workflow,tsc_crm_commission,tsc_crm_integration --stop-after-init
    echo "Modules updated successfully!"
    ;;

  test)
    echo "Running tests..."
    $COMPOSE exec odoo python -m pytest /mnt/extra-addons/tsc_crm/tests/ -v
    ;;

  shell)
    echo "Opening Odoo shell..."
    $COMPOSE exec odoo odoo shell -d $DB_NAME
    ;;

  logs)
    $COMPOSE logs -f odoo
    ;;

  reset)
    echo "Resetting database..."
    $COMPOSE down -v
    $COMPOSE up -d db
    sleep 5
    $COMPOSE up -d
    sleep 10
    echo "Installing modules..."
    $COMPOSE exec odoo odoo -d $DB_NAME -i tsc_crm,tsc_crm_auth,tsc_crm_service,tsc_crm_workflow,tsc_crm_commission,tsc_crm_integration --stop-after-init
    echo "Database reset and modules installed!"
    ;;

  help|*)
    echo "TSC-CRM Docker Test Commands:"
    echo ""
    echo "  ./test-docker.sh up        Start environment"
    echo "  ./test-docker.sh down      Stop environment"
    echo "  ./test-docker.sh install   Install all modules"
    echo "  ./test-docker.sh update    Update all modules"
    echo "  ./test-docker.sh test      Run tests"
    echo "  ./test-docker.sh shell     Open Odoo shell"
    echo "  ./test-docker.sh logs      View Odoo logs"
    echo "  ./test-docker.sh reset     Reset DB and reinstall"
    echo ""
    ;;
esac
