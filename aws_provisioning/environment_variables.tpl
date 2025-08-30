cat << EOF >> ./.ENVIRONMENT_VARIABLES

${instance}_PUBLIC_IP=${public_ip}
${instance}_PRIVATE_IP=${private_ip}
EOF
