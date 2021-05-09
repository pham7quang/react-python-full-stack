# About this Project
The goal of this project is to provide a full stack coding example:
 * Frontend running React
 * Backend running Python with Flask/Flask-Restx
 * Kubernetes deployment

This project will be:
* Calling the Census API to obtain the data from https://www.census.gov/data/developers/data-sets/ase.html which contains the details from the survey sent to Business Owners in 2014-2016
* Transform the Census API to a REST API friendly format
* Host and provide a REST API to proxy and transform the calls to/from the Census API
* Cache the results of the Census API to reduce response time on subsequent calls
* Display the Census data in a Table on the browser

# Local Build
## Install the Tools
You'll need to install the necessary tools to get the project running, assuming you are using a Mac:
* Install Brew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
* For the frontend:
  * Install Node: `brew install node`
  * Install NVM to manage Node Versions: `brew install nvm`
  * Install Yarn: `npm install --global yarn`
* For the backend:
  * Install Python:  `brew install python`
  * Install pyenv to manage Python Versions: `brew install pyenv`
  * Install virtualenvwrapper, a virtual environment for the dependencies to be installed in: `pip install virtualenvwrapper`
* For the Local Kubernetes deployment:
  * Install Docker Desktop: https://www.docker.com/products/docker-desktop
  * Install `kubectl` for the Kubernetes command line tool: `brew install kubectl ` or check out https://kubernetes.io/docs/tasks/tools/
  * Install minikube on your Mac: `brew install minikube`. More details here if it the brew command or starting minikube fails: https://minikube.sigs.k8s.io/docs/start/

## Running the backend locally
To run the app locally, Python version >= 3.9.4 is needed. Use `pyenv` to install a later version if needed.

In the `backend/` folder run:
1. Start a virtual environment for this project: 
    1. `mkvirtualenv census-backend`
    1. `workon census-backend`
1. Install the dependencies: `pip install -r requirements.txt`
1. Sign up for a Census API Key: https://api.census.gov/data/key_signup.html
1. Go to the `settings.yaml` and update the value for  `CENSUS_API_KEY`
1. Start the backend server: `python3 main.py`
1. To check the Swagger API documentation use this url: http://localhost:5000/api

## Running the frontend locally
To run the app locally, node version >== 12.0.0 is needed. Use `nvm` to install a later version if needed.

In the `frontend/` folder run: 
1. `yarn install`
1. `yarn start`
1. Open http://localhost:3000/ to access the app


# Local Kubernetes deployment
## Kubernetes using minikube
Start Minikube and deploy the backend and frontend as a Deployment:
1. Start minikube with access to lower port numbers: `minikube start --extra-config=apiserver.service-node-port-range=1-10000`
1. Run `eval $(minikube docker-env)` to set the environment variables and allow local image builds to connect to minikube 
1. Add the deployments:
    1. Create the backend image: 
        1. Move to the `backend/` root directory 
        1. Run `docker build -t entrepreneur-backend:latest .`
    1. Create the frontend image: 
        1. Move to the `frontend/` root directory:
        1. Run `yarn build` to create the deployable build folder
        1. Run `docker build -t entrepreneur-frontend:latest .`
    1. Deploy both images to Minikube: 
        1. Move to the `kubernetes/` root folder 
        1. Run `kubectl apply -f deployment.yaml`
1. Expose the Loadbalancer to the local machine by running: `minikube tunnel`. NOTE: this command will have to be running to be able to access the site/APIs
1. To check the backend is up and running, check the backend swagger api docs via: http://localhost:5000/api
1. To check the frontend is up and running, access the site via : http://localhost:5080
1. If you want to see the running kubernetes components, run: `minikube dashboard`

Shut down the service:
1. Move to the `kubernetes/` folder
1. Run `kubectl delete -f deployment.yaml`
1. When finished, stop minikube: `minikube stop`

