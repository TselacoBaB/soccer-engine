FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY services ./services
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["uvicorn","services.api.app.main:app","--host","0.0.0.0","--port","8000"]
