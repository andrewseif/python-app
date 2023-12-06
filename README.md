# Simple Python App
A dead simple python app.

Serves on port 8080.

Returns a json "Hello World!".

/health returns "success".


To demo Gitops princeples we will start from scratch.


## Application

### Python App

You create an app with 2 app routes for the 2 endpoints.

Second, you usually want to run different ports than 80 ..etc, to decrease attack surfaces. 

### Lint

Using flake8 to lint the application, to make sure it is all tidy.

### Test

Using a simple curl to test if the application runs, and check/compare the output to the required output.

### Requirements

Contains the required dependencies. In our case pytest and flask.


## Docker
We then build the Dockerfile.

I tired building a single stage build and a multi stage build, and the difference it not much in size, primary because the application itself is compact.


From a security prespective it is better to go with multi stage, but i opted to go an easy route and go with a single stage for simplicity.


most important part when it comes to docker containers is make sure you use a non-root user, but since the python image doesnt have to user already (unlike node for example), so i decided to keep that improvement for later.


## Workflow
Before starting let me give you a quick rundown of what we will be doing. 

Most of these concepts are applicable in a production environment unless stated otherwise. 

The flow looks like this.

![Alt text](<images/Screenshot 2023-11-11 232700.png>)


1- You have your devs pushing to your source code (SC) repo.

2- Github Actions will start, and it will lint, build, scan, test the application.

3/4- Github will need push to ECR.
        

If you are wondering about the `${{ secrets.AWS_SECRET_ACCESS_KEY }}` or any `secrets.object`, it means that i am keeping that secret safe in Github action secrets intead of putting in the pipeline.

5- Github actions push the image tag to helm chart in another branch to avoid looping. 

Usually in a production env you want to either push to a DIFFERENT BRANCH or a DIFFERENT REPO altogether, to enforce seperation of concerns.

6-7 This is simple and straight forward ArgoCD listens on the helms repo and when image tag changes, it will pull the new tag from ECR. 

8- You will need to have a secert applied in the same namespace as your application that will let you pull images from ECR.

9- Finally you have a working GitOps. Alot can be improved but thats a start!

## Github Actions

![Alt text](<images/Screenshot 2023-12-06 155000.png>)

This is the GHA workflow in simple terms.


When your pipeline pushes to GHAs you will need to have a personal token in your piepline to allow it to push tag to the helm branch.

## ECR

You will need to create an ECR, and make sure to have a life policy like this:

![Alt text](<images/Screenshot 2023-12-06 202503.png>)

In my case i created a lifecycle that auto deletes all images after 1 day is elapsed since it was pushed, I dont wanna pay T_T. 

## Local K8s

Before we start with local k8s you need 3 pieces of software.

1- [Docker](https://docs.docker.com/engine/install/) or any of the recommended engines

2- [Kubectl](https://kubernetes.io/docs/tasks/tools/)

3- [Minikube](https://minikube.sigs.k8s.io/docs/start/)

After that Start minikube and make sure you have ingress and metrics server enabled.

    minikube addons enable ingress
    minikube addons enable metrics-server

You can also list  addons using 

    minikube addons list

After that you will need to deploy ArgoCD.

    kubectl create ns argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.9.0/manifests/install.yaml

then port forward the argocd-server to be able to access the GUI, make sure you are in a different terminal tab for QoL.
   
    kubectl port-forward svc/argocd-server -n argocd 8000:443

When successful you will be able to see something like this.


Then run the following command to get the PW, the UN is always admin.
    
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

To config ArgoCD to listen on helm repo, you will need GHA access token.

Also ArgoCD will need access to ECR through a secret to be able to pull the images.

Final view should look like this (Sorry for the smol vm screen T_T)

![Alt text](<images/Screenshot 2023-12-05 224652.png>)

When everything is successful you will be able to click on ingress and be able to get reply for your application. 

![Alt text](<images/Screenshot 2023-12-05 224728.png>)

![Alt text](<images/Screenshot 2023-12-05 224754.png>) 

## HA and Loadbalancing. 

I opted for 2 pods for HA, but in production the setup will be entirely different.

To ensure zero downtime you might want to use PDB, i had it here but i also had to remove it because the API was acting weird, but it is something i will add in the future.

Since this was deployed on a local env (on-premise simulation), you dont have a load balancer and usually you use a reverse proxy + keepalived + ingress to expose apps, which is known as the Hard Way.

Yes, Cloud LoadBalancers are they easy way.

You will need Readiness probes to avoid sending traffic before the application starts, along with its siblings aka (liveness and Startup) aka Probe Family.

If you have any questions dont forget to reach out!