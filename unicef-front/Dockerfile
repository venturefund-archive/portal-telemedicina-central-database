FROM node:14.20-alpine as develop-stage

WORKDIR /app

COPY ./package.json /app
COPY ./package-lock.json /app

COPY . .

RUN npm install

RUN npm run build

# production stage
# FROM nginx:alpine as production-stage
# COPY --from=build-stage /app/dist /usr/share/nginx/html

# CMD ["nginx", "-g", "daemon off;"]
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
