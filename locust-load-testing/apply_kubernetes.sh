export SAMPLE_APP_TARGET=35.192.101.24:8000
export PROJECT=fiery-synthesis-359714
export AR_REPO=dist-lt-repo
export REGION=us-central1

export LOCUST_IMAGE_NAME=locust-tasks
export LOCUST_IMAGE_TAG=latest

envsubst < kubernetes-config/locust-master-controller.yaml.tpl | kubectl apply -f -
envsubst < kubernetes-config/locust-worker-controller.yaml.tpl | kubectl apply -f -
envsubst < kubernetes-config/locust-master-service.yaml.tpl | kubectl apply -f -
