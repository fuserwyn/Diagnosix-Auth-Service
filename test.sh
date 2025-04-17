#!/bin/bash
WEB_NAME=$(docker ps --format "table {{.Names}}" | grep web_app)

DB_NAME=$(docker ps --format "table {{.Names}}" | grep postgres)
echo "Push to $DB_NAME"
docker exec -it $DB_NAME psql -c "DROP USER if exists app_db_user" -c "CREATE USER app_db_user with PASSWORD 'SECRET_PASS';ALTER ROLE app_db_user with createdb;"
docker exec -it $DB_NAME psql -U app_db_user -d app_db -c "drop database if exists app_db_user;" -c "create database app_db_user;" -c "GRANT ALL PRIVILEGES ON DATABASE app_db_user to app_db_user;"


echo "Started pytest"
docker exec -it $WEB_NAME pytest -s