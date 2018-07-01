# TwitterAPI

<h4>HowTo:</h4>

1. Need to run Arangodb in docker (example):
```
sudo docker run -ti -p 8529:8529 -e ARANGO_ROOT_PASSWORD=123456 arangodb
```
2. Get ID of the container contain ArangoDB:
```
sudo docker ps 
```
3. Get IP of the container
```
sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER_ID
```
4. Build local image
```
sudo docker build -t twitterapi .
```
5. Run app (Change DBIP, if you need it):
```
sudo docker run -p 5000:5000 -ti -e DBIP=172.17.0.2 -e DBPORT=8529 -e DBUSER=root -e DBPASSWORD=123456 twitterapi:latest
```
6. URLs (example):
```
http://172.17.0.3:5000/proximity/user_id_0/user_id_1
http://172.17.0.3:5000/friendship/user_id_0/user_id_1
```
7. Curl request (optional):
```
curl -X GET -d "user_a=user_id_0&user_b=user_id_1" appIP:PORT/friendship
```
