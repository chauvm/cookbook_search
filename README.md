# cookbook_search
SearchService for cookbook project

## Build, start and run Cookbook search gRPC server with kubernetes
- Create the docker image named `tcc-cookbook-search`: `docker build . -t tcc-cookbook-search`
    - Validate the Docker image by `docker image ls`, you should see the image we've just created
- Deploy the service:
    - Apply the deployment: `kubectl apply -f k8s/deployments/deployment.yaml`
    - Apply the service: `kubectl apply -f k8s/service/service.yaml`
- We now have the deployed service, let's verify:
    - Verify the deployment: `kubectl get deployments -n cookbook-search`
    - Check the pods are running: `kubectl get pods -n cookbook-search`
    - Verify the service `kubectl get services -n cookbook-search`
- To run the service and access it locally, run this in a separate terminal from the root of this app directory: `kubectl port-forward service/cookbook-search-service 50051:50051 -n cookbook-search`
    - Example of a successfully deployed service running:
<img width="637" alt="image" src="https://github.com/user-attachments/assets/9a1064b0-1ee6-47c4-b4a0-86ffc323e8a8" />

- Run the client script to test the connection: `python3 -m src.client.client`. We will not use this file in production, this is just to test if the server is running and responding.
    - If both server and client work, the client will print out:
```
❯ python3 -m src.client.client
Received from server: Pong: Hello, Server!
```
And server will print out (upon client sending request to it):
```
kubectl port-forward service/cookbook-search-service 50051:50051 -n cookbook-search
Forwarding from 127.0.0.1:50051 -> 50051
Forwarding from [::1]:50051 -> 50051
Handling connection for 50051
```

## Setup Elastic Search server on Kubernetes
- Install Docker Desktop
- Setup k8s by Turn on Kubernetes on docker desktop https://docs.docker.com/desktop/kubernetes/
- Install these utilities for k8s: https://github.com/chauvm/techcare_onboarding/wiki/Kubernetes 
- Install k8s CRDs and Operator (pre-requisite for elastic search): https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart
    - (Notes) There are 2 basic steps here: install CRS and install operator with its RBAC rule - just follow the link above
    - Specifically, you can run these 2 commands : 
    ```bash
    kubectl create -f https://download.elastic.co/downloads/eck/3.0.0/crds.yaml
    kubectl apply -f https://download.elastic.co/downloads/eck/3.0.0/operator.yaml
    ```
    - Once finished, you can check the elastic system namespace:
      ![kubectl get -n elastic-system pods](https://github.com/user-attachments/assets/79c56c3c-19e0-4505-9278-3ce699adc339)
    - Or run `kubectl describe crd elasticsearch`    
- Deploy a simple elastic search cluster: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html 
    - The operator automatically creates and manages Kubernetes resources after successful instalment:
      ![kind Elasticsearch](https://github.com/user-attachments/assets/5b0e7128-38ad-4a2e-9747-78a40828dee0)
    - To run Kubernetes locally: In a separate terminal, port-forward elastic search 
    `kubectl port-forward service/quickstart-es-http 9200`
- Then deploy a kibana instance: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-kibana.html
    - Kibana is the UI client for us to interact with elastic search and can be accessed via a browser
    - To run Kibana locally: in a separate terminal, port-forward it `kubectl port-forward service/quickstart-kb-http 5601`
- Then you can go to `localhost:5601` to access Kibana and interact with elastic search
- Default credentials to use elastic search can be found in this [guide](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html) , look for the `Get the credentials.` part
- Quick start on indexing a document and perform simple search: https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
    -  By `console`, the guide means console of Kibana which looks like this:
      ![image](https://github.com/user-attachments/assets/42598351-303e-4343-82ad-58d06d48b83a)



## Notes on cleaning up containers if you need to remove and rebuild a new one
- Get the docker image id associate with `tcc-cookbook-search`: `docker image ls`
- For example, if the docker image ID is `73a81f3c01a9`, to remove containers created from a Docker image with ID `73a81f3c01a9` and created by Kubernetes using kubectl apply deployment.yaml, follow these steps:
    - Delete the k8s deployment: `kubectl delete -f k8/deployments/deployment.yaml`
        - If you don't have access to the deployment.yaml file, you can delete the deployment by its name. To get the deployment name of this cookbook search namespace: `kubectl get deployments -n cookbook-search` - the deployment name of this app is `cookbook-search-deployment` ( you can check it in `k8s/deployement/deployment.yaml`)
        - And then delete the deployment: `kubectl delete deployment <deployment-name>` , replace `<deployment-name>` with the actual name of your deployment
    - Remove docker container: `docker rm $(docker ps -a -q --filter ancestor=73a81f3c01a9)`
    - After executing these commands, both the Docker containers and the Kubernetes deployment associated.with the specified image will be removed. Then you can delete the docker image by `docker image rm <image-id>`
