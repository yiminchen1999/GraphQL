# Build Part
FROM python:3.9-slim as builder
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --user -r requirements.txt
COPY . /app

# Run Part
FROM python:3.9-slim as runner
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
# This will not be overriden when docker-compose call command label
ENTRYPOINT uvicorn main:app --reload
# This will be overriden when docker-compose call command label
CMD [ "--port","8000","--host","0.0.0.0" ]