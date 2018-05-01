# Hjalp

```
docker run -d -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
docker run -d -p 6379:6379 redis
python3 -m pip install -r requirements.txt
curl -d '{"state":"online", "latitude":0, "longitude":0}' -H "Content-Type: application/json" -X POST http://localhost:4001/track -v
curl -v localhost:5001
```
