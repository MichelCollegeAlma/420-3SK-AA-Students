FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir flask==3.0.0
COPY app.py .
EXPOSE 5000
CMD ["python","app.py"]
