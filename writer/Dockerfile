FROM python:latest

COPY ./rabbtreader /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV host "127.0.0.1"
ENV port "5672"
ENV postgreshost "localhost"
ENV postgresport "5432"
EXPOSE $port
ENV username "guest"
ENV pass "guest"
CMD python3 -u main.py $host $port $username $pass $postgreshost $postgresport
