#!/bin/bash
set -e

echo "Waiting for Solr to start up..."
echo "Waiting for Solr to start up..."
until $(curl --output /dev/null --silent --head --fail http://localhost:8983/solr); do
    echo "waiting"
    sleep 1
done &
echo "Creating Solr core..."
solr create_core -c stock_project_core -d stock_project_configs

echo "Starting Solr..."
exec solr-foreground