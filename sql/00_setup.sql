-- One-time setup, run as the postgres admin user in psql
CREATE USER olist WITH PASSWORD 'olist';
CREATE DATABASE olist OWNER olist;