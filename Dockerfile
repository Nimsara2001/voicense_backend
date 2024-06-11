FROM python:3.10-slim

WORKDIR /voicense

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install git -y

RUN pip install -r requirements.txt

RUN pip install git+https://github.com/openai/whisper.git

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
