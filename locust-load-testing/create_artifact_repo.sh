export AR_REPO=dist-lt-repo
export REGION=us-central1

gcloud artifacts repositories create ${AR_REPO} \
    --repository-format=docker  \
    --location=${REGION} \
    --description="Distributed load testing with GKE and Locust"
