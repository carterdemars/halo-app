Run the following command to deploy the function
```
gcloud run deploy <function-name> \
  --source . \                      
  --region=northamerica-northeast2 \
  --project=leafy-summer-476303-c1 \
  --allow-unauthenticated
```