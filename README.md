Enter the webserver dirctory and build the Docker image:
```bash
docker build -t webserver .
```

3. Run the Docker image:
```bash
docker container run -p 5000:5000 -d webserver
