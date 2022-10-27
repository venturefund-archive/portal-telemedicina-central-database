FROM node:alpine as develop-stage

WORKDIR /app

COPY ./package.json /app
COPY ./package-lock.json /app

RUN npm install

COPY ./ /app
RUN npm run build

# production stage
# FROM nginx:alpine as production-stage
# COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 90
# CMD ["nginx", "-g", "daemon off;"]
CMD ["npm", "run", "dev"]
