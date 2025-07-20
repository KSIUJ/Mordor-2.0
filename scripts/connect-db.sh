#!/bin/bash

echo "Connecting to database..."

# Connection parameters from docker-compose.yml
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="template"
DB_HOST="localhost"
DB_PORT="5432"

# Connect to the database using psql
# The PGPASSWORD must be on the same line as the psql command
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
