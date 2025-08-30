# Hotel App Deploy and Lambdas

The Continous Integration, Delivery and Deployment are carried out by GitHub Actions. 

This repository is executed by Continous Deployment every time that a docker image either backend or frontend is pushed and released to the main branch.


## Project Download
```
git clone https://github.com/alexandermamaniyucra/ccp-hotel-coupon-deploy.git
cd ccp-hotel-coupon-deploy/
```

### About PRODUCTION ENVIRONMENT
you must create a file named ".env.production" in the same directory of project with the environment variables for the database and set up your database configurations

```
MYSQL_DATABASE=databasename
MYSQL_USER=userdatabase
MYSQL_PASSWORD=databasepassword
MYSQL_HOST=host
MYSQL_PORT=3306
MYSQL_ROOT_PASSWORD=password
AWS_ACCESS_KEY_ID=awsaccesskey
AWS_SECRET_ACCESS_KEY=awssecretkey
AWS_STORAGE_BUCKET_NAME=awsbucketname
AWS_REGION=awsrregion
AWS_SQS_QUEUE_URL=sqsurl
AWS_SNS_REPORT_NOTIFICATION_ARN=snsarn
AWS_SNS_USED_COUPON_NOTIFICATION_ARN=snsarn
AWS_SNS_NEW_COUPON_NOTIFICATION_ARN=snsarn
AWS_QUERYSTRING_AUTH=False
```

docker-compose -f docker-compose.production.yml up


### About Dependencies
Docker and Docker compose must be installed in your machine
```shell
sudo apt install docker docker-compose
```
### Excute the docker-compose file
```shell
docker-compose -f docker-compose.staging.yml up
```

## About AWS Lambdas functions

The folder lambdas contains all used lambda functions in the project.

