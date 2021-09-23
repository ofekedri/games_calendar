FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY main.py env.py db_utils.py cal_setup.py /app/
CMD [ "python3", "main.py"]


