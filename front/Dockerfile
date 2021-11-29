FROM nginx:1.14.0-alpine

WORKDIR code

COPY ./code/index.html /code

COPY ./nginx/nginx-front.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]


