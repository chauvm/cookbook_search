# cookbook_search
SearchService for cookbook project

## Build, start and run Cookbook search gRPC server with kubernetes
- Create the docker image named `tcc-cookbook-search`: `docker build . -t tcc-cookbook-search`
    - Valicate the Docker image by `docker image ls`, you should see the image we've just created
- Deploy the service:
    - Apply the deployment: `kubectl apply -f k8/deployments/deployment.yaml`
    - Apply the service: `kubectl apply -f k8/service/service.yaml`
- We now have the deployed service, let's verify:
    - Verify the deployment: `kubectl get deployments -n cookbook-search`
    - Check the pods are running: `kubectl get pods -n cookbook-search`
    - Verify the service `kubectl get services -n cookbook-search`
- To run the service and access it locally: `kubectl port-forward service/cookbook-search-service 50051:50051 -n cookbook-search`
- Run the client script to test the connection: `python3 -m src.ping_pong_client`


## Setup Elastic Search server on Kubernetes
- Install Docker Desktop
- Setup k8s by Turn on Kubernetes on docker desktop https://docs.docker.com/desktop/kubernetes/
- Install these utilities for k8s: https://github.com/chauvm/techcare_onboarding/wiki/Kubernetes 
- Install k8s CRDs and Operator (pre-requisite for elastic search): https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions 
    - (Notes) There are 2 basic steps here: install CRS and install operator with its RBAC rule - just follow the link above
    - Once finished, you can check the elastic system namespace:
      ![kubectl get -n elastic-system pods](https://github.com/user-attachments/assets/79c56c3c-19e0-4505-9278-3ce699adc339)
    - Or run `kubectl describe crd elasticsearch`    
- Deploy a simple elastic search cluster: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html 
    - The operator automatically creates and manages Kubernetes resources after successful instalment:
      ![kind Elasticsearch](https://github.com/user-attachments/assets/5b0e7128-38ad-4a2e-9747-78a40828dee0)
    - To run Kubernetes locally: In a separate terminal, port-forward elastic search `kubectl port-forward service/quickstart-es-http 9200`
- Then deploy a kibana instance: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-kibana.html
    - Kibana is the UI client for us to interact with elastic search and can be accessed via a browser
    - To run Kibana locally: in a separate terminal, port-forward it `kubectl port-forward service/quickstart-kb-http 5601`
- Then you can go to `localhost:5601` to access Kibana and interact with elastic search
- Default credentials to use elastic search can be found in this [guide](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html) , look for the `Get the credentials.` part
- Quick start on indexing a document and perform simple search: https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
    -  By `console`, the guide means console of Kibana which looks like this:
      ![image](https://github.com/user-attachments/assets/42598351-303e-4343-82ad-58d06d48b83a)



