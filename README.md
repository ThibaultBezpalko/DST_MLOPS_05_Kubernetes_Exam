# DST_MLOPS_05_Kubernetes_Exam
Datascientest Cursus MLOPS - Sprint 5 - Kubernetes Exam


## Namespace creation
kubectl create namespace k8s-exam


## Secrets as environment variables creation
> create the password of superuser + check
kubectl create secret generic k8s-exam-mysqldb-superuser --from-literal 'MYSQL_ROOT_PASSWORD=dstsuperuser2025!_' --namespace=k8s-exam
kubectl get secret k8s-exam-mysqldb-superuser --namespace=k8s-exam
> create the secret of common user and the name of database at startup on which he's granted + check
kubectl create secret generic k8s-exam-mysqldb-user \
--from-literal 'MYSQL_USER=dstuser' \
--from-literal 'MYSQL_PASSWORD=dstuser2025!_' \
--from-literal 'MYSQL_DATABASE=k8s-exam-mysqldb' \
--namespace=k8s-exam
kubectl get secret k8s-exam-mysqldb-user --namespace=k8s-exam

> deletion
kubectl delete secret k8s-exam-mysqldb-superuser --namespace=k8s-exam
kubectl delete secret k8s-exam-mysqldb-user --namespace=k8s-exam


## PersitentVolume and PersistentVolumeClaim creation
> PersitentVolume (PV) creation (no namespace tied) + check
kubectl apply -f mysql-local-data-folder-pv.yaml 
kubectl get pv 
> PersistentVolumeClaim (PVC) creation (namespace tied) + check
kubectl apply -f mysql-local-data-folder-pvc.yaml --namespace=k8s-exam
kubectl get pvc --namespace=k8s-exam


## Launch the StatefulSet
> create the item StatefulSet + check
kubectl create -f mysql-statefulset.yml -n k8s-exam
kubectl get sts k8s-exam-mysqldb -n k8s-exam
> check environment variables
kubectl exec -it k8s-exam-mysqldb-0 env | grep MYSQLDB
> check config file content
kubectl exec -it k8s-exam-mysqldb-0 -- cat /etc/mysql/conf.d/mysqld.cnf
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
> create the item NodePort + check
kubectl apply -f mysql-NodePort.yml -n k8s-exam
kubectl get svc k8s-exam-mysqldb-nodeport -n k8s-exam

> deletion 
kubectl delete svc k8s-exam-mysqldb-nodeport -n k8s-exam
