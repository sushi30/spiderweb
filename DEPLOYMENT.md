First deploy the infrastructure (pipelines and artifact buckets)

```shell script
aws cloudformation deploy --template-file=infrastructure.yaml --stack-name=STACK_NAME
```

run
```shell script
aws cloudformation list-exports
```

to get the the list of exports.

```shell script
aws cloudformation package \
--template-file=template.yaml \
--output-template-file packaged.yaml \
--s3-bucket=YOUR_BUCKET 
```

```shell script
aws cloudformation deploy \
--template-file=packaged.yaml \
--stack-name=SpiderwebDev \
--parameter-overrides env=dev
```

