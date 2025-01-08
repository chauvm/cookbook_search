# cookbook_search
SearchService for cookbook project

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
- Quick start on indexing a document and perform simple search: https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
    -  By `console`, the guide means console of Kibana which looks like this:
      ![image](https://github.com/user-attachments/assets/7aaca52f-4936-438a-b14f-cc9c2c209a18)


