FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt


EXPOSE 5000


RUN pip install newrelic 
ENV NEW_RELIC_APP_NAME="entrega4" 
ENV NEW_RELIC_LOG=stdout 
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true 
ENV NEW_RELIC_LICENSE_KEY=d94cf34cb2bfa2a08793399acc19191fFFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info 
RUN echo $NEW_RELIC_LICENSE_KEY
ENTRYPOINT [ "newrelic-admin", "run-program", "python3", "src/main.py" ] 