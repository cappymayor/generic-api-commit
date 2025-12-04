FROM python:3.9.25-slim-trixie

WORKDIR /data_directory

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY war_data_extractor.py .

CMD ["python3", "war_data_extractor.py"]
