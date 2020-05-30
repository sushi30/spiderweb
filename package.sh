#!/bin/sh

INFRA_STACK=$1
DEPLOYMENT_STACK=$2
EXPORT_NAME="$INFRA_STACK-BuildArtifacts"
echo "getting $EXPORT_NAME"
INFRA_BUCKET=$(python get_export.py $EXPORT_NAME)
aws cloudformation package --template-file template.yaml --s3-bucket $INFRA_BUCKET --output-template-file packaged.yaml
aws cloudformation deploy --template-file packaged.yaml --stack-name DEPLOYMENT_STACK

#echo "deploying website"
#npm rm -Rf client/.next
#npm run build --prefix client
#echo "deleting old website"
#sls --config client/serverless.yaml