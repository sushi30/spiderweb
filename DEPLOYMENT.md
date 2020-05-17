run cloudformation script:

set up infrastructure:
```shell script
aws cloudformation deploy --template-file infrustructure.yaml --stack-name YOUR_INFRA_STACK
```

```shell script
aws cloudformation package --template-file template.yaml 
aws cloudformation deploy --template-file template.yaml --stack-name YOUR_STACK
```