export INTERNAL_LB_IP=$(kubectl get svc locust-master-web  \
                               -o jsonpath="{.status.loadBalancer.ingress[0].ip}") && \
                               echo $INTERNAL_LB_IP

export PROXY_VM=locust-nginx-proxy
export ZONE=us-central1-c

gcloud compute instances create-with-container ${PROXY_VM} \
   --zone ${ZONE} \
   --container-image gcr.io/cloud-marketplace/google/nginx1:latest \
   --container-mount-host-path=host-path=/tmp/server.conf,mount-path=/etc/nginx/conf.d/default.conf \
   --metadata=startup-script="#! /bin/bash
     cat <<EOF  > /tmp/server.conf
     server {
         listen 8089;
         location / {
             proxy_pass http://${INTERNAL_LB_IP}:8089;
         }
     }
EOF"

gcloud compute ssh --zone ${ZONE} ${PROXY_VM} \
                 -- -N -L 8089:localhost:8089
