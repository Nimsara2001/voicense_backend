import whisper
from secrets import token_hex
import os

model = whisper.load_model("base.en")


async def save_audio(file):
    try:
        file_ext = file.filename.split('.')[-1]
        if file_ext not in ['wav', 'mp3', 'flac', "m4a"]:
            print("Invalid file type. Please upload an audio file.")
            return None
        file_name = token_hex(8)
        file_path = f"resources/audio/{file_name}.{file_ext}"
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        print("File saved successfully.")
        return {"message": "success", "path": file_path}
    except AttributeError:
        return {"message": "failed", "details": "The file object does not have the expected attributes."}
    except IOError:
        return {"message": "failed", "details": "An error occurred while trying to write the file."}


async def generate_transcription(path):
    try:
        result = model.transcribe(path, fp16=False)
        print("Transcription generated successfully.")

        return {"message":"success","result":result["text"]}
    except Exception as e:
        # Return a message indicating that an error occurred
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
