FROM python:alpine3.19
COPY requirements /opt/requirements
RUN pip install -r /opt/requirements
VOLUME [ "/app" ]
CMD ["uvicorn",  "src.api:app",  "--host",  "0.0.0.0",  "--port",  "8000"]