FROM python:3.10-slim

WORKDIR /voicense

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install git -y

RUN pip install -r requirements.txt

RUN pip install git+https://github.com/openai/whisper.git

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

RUN mkdir -p resources/audio

EXPOSE 8000

VOLUME ["D:/voicense_volume:/resources/audio"]

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]