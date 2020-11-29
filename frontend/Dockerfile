# pull official base image
FROM node:13.12.0-alpine

WORKDIR /app

COPY frontend/frontend/package.json /app/package.json
COPY frontend/frontend/package-lock.json /app/package-lock.json

RUN npm install
RUN npm install react-scripts -g
RUN npm install swagger-ui
RUN npm install swagger-ui-react

COPY frontend/frontend/ /app/

CMD ["npm", "start"]