#!/bin/bash
psql -c "CREATE USER abidria_user WITH PASSWORD 'password';"
psql -c "CREATE DATABASE abidria_db WITH OWNER abidria_user;"
psql -c "ALTER USER abidria_user CREATEDB;"
