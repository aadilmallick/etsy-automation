docker build -t bun-etsy .
docker run -p 3015:80 --rm bun-etsy