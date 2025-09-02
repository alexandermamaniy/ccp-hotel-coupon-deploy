docker compose -f docker-compose.staging.yml up certbot
chown $USER:$USER -R $1/certbot
