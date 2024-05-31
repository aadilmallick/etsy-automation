FROM node:20-alpine

RUN apk update
RUN apk add bash
RUN apk add curl
# automatically types in Y when prompted to install nano
RUN echo Y | apk add nano  

# essential code to get bun working properly on alpine linux
RUN apk --no-cache add ca-certificates wget
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.28-r0/glibc-2.28-r0.apk
RUN apk add --no-cache --force-overwrite glibc-2.28-r0.apk

RUN npm install -g bun

WORKDIR /usr/src/app

COPY package*.json ./
COPY bun.lockb ./

RUN bun install

COPY . .
RUN npm install --prefix frontend



# run the app
EXPOSE 80
CMD [ "bun", "start" ]
# CMD ["sh"]