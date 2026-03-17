# Minikube deploy on Linux Ubuntu VM (based on Proxmox env)

# Kubernetes Tasks for Minikube

## Task 1 — Cluster Startup [v]

- Install Minikube (any driver).
- Start the cluster with your chosen configuration.
- Check all system components and ensure everything is running correctly.

**Expected result:**
- one node in *Ready* state,
- all core pods running.

---
### Solution:
- Install Minikube:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

- Run minikube cluster:
```bash
minikube start --driver=docker
```

- Install kubectl:
```bash
sudo snap install kubectl --classic
```

- check Kubernetes status:
```bash
kubectl get nodes
---->
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   115s   v1.34.0

kubectl get pods -A
---->
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-66bc5c9577-l2v94           1/1     Running   0               3m2s
kube-system   etcd-minikube                      1/1     Running   0               3m8s
kube-system   kube-apiserver-minikube            1/1     Running   0               3m8s
kube-system   kube-controller-manager-minikube   1/1     Running   0               3m8s
kube-system   kube-proxy-tl7kr                   1/1     Running   0               3m3s
kube-system   kube-scheduler-minikube            1/1     Running   0               3m8s
kube-system   storage-provisioner                1/1     Running   1 (2m31s ago)   3m6s
```

## Task 2 — Simple Application

- Create a Deployment with one replica of any lightweight application.
- Expose it outside the cluster using a *NodePort* Service.
- Verify that the application responds in your browser.
---
### Solution:
*Using nginx*

- create deployment.yml from template:
```yml
kubectl create deployment nginx --image=nginx:latest --dry-run=client -o yaml > deployment.yml
---->
apiVersion: apps/v1

kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:latest
        name: nginx
        resources: {}
status: {}
```
---
### Apply deployment.yml:
```bash
kubectl apply -f deployment.yml
```
---
### Check deployment status:
```bash
kubectl get deployments
kubectl get pods
```

---
### Set NodePort to expose the port outside

To expose the port outside the cluster we need to create _service.yml_ file:
```yml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30036
    protocol: TCP
```

Then just apply the changes deployment:
```bash
kubectl apply -f deployment.yml
```
and service:
```bash
kubectl apply -f service.yml
```
### Verification:
Check the services:
```bash
kubectl get svc
---->
NAME            TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
kubernetes      ClusterIP   10.96.0.1     <none>        443/TCP        13d
nginx-service   NodePort    10.98.75.55   <none>        80:30036/TCP   86s
```
Check minikube services:
```bash
minikube service _appName_
---->
minikube service nginx-service
---->
┌───────────┬───────────────┬─────────────┬───────────────────────────┐
│ NAMESPACE │     NAME      │ TARGET PORT │            URL            │
├───────────┼───────────────┼─────────────┼───────────────────────────┤
│ default   │ nginx-service │ 80          │ http://192.168.49.2:30036 │
└───────────┴───────────────┴─────────────┴───────────────────────────┘
```

## Task 3 Scaling and Rollout [v]
---

- Increase the number of replicas in the Deployment.
- Perform a rolling update to a different image version.
- Roll back the update to the previous version.
- Check the rollout history.
---
### Solution
Increasing the number of replicas in the *deployment.yml* we do this changing the *replicas: X* value
example:
```yml
[...]
spec:
  replicas: 2 #previous: 1
[...]
```
This changing means that Kubernetes will create as much pods as *replicas* value.

### Check ReplicaSet
```bash
kubectl get rs
---->
NAME               DESIRED   CURRENT   READY   AGE
nginx-7c5d8bf9f7   2         2         2       22h
```

>How it works? Kubernes checks *DESIRED STATE* (at the begining we had 1pod so kubernetes will create additionally 1pod to achive all pods in desired state.) **All pods are up and running simultaneously.**

### Pods traffic

In our case we have *NodePort* set. It works as a LoadBalancer -> **all incoming traffic evenly directed to all available pods.** It means in our case we have 2 pods one request may go to the first pod another to the second and so on.

### Perform a rolling update to a different image version.

First of all lets change the nginx version:
```yml
[...]
      containers:
      - image: nginx:1.29 #previous: nginx:latest
        name: nginx
[...]
```

After saving the deployment.yml lets apply the changes:
```bash
kubectl apply -f deployment.yml
```

To check the changes first we need to grab the pod name:
```bash
kubectl get pods -l app=nginx -o wide
---->
NAME                   READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
nginx-5b6f67b6-7985b   1/1     Running   0          63s   10.244.0.10   minikube   <none>           <none>
nginx-5b6f67b6-thdsv   1/1     Running   0          66s   10.244.0.9    minikube   <none>           <none>
```

Then we can check nginx version per pod:
```bash
kubectl describe pod nginx-5b6f67b6-7985b
---->
[...]
Image:          nginx:1.29
[...]
```

If the deployment is updated (i.e. new image version) Kubernetes will perform *rolling update*:
- it will create new pods with new image version one by one.
- it gradually removes old pods only when new ones are working properly.
This ensures that there is always a minimum number of pods available in the cluster and the application does not stop working.

### Rollback the update to the previous version

To rollback the changes we need to check the *rollout history*
```bash
kubectl rollout history deployment **<deployment-name>**
---->
deployment.apps/nginx 
REVISION  CHANGE-CAUSE
1         <none>
2         Switched to new nginx version
```

Right now we can perform the *rollback update:*
```bash
kubectl rollout undo deployment nginx --to-revision=**NUMBER OF REVISION**
---->
kubectl rollout undo deployment nginx --to-revision=1
---->
deployment.apps/nginx rolled back
```

Check the rollout status:
```bash
kubectl rollout status deployment nginx
---->
deployment "nginx" successfully rolled out
```
Then we can again check the nginx image version:
```bash
kubectl get pods -l app=nginx -o wide
---->
NAME                     READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES
nginx-7c5d8bf9f7-mskjf   1/1     Running   0          113s   10.244.0.11   minikube   <none>           <none>
nginx-7c5d8bf9f7-mtmlb   1/1     Running   0          108s   10.244.0.12   minikube   <none>           <none>
```

```bash
kubectl describe pod nginx-7c5d8bf9f7-mskjf
---->
[...]
Image:          nginx:latest
[...]
```

**The rollout won't change deployment.yml or service.yml files. Kubernetes takes this files only as a source of input, not as something that it must update or change later**

## Task 4 - Application Configuration (Secret and ConfigMap) [v]
- Create a ConfigMap containing some application configuration.
- Create a Secret with sensitive data.
- Run an application that reads values from both the ConfigMap and the Secret.
- Verify that the configuration is applied correctly (e.g., via environment variables or mounted files).

### Solution

First of all lets create a deployment without environmental variables:
```yml
###Task 4

apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodatabase
spec:
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:latest
        resources: {0}   
      - name: mongo_express
        image: mongo-express:latest
        resources: {0}      
```

Then we need to create a `configmap.yml` with some env variables:
```yml
config map:
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongodb
data:
  ME_CONFIG_BASICAUTH_ENABLED: "true"
```
`ConfigMap` is related with *POD* and not related with container. So that container could use `ConfigMap` we need to specify it at `env:` section in `deployment`.

To use configmap variables do the following:

```yml
      env:
          valueFrom:
            configMapKeyRef:
              name: mysql-configmap
              key: MYSQL_DATABASE
```

---
### Secrets
Kubernetes Secrets are objects used to store and manage sensitive information such as passwords, OAuth tokens, SSH keys, and API keys. The primary purpose of Secrets is to reduce the risk of exposing sensitive data while deploying applications on Kubernetes.

We need to encode all sensitive data to store in secret objects:
```bash
echo -n "root" | base64
---->
cm9vdA==
```

And then we can add secrets we can create `secret.yml:`

```yml
secret:
apiVersion: v1
kind: Secret
metadata:
  name: mongo-secrets
type: Opaque
data:
  ME_CONFIG_MONGODB_AUTH_DATABASE: ZGI= 
  ME_CONFIG_MONGODB_AUTH_USERNAME: cm9vdA==
  ME_CONFIG_MONGODB_AUTH_PASSWORD: bW9qZWhhc2xvMTIz

```

To use base64 encoded secrets we can add following to deployment.yml:
```yml
       env:
          - name: ME_CONFIG_MONGODB_AUTH_DATABASE
            valueFrom:
              secretKeyRef:
                name: mongo-secrets
                key: ME_CONFIG_MONGODB_AUTH_DATABASE
          - name: ME_CONFIG_MONGODB_AUTH_USERNAME
            valueFrom:
              secretKeyRef:
                name: mongo-secrets
                key: ME_CONFIG_MONGODB_AUTH_USERNAME
          - name: ME_CONFIG_MONGODB_AUTH_PASSWORD
            valueFrom:
              secretKeyRef:
                name: mongo-secrets
                key: ME_CONFIG_MONGODB_AUTH_PASSWORD
```

After that we need to apply all changes. Main sequence of applies:
```bash
kubectl apply -f mongo-secret.yml
kubectl apply -f mongo-configmap.yml
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

---

## Task 5 - Working with Volumes [v]

- Create a PersistentVolume using *hostPath*.
- Create a matching PersistentVolumeClaim.
- Attach the volume to a new Pod.
- Write a file inside the Pod and ensure it persists after restarting the Pod.

### Solution

We can use *hostPath* to create a local PersistentVolume. A *hostPath* volume mounts a file or directory from the host node's file system into pod.

| FEATURE                            | **hostPath**   | **storage-provisioner (dynamic PV)**|
| -----------------------------------| -------------------|:-------------------------------:|
| Where the data are stored ?        | In the node directory (VM Minikube or physical node)         | In the Minikube host directory (via provisioner), in a “safe” location that will survive a cluster restart
| Data durability (after pod restart)| ❌ No — VM/hostPath disappears          | ✅ Yes — the data is in the host directory and the PV is dynamically created. 
| Scalability                        | Weak — each node has its own catalog, it is difficult to connect several pods to one PV.        | Good — provisioner manages PV and you can easily create multiple PVCs
| Pros                               | Simple, quick to test | Safe, durable, closer to production
| Cons| Temporary in Minikube, susceptible to accidental deletion | A little more abstraction, requires addon/StorageClass

To avoid data loss I prefer to use *storage-provisioner* on Minikube.

Storage-provisioner installation:
```bash
minikube addons enable storage-provisioner
```
Then delete already created PV and PVCs:
```bash
kubectl delete pvc mongo-claim
kubectl delete pv local-pv-mongo
```

And we need only PVC (Claim) with `storageClassName: standard` :
```yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongo-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: standard
```

Minikube will automatically create a PV in the Minikube host directory (~/.minikube/...), which will survive a VM restart.



## Task 6 — Ingress [v]

- Install an Ingress Controller in Minikube.
- Expose the application from Task 2 using an Ingress.
- Configure a custom hostname and verify access through it.

---

### Solution

First of all we need to enable the *NGINX Ingress* controller:

```bash
minikube addons enable ingress
```

Verify that *Ingress* is running:

```bash
kubectl get pods -n ingress-nginx
---->
NAME                                       READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-6pxf4       0/1     Completed   0          5m20s
ingress-nginx-admission-patch-v9jzz        0/1     Completed   1          5m20s
ingress-nginx-controller-9cc49f96f-b82gm   1/1     Running     0          5m20s
```

Then we can deploy simple app (we're using deployment and service from Task2):
```yml
#deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 2 #previous: 1
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.29
        name: nginx
        resources: {}
status: {}
```
```yml
#service
service:
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30036
    protocol: TCP
```

Let's deploy our objects:

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

And check if the service is created and available on a node port:

```bash
kubectl get service nginx-service
---->
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
nginx-service   NodePort   10.104.37.162   <none>        80:30036/TCP   63s
```

Visit the service  via node port:

```bash
minikube service nginx-service
```
We can use web browser to see welcome page from nginx (http://192.168.49.2:30036)

Let's create an Ingress file:

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  labels:
    app.kubernetes.io/name: nginx-ingress
spec:
  rules:
  - host: local.example
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: nginx-service
            port: 
              number: 80
```

And apply the Ingress object:

```bash
kubectl apply -f ingress.yml
```

Let's verify the IP address:

```bash
kubectl get ingress
---->
NAME            CLASS   HOSTS           ADDRESS        PORTS   AGE
nginx-ingress   nginx   local.example   192.168.49.2   80      21m
```

Also we can add *local.example*  to an **/etc/hosts** file:

```bash
192.168.49.2  local.example
```
Then we can visit http://local.example to confirm ingress configuration!

## Task 7 — Multi-component Application[v]

- Prepare a 3-tier application: frontend, backend, and database.
- Run the frontend and backend using Deployments; run the database using a StatefulSet.
- Use a single ConfigMap and a single Secret for configuration.
- Expose the frontend using Ingress.

---

### Solution

**1. MySQL**

To achieve goal in this task first we need to create a MySQL deployment. Avoiding some mess in code let's create a namespace indicator for only this task.

```yml
#namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: triple-stack
```
Next we can use our *triple-stack* in the code:

```yml
#deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: triple-stack
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:latest
        resources: {}
```

Right now let's create *configMap* and *secrets* to provide all required variables to launch MySQL:

```yml
#secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secrets
  namespace: triple-stack
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: dGVzdHBhc3N3b3JkMTIzIQ==
  MYSQL_USER: bG9vc2Vy
  MYSQL_PASSWORD: bG9vc2VyMTIzIQ== 
```
```yml
#configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-configmap
  namespace: triple-stack
data:
  MYSQL_DATABASE: "maindb"
```

Then we need to create a *persistentVolume* for all MySQL data: login to the minikube and create dir for mysql data.

```bash
minikube ssh
---->
docker@minikube:~$ sudo mkdir -p /data/mysql
docker@minikube:~$ sudo chmod 777 /data/mysql
```
After creating the catalog in minikube host we can create *persistentVolume* and *persistentVolumeClaim* files:

```yml
#static-pv.yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
  namespace: triple-stack
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/mysql
```
```yml
#static-pvc.yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: triple-stack
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
```
Lastly we need to create *service* for MySQL:

```yml
#service.yml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: triple-stack
spec:
  selector:
    app: mysql
  ports:
  - port: 3306
```

We are ready to apply all codes.

> ⚠️ **Main apply sequence:**
> 1. Namespace.
> 2. Secret.
> 3. ConfigMap.
> 4. PersistentVolume.
> 5. PersistentVolumeClaim.
> 6. Deployment.
> 7. Service.

After applying all objects we need to check if it's working properly. When we set a namespace we need to add *-n [namespace]* to commands:
```bash
kubectl get pods -n triple-stack
---->
NAME                     READY   STATUS    RESTARTS   AGE
mysql-64bbbc5ff7-92v9v   1/1     Running   0          60s
```

Let's login to mysql (using our credentials in secrets.yml):
```bash
kubectl exec -it mysql-64bbbc5ff7-92v9v -n triple-stack -- mysql -u looser -p
---->
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 9.5.0 MySQL Community Server - GPL

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| maindb             |
| performance_schema |
+--------------------+
3 rows in set (0.016 sec)
```
Looks the MySQL is working properly!

**2. Backend**

We'll need to create a Dockerfile with some basic nodejs backend code:

```javascript
/*#backend/server.js*/
import express from "express";
import mysql from "mysql2/promise";

const app = express();

const dbConfig = {
  host: process.env.DB_HOST || "mysql-service",
  user: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE || "maindb",
  port: process.env.DB_PORT || 3306,
};

app.get("/health", async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.query("SELECT NOW() AS now");
    await connection.end();

    res.json({
      status: "ok",
      mysql_time: rows[0].now,
    });
  } catch (err) {
    res.status(500).json({
      status: "error",
      error: err.message,
    });
  }
});

app.listen(3000, "0.0.0.0", () => console.log("Backend działa na porcie 3000"));
```
```backend/package.json:```
```json
{
  "name": "minimal-backend",
  "version": "1.0.0",
  "main": "server.js",
  "type": "module",
  "dependencies": {
    "express": "^4.18.2",
    "mysql2": "^3.11.0"
  }
}
```
and finally we can create a `Dockerfile`:

```yml
#backend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

After all we need to build docker image:
```bash
docker build -t minimal-backend:1.0 .
```

and we are able to load image to minikube:
```bash
minikube image load minimal-backend:1.0
```
...and apply all K8s objects:
```bash
kubectl apply -f ./namespace.yml
kubectl apply -f ./secret.yml
kubectl apply -f ./configmap.yml
kubectl apply -f ./deployment.yml
kubectl apply -f ./service.yml
```

_Backend test:_
```bash
kubectl port-forward svc/backend-service 3000:3000 -n triple-stack
---->
Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000
Handling connection for 3000
```
```bash
curl http://localhost:3000/health
---->
{"status":"ok","mysql_time":"2025-12-12T12:34:48.000Z"}
```
MySQL+Backend working properly!


**3. Frontend**

To start working on frontend let's first create a frontend files:

```html
<!--frontend/index.html-->
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <title>3-tier app</title>
</head>
<body>
  <h1>Frontend działa</h1>
  <button onclick="checkBackend()">Sprawdź backend</button>
  <pre id="result"></pre>

<script>
  async function checkBackend() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      document.getElementById("result").textContent =
        JSON.stringify(data, null, 2);
    } catch (err) {
      document.getElementById("result").textContent =
        "Błąd: " + err;
    }
  }
</script>

</body>
</html>
```

```
#/frontend/nginx.conf
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend-service:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```yml
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/index.html

```

After all we need to build docker image:
```bash
docker build -t minimal-frontend:1.0 .
```

and we are able to load image to minikube:
```bash
minikube image load minimal-frontend:1.0
```
...and apply all K8s objects:
```bash
kubectl apply -f ./namespace.yml
kubectl apply -f ./secret.yml
kubectl apply -f ./configmap.yml
kubectl apply -f ./deployment.yml
kubectl apply -f ./service.yml
```

_Frontend test:_
```bash
minikube service frontend-service -n triple-stack
---->
┌──────────────┬──────────────────┬─────────────┬───────────────────────────┐
│  NAMESPACE   │       NAME       │ TARGET PORT │            URL            │
├──────────────┼──────────────────┼─────────────┼───────────────────────────┤
│ triple-stack │ frontend-service │ 80          │ http://192.168.49.2:30534 │
└──────────────┴──────────────────┴─────────────┴───────────────────────────┘
```

Let's open the browser and check:

![frontend-url](image.png)
---

## Task 8 — Horizontal Pod Autoscaler [v]

- Install and configure the metrics-server.
- Add an HPA to the application from Task 7.
- Generate load and verify that autoscaling works.

---

## Kubernetes Metrics Server

### Overview

Metrics Server is a lightweight, scalable service that provides container resource metrics to Kubernetes, primarily for autoscaling purposes.

It gathers resource usage information from Kubelets and exposes it through the Metrics API in the Kubernetes API server. This data can be used by Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA). Additionally, it enables `kubectl top` commands for easier debugging of autoscaling setups.

### Important Note

Metrics Server is designed exclusively for autoscaling. It should not be used as a source for monitoring systems. For external monitoring, metrics should be collected directly from the Kubelet `/metrics/resource` endpoint.

## Key Features

- Single deployment compatible with most clusters (see requirements).
- Metrics collection every 15 seconds for rapid autoscaling.
- Lightweight: consumes \~1 millicore of CPU and 2 MB of memory per node.
- Supports clusters up to 5,000 nodes.

## Use Cases

- CPU/Memory-based horizontal pod autoscaling.
- Resource adjustments and recommendations for containers using VPA.

## Limitations / When Not to Use

- Non-Kubernetes clusters.
- Reliable source for full resource usage metrics.
- Autoscaling based on resources other than CPU or memory.

For unsupported scenarios, consider using full monitoring solutions like Prometheus.

To install `mertics-server` run:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Then we can prepare yml file with HPA (Horizontal Pod Autoscaler):
```yml
#autoscaling.yml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-mysql-triple-stack
  namespace: triple-stack
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mysql
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 3 #3%
```
and need to add resource limits on our deployment:
```yml
#deployment.yml
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```
Let's apply the changes:
```bash
kubectl apply -f ./autoscaling.yml
kubectl apply -f ./deployment.yml
```
To check if HPA works properly we need to make some overload:

```bash
while true; do wget -q -O- http://192.168.49.2:30534; done
```
It's a while loop which will generate traffic to our frontend. Now we can check the HPA status:
```bash
kubectl get hpa -n triple-stack --watch
---->
NAME                        REFERENCE                   TARGETS             MINPODS   MAXPODS   REPLICAS   AGE
hpa-backend-triple-stack    Deployment/myapp-backend    cpu: 2%/5%          1         3         1          13m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 0%/5%          1         3         1          12m
hpa-mysql-triple-stack      Deployment/mysql            cpu: <unknown>/3%   1         3         1          15m
hpa-mysql-triple-stack      Deployment/mysql            cpu: 265%/3%        1         3         1          15m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 38%/5%         1         3         1          12m
hpa-backend-triple-stack    Deployment/myapp-backend    cpu: 1%/5%          1         3         1          13m
hpa-mysql-triple-stack      Deployment/mysql            cpu: 5%/3%          1         3         3          16m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 47%/5%         1         3         3          12m
hpa-mysql-triple-stack      Deployment/mysql            cpu: 4%/3%          1         3         3          16m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 21%/5%         1         3         3          12m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 23%/5%         1         3         3          13m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 2%/5%          1         3         3          13m
hpa-frontend-triple-stack   Deployment/myapp-frontend   cpu: 0%/5%          1         3         3          13m
```

As we can observe after peak of traffic the HPA created more replicas of our frontend service.

## Task 9 — Monitoring

- Install Prometheus + Grafana (e.g., using Helm).
- Configure a dashboard that monitors:
  - nodes,
  - pods,
  - CPU and RAM usage.

---

First of all we need to install Helm using apt:

```bash
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

after all above steps we should see output of helm version:
```bash
helm version
---->
version.BuildInfo{Version:"v3.19.3", GitCommit:"XXXX", GitTreeState:"clean", GoVersion:"go1.24.10"}
```

Once we have installed helm we can find proper helm charts using https://artifacthub.io/ (we need to find Prometheus) and then click "install":
![alt text](image-1.png)


There is a need to add prometheus repo:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
and install Prometheus chart:
```bash
helm install my-prometheus prometheus-community/prometheus --version 28.0.0
```
Once it's installed we can expand prometheus address by:
```bash
Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=my-local-prometheus" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 9090
```

and now we are able to visit Prometheus server -> http://127.0.0.1:9090

![alt text](image-2.png)


## Task 10 — Helm Charts and Custom values.yaml [v]

- Create your own Helm chart for a simple web application (e.g., Nginx).
- Use Helm templating in the manifests (Deployment and Service) so that key parameters (replica count, image version, Service type and port, container port) are driven from the values.yaml file.
- Prepare at least two custom values files:
  - `dev-values.yaml` – e.g., 2 replicas, image nginx:1.21, Service type NodePort.
  - `prod-values.yaml` – e.g., 5 replicas, image nginx:latest, Service type LoadBalancer, different port.
- Test the chart:
  - Render the manifests using `helm template` with each of the custom values files.
  - Install the chart in a Kubernetes cluster separately for dev and prod environments (in different namespaces), using the respective custom values files.
  - Verify that the resources were created according to the overridden values (replica count, Service type, image version, etc.).

### Solution:

1. To create an own Helm chart we can use below command:
```bash
helm create my-nginx-chart
```
It'll create a skeleton helm chart (with all files and dependencies).

2. Next we need to create the prod-values.yaml and preprod-values.yaml files for our purposes:
```yaml
#prod
replicaCount: 5

image:
  repository: nginx
  tag: "1.25"

service: 
  type: LoadBalancer
  port: 8080

containerPort: 80
```
```yaml
#preprod
replicaCount: 1

image:
  repository: nginx
  tag: "latest"

service: 
  type: NodePort
  port: 80
```

3. We can perform some checks before chart installation:

```bash
helm template my-release ./my-nginx-chart --values prod-values.yaml
---->

# Source: my-nginx-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-release-my-nginx-chart
  labels:
    helm.sh/chart: my-nginx-chart-0.1.0
    app.kubernetes.io/name: my-nginx-chart
    app.kubernetes.io/instance: my-release
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: my-nginx-chart
    app.kubernetes.io/instance: my-release
---
# Source: my-nginx-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-release-my-nginx-chart
  labels:
    helm.sh/chart: my-nginx-chart-0.1.0
    app.kubernetes.io/name: my-nginx-chart
    app.kubernetes.io/instance: my-release
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 5
  selector:
    matchLabels:
      app.kubernetes.io/name: my-nginx-chart
      app.kubernetes.io/instance: my-release
  template:
    metadata:
      labels:
        helm.sh/chart: my-nginx-chart-0.1.0
        app.kubernetes.io/name: my-nginx-chart
        app.kubernetes.io/instance: my-release
        app.kubernetes.io/version: "1.16.0"
        app.kubernetes.io/managed-by: Helm
    spec:
      serviceAccountName: my-release-my-nginx-chart
      containers:
        - name: my-nginx-chart
          image: "nginx:latest"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

4. After checks we can install chart:

```bash
helm install my-prod-nginx ./my-nginx-chart --values prod-values.yaml --namespace prod --create-namespace
---->
NAME: my-prod-nginx
LAST DEPLOYED: Wed Jan  7 15:28:08 2026
NAMESPACE: prod
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch its status by running 'kubectl get --namespace prod svc -w my-prod-nginx-my-nginx-chart'
  export SERVICE_IP=$(kubectl get svc --namespace prod my-prod-nginx-my-nginx-chart --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
  echo http://$SERVICE_IP:8080
```


# Task 11 — Kubernetes Jobs and CronJobs [v]

- Create a simple one-time **Job** and a **Job** with multiple completions (using `completions` + `parallelism`).
- Create a **CronJob** that runs on a schedule and executes a basic command.
- Observe behavior, statuses, logs, and automatic pod creation by Kubernetes.
- Learn how to clean up Jobs/CronJobs and their completed instances.

## Solution

### 1. Simple One-Time Job

Basic version with echo + sleep:

```yaml
# jobs.yml
apiVersion: batch/v1
kind: Job
metadata:
  name: busybox-job1
spec:
  template:
    spec:
      containers:
      - name: busybox-1
        image: busybox:latest
        command: ["/bin/sh", "-c", "echo 'Hello from Job!' && sleep 10"]
      restartPolicy: Never

Useful commands:
```bash
kubectl apply -f jobs.yml
kubectl get jobs -w
kubectl get pods -w
kubectl logs busybox-job1-xxxxx          # pod name from get pods
```

### 2. Job with Multiple Completions & Parallelism

```yaml
# jobs.yml (advanced version)
apiVersion: batch/v1
kind: Job
metadata:
  name: busybox-job1
spec:
  completions: 5           # must successfully complete 5 times
  parallelism: 2           # maximum 2 pods running at the same time
  backoffLimit: 4          # how many retries after failure (optional)
  template:
    spec:
      containers:
      - name: busybox-1
        image: busybox:latest
        command: ["/bin/sh", "-c", "echo 'exec number $((JOB_COMPLETION_INDEX+1)) of 5' && sleep 3"]
      restartPolicy: Never
```

**What happens?**

- 2 pods start at the same time (parallelism = 2)
- When one finishes → next one starts immediately
- In total you will see 5 completed pods numbered 1–5
---

### 3. CronJob - Daily / Periodic Execution

Simple example:
```yaml
# cronjobs.yml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: busybox-cronjob1
spec:
  schedule: "*/2 * * * *"     # every 2 minutes
  # schedule: "0 4 * * *"     # original: every day at 04:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            command:
            - /bin/sh
            - -c
            - date; echo "Hello from the Kubernetes cluster"
          restartPolicy: OnFailure
```

*Apply and observe:*
```bash
kubectl apply -f cronjobs.yml
kubectl get cronjobs
kubectl get jobs -w               # new Jobs appear according to schedule
kubectl get pods -w
kubectl logs busybox-cronjob1-1234567890-xxxxx
```