docker compose -f $1/docker-compose.staging.yml up certbot
chmod o+rw -R $1/certbot
