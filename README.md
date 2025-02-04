# DST_MLOPS_05_Kubernetes_Exam
Datascientest Cursus MLOPS - Sprint 5 - Kubernetes Exam



## General commands
> Get all resources across all namespaces with detailed information
kubectl get all --all-namespaces -o wide



## Namespace creation
> create the namespace
kubectl create namespace k8s-exam

> deletion
kubectl delete namespace k8s-exam



## Secrets as environment variables creation
Directory: any 

> create the password of superuser + check
kubectl create secret generic k8s-exam-mysqldb-superuser --from-literal 'MYSQL_ROOT_PASSWORD=dstsuperuser2025!_' -n k8s-exam
kubectl get secret k8s-exam-mysqldb-superuser -n k8s-exam
> create the secret of common user and the name of database at startup on which he's granted + check
kubectl create secret generic k8s-exam-mysqldb-user \
--from-literal 'MYSQL_USER=dstuser' \
--from-literal 'MYSQL_PASSWORD=dstuser2025!_' \
--from-literal 'MYSQL_DATABASE=k8s-exam-db' \
--from-literal 'MYSQL_HOST=k8s-exam-mysqldb-service' \
-n k8s-exam
kubectl get secret k8s-exam-mysqldb-user -n k8s-exam

> deletion
kubectl delete secret k8s-exam-mysqldb-superuser -n k8s-exam
kubectl delete secret k8s-exam-mysqldb-user -n k8s-exam



## PersitentVolume and PersistentVolumeClaim creation
> PersitentVolume (PV) creation (no namespace tied) + check
kubectl apply -f mysql-local-data-folder-pv.yaml 
kubectl get pv 
> PersistentVolumeClaim (PVC) creation (namespace tied) + check
kubectl apply -f mysql-local-data-folder-pvc.yaml -n k8s-exam
kubectl get pvc -n k8s-exam

> deletion
kubectl delete pv k8s-exam-pv
kubectl delete pvc -n k8s-exam



## Launch the StatefulSet
Directory: /home/ubuntu/DST_MLOPS_05_Kubernetes_Exam/eval/mysql

> create the item StatefulSet + check
kubectl create -f mysql-statefulset.yml -n k8s-exam
kubectl get sts k8s-exam-mysqldb -n k8s-exam
> check environment variables
kubectl exec -it k8s-exam-mysqldb-0 -n k8s-exam env | grep MYSQLDB
> check config file content
kubectl exec -it k8s-exam-mysqldb-0 -n k8s-exam -- cat /etc/mysql/conf.d/mysqld.cnf
> check the use of environment variables
    kubectl exec -it k8s-exam-mysqldb-0 -n k8s-exam -- /bin/sh
    > check the ability to use the root password
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e 'show databases;'
    > check the parsing of config file
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "SHOW VARIABLES LIKE 'max_allowed_packet';"

> debug + logs
kubectl get all -n k8s-exam
kubectl describe pod k8s-exam-mysqldb-0 -n k8s-exam
kubectl logs k8s-exam-mysqldb-0 -n k8s-exam

> deletion
kubectl delete sts k8s-exam-mysqldb -n k8s-exam



## Launch the mysql exposing service
Directory: /home/ubuntu/DST_MLOPS_05_Kubernetes_Exam/eval/mysql

> create the item NodePort + check
kubectl apply -f mysql-service.yml -n k8s-exam
kubectl get svc k8s-exam-mysqldb-service -n k8s-exam

> deletion 
kubectl delete svc k8s-exam-mysqldb-service -n k8s-exam



## Prepare the final api image
### Build the first version of api
> build the docker image
docker build -t k8s-exam-fastapi:latest .

> connect to dockerhub
docker login

> tag the image
docker tag k8s-exam-fastapi:latest thibaultbezpalko/k8s-dst-eval-fastapi:latest

> push the image to Dockerhub
docker push thibaultbezpalko/k8s-dst-eval-fastapi:latest


### Launch the api 
Prerequisite: launch the mysql exposing service
Directory: /home/ubuntu/DST_MLOPS_05_Kubernetes_Exam/eval/test

> create the item fastapi
kubectl apply -f fastapi-pod.yaml -n k8s-exam
kubectl get pod k8s-exam-fastapi -n k8s-exam

> logs
kubectl logs -f k8s-exam-fastapi -n k8s-exam

> deletion 
kubectl delete pod k8s-exam-fastapi -n k8s-exam


### Launch the api exposing service
> create the item NodePort + check
kubectl apply -f fastapi-pod-nodeport.yml -n k8s-exam
kubectl get svc k8s-exam-fastapi-pod-nodeport -n k8s-exam

> deletion 
kubectl delete svc k8s-exam-fastapi-pod-nodeport -n k8s-exam



## Deploy and expose the api replicaset
Directory: /home/ubuntu/DST_MLOPS_05_Kubernetes_Exam/eval/fastapi

> create the item fastapi
kubectl create -f fastapi-deploy.yml -n k8s-exam
kubectl get deploy k8s-exam-fastapi-deploy -n k8s-exam

> logs
kubectl get pod -n k8s-exam
kubectl logs -f <pod name> -n k8s-exam
kubectl logs -f k8s-exam-fastapi-deploy-bb665b8d9-55krv -n k8s-exam
kubectl logs -f k8s-exam-fastapi-deploy-bb665b8d9-p9n49 -n k8s-exam
kubectl logs -f k8s-exam-fastapi-deploy-bb665b8d9-lflrn -n k8s-exam

> deletion 
kubectl delete deploy k8s-exam-fastapi-deploy -n k8s-exam




## Launch the api exposing service
Directory: /home/ubuntu/DST_MLOPS_05_Kubernetes_Exam/eval/fastapi

> create the item NodePort + check
kubectl apply -f fastapi-nodeport.yml -n k8s-exam
kubectl get svc k8s-exam-fastapi-nodeport -n k8s-exam

> deletion 
kubectl delete svc k8s-exam-fastapi-nodeport -n k8s-exam



