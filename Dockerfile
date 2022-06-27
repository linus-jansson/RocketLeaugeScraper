FROM python:3.10.5-alpine3.16
RUN pip3 install fake_headers requests
COPY main.py /
ENTRYPOINT ["python3", "/main.py"]
