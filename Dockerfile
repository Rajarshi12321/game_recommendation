FROM python:3.10-slim

WORKDIR /app

COPY . /app


RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

ARG GOOGLE_API_KEY1
ENV GOOGLE_API_KEY=$GOOGLE_API_KEY1

ARG LANGCHAIN_API_KEY1
ENV LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY1

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]