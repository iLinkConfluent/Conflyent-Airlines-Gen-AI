FROM python:3.11
RUN pwd
COPY chat_app /src/chat_app
RUN ls
ADD requirements.txt /src/
RUN ls 
RUN pip install -r src/requirements.txt
WORKDIR /src/chat_app
CMD ["python", "./consumer.py"]
