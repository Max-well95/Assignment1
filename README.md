1.Enter the webserver dirctory and build the Docker image:
```bash
docker build -t webserver .
```

2. Run the Docker image:
```bash
docker container run -p 5000:5000 -d webserver

3.Enter the webserver dirctory and build the Docker image:
```bash
docker build -t loadbalancer .
```

4. Run the Docker image:
```bash
docker container run -p 5000:5000 -d loadbalancer
