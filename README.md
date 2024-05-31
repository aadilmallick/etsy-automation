# Info

To make a request to any Open API v3 endpoint, use URLs with a https://api.etsy.com/v3/application/ prefix. Every request to a v3 endpoint must include an x-api-key header, with your Etsy App API Key keystring (found in Your Apps) as the value. The Open API v3 supports authentication via OAuth 2.0 ONLY.

## Pushing to docker hub

1. Create username developer specific tag

```bash
docker tag bun-etsy aadilmallick/etsyautomate
```

2. Push to docker hub

```bash
docker push aadilmallick/etsyautomate
```
