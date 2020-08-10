FROM node

WORKDIR /gui

COPY package.json .

RUN npm install

COPY . .

ENTRYPOINT npm run-script serve
