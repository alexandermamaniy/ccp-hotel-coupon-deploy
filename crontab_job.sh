docker compose -f $1/docker-compose.staging.yml up certbot
chown 1000:1000 -R $1/certbot
