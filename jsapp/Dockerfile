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

# ENV BUN_INSTALL=/root/.bun
# RUN echo 'export BUN_INSTALL=/root/.bun' >> /etc/profile.d/bun.sh && \
#     echo 'export PATH=$BUN_INSTALL/bin:$PATH' >> /etc/profile.d/bun.sh

# # Source the profile in every shell session
# SHELL ["/bin/bash", "-l", "-c"]
# RUN curl -o https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
# RUN source ~/.nvm/nvm.sh
# RUN nvm install 20
# RUN nvm alias default 20
# RUN nvm use 20


# WORKDIR /usr/src/app

# COPY package*.json ./
# COPY bun.lockb ./
# COPY . .

# RUN bun install
# RUN npm install --prefix frontend

# # run the app
# USER bun
# EXPOSE 80
# CMD [ "bun", "start" ]
CMD ["sh"]