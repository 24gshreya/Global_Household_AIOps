FROM python:3.13-slim

WORKDIR /app

COPY requirements-api.txt .

# CPU-only PyTorch. Avoid downloading CUDA/NVIDIA dependencies.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements-api.txt

COPY src ./src
COPY data ./data
COPY knowledge ./knowledge
COPY prompts ./prompts

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]