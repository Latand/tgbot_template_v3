# SET ENVIRONMENT VARIABLES
export PG_CONTAINER_NAME=pg_database
export POSTGRES_USER=someusername
export POSTGRES_DB=bot
docker exec -t ${PG_CONTAINER_NAME} pg_dump -U ${POSTGRES_USER} -Fp -f /tmp/db_dump.sql --dbname=${POSTGRES_DB}
mkdir -p ./postgres
docker cp ${PG_CONTAINER_NAME}:/tmp/db_dump.sql ./postgres/db_dump.sql
