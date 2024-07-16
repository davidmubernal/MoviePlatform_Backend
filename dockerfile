FROM python:alpine3.19
COPY requirements /opt/requirements
RUN pip install -r /opt/requirements
VOLUME [ "/app" ]
CMD [ "/app/entrypoint.sh" ]