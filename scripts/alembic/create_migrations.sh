read -p "Enter name of migration: " message
export BOT_CONTAINER_NAME=bot_container_name
docker exec ${BOT_CONTAINER_NAME} alembic revision --autogenerate -m "$message"