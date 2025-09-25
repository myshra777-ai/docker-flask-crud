\# Dockerized Flask + Postgres CRUD App



This project contains a Flask API with PostgreSQL backend, containerized using Docker and tested via PowerShell scripts.



\## Features

\- Add, update, delete users

\- Docker Compose integration

\- PowerShell test harness with parameters



\## Usage

```bash

docker compose up

.\\test-crud.ps1 -Name "Amit" -Email "amit@example.com" -UserId 2

