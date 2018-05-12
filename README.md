# Hjalp

## Usage

```
docker-compose build --no-cache
docker-compose up -d

curl -d '{"state":"online", "latitude":0, "longitude":0}' -H "Content-Type: application/json" -X POST http://localhost:4011/track -v
curl -d '{"latitude":0, "longitude":0}' -H "Content-Type: application/json" -X POST http://localhost:4031/dispatch -v
```
