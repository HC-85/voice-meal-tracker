# syntax=docker/dockerfile:1
FROM huggingface/transformers-pytorch-gpu
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
RUN apt install -y sqlite3
#RUN chmod +x logging_/idx_logging.sh
#RUN chmod +x logging_/init_db.sh