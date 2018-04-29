# Hjalp

```
docker run -p 6379:6379 redis 
python3 -m pip install -r requirements.txt
curl -d '{"state":"online", "latitude":0, "longitude":0}' -H "Content-Type: application/json" -X POST http://localhost:5000/track -v
curl -v localhost:5001
```
