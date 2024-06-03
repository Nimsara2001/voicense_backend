import whisper
from secrets import token_hex
import os

model = whisper.load_model("base.en")


async def save_audio(file):
    try:
        file_ext = file.filename.split('.')[-1]

        if file_ext not in ['wav', 'mp3', 'flac', "m4a"]:
            return {"message": "failed", "details": "Invalid file type. Please upload an audio file."}

        file_name = token_hex(8)

        os.makedirs("resources/audio", exist_ok=True)

        file_path = f"resources/audio/{file_name}.{file_ext}"

        with open(file_path, 'wb') as f:
            f.write(file.file.read())

        return {"message": "success", "path": file_path}

    except AttributeError:
        return {"message": "failed", "details": "The file object does not have the expected attributes."}
    except IOError:
        return {"message": "failed", "details": "An error occurred while trying to write the file."}


async def generate_transcription(path):
    try:
        result = model.transcribe(path, fp16=False)
        return {"message": "success", "result": result["text"]}

    except Exception as e:

        return {"message": "failed", "details": str(e)}


async def delete_audio(path):
    try:
        os.remove(path)
        print("File deleted successfully.")
        return {"message": "success"}
    except FileNotFoundError:
        return {"message": "failed", "details": "The file does not exist."}
    except Exception as e:
        return {"message": "failed", "details": str(e)}
