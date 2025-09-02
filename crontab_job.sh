docker compose -f $1/docker-compose.staging.yml up certbot
chmod o+rwx -R $1/certbot
