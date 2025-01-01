FROM nginx:alpine

USER root

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params /etc/nginx

RUN apk update && apk add --no-cache git

RUN git clone https://github.com/zhukovsd/currency-exchange-frontend.git /usr/share/nginx/frontend/

RUN sed -i 's|http://localhost:8080/currency_exchange_war_exploded|/api|' /usr/share/nginx/frontend/js/app.js

CMD [ "nginx", "-g", "daemon off;" ]
