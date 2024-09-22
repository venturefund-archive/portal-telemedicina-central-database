FROM node:18.19-alpine

WORKDIR /app

COPY . .
RUN npm install
RUN npm install @vuepress/bundler-vite@^2.0.0-rc.15

EXPOSE 8002

CMD ["npm", "run", "docs:dev"]