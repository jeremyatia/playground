# run from code directory
mkdir package
pip install \
    --platform manylinux2010_x86_64 \
    --implementation cp \
    --only-binary=:all: --upgrade \
    --target ./package \
    -r requirements.txt


cp ./* package/

cd package
rm -r package # the package inside package
zip -r ../my_deployment_package.zip .

