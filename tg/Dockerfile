FROM python:3.11-alpine
# Alpine is a lightweight Linux distribution

WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
# RUN apk add g++ libpq-dev python3-dev gcc musl-dev libffi-dev
COPY ./tg/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache --upgrade

# Now copy in our code, and run it
COPY . /app
CMD ["python3", "tg/main.py"]