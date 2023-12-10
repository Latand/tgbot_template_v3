read -p "Enter name of migration: " message
docker-compose exec bot alembic revision --autogenerate -m "$message"
