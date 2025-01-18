This repository contains a simple chat application that demonstrates the use of Docker, Kubernetes,
CI/CD, and a basic API.
Setup and Run Locally
---------------------
Build the Docker Container:
1. Clone this repository to your local machine.
$ git clone git@github.com:sree7979/syndio-chat-app.git
$ cd chat-app
2. Build the Docker container:
$ docker build -t your-dockerhub-username/chat-app .
3. Run the Docker container locally:
$ docker run -p 8000:8000 your-dockerhub-username/chat-app
Environment Variables:
The application uses the following environment variables:
- APP_SECRET_KEY: Secret key for the application.
- DATABASE_URL: URL for the database connection (if applicable).
You can set these in a .env file or pass them directly via Docker or Kubernetes.
Kubernetes Deployment
----------------------
To deploy the application to a Kubernetes cluster:
1. Ensure Kubernetes is set up on your machine or cloud environment.
2. Apply the deployment and service manifests:
$ kubectl apply -f deployment.yaml
$ kubectl apply -f service.yaml
3. Check the deployment status:
$ kubectl get pods
$ kubectl get services
4. Access the application via the external IP:
$ kubectl get services
API Contract
------------
- GET /docs: Displays the API documentation.
- POST /chat: Send a message to the chat application.
Request body:
{ "message": "Hello" }
Response:
{ "response": "Hi there!" }
CI/CD
-----
A basic CI/CD pipeline is set up using GitHub Actions and shell scripts.

CI/CD Process:
1. On each push to the main branch, GitHub Actions will automatically build the Docker image, push
it to DockerHub, and deploy it to the Kubernetes cluster.
2. A shell script (scripts/ci-cd-pipeline.sh) is included to automate the process.
Known Limitations and Future Improvements
-----------------------------------------
- The current version is a basic implementation without advanced error handling and logging.
- The app can be scaled to use a database and store messages persistently.
- Additional features such as user authentication and real-time messaging (via WebSockets) can be
added in the future.
