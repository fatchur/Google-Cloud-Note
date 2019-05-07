FROM python:3.6
WORKDIR /app
COPY . /app
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--timeout", "7000"]
