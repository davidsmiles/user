name=user-service
docker build -t ${name} .
docker run -d -p 5000:5000 -v $PWD:/app --name ${name} ${name}