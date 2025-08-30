mkdir package
cp lambda_function.py package
pip install --target package pymysql
#pip install -i https://test.pypi.org/simple/ hotel-coupon-app-package-alexandermamani --upgrade --target package
cd package/
zip -r ../lambda_function.zip .
