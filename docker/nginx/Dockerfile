FROM nginx:alpine

USER root

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params /etc/nginx

RUN apk update

COPY ./frontend /usr/share/nginx/frontend/

CMD [ "nginx", "-g", "daemon off;" ]
