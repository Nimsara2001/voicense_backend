import whisper

from note_generator.optimizer import optimize_note
from secrets import token_hex


# def get_transcription():
#     print("Transcribing audio")
#     result = model.transcribe("resources/audio.mp3", fp16=False)
#     with open('resources/transcription.txt', 'w') as f:
#         f.write(result["text"])
#     print("Transcription complete")
#     optimize_note("Python FastAPI")
#     print("Note optimized")


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
        return {"message": "success", "path": file_path}
    except AttributeError:
        return {"message": "failed", "details": "The file object does not have the expected attributes."}
    except IOError:
        return {"message": "failed", "details": "An error occurred while trying to write the file."}


async def generate_transcription(path):
    model = whisper.load_model("base.en")
    result = model.transcribe(path, fp16=False)
    with open('resources/transcription.txt', 'w') as f:
        f.write(result["text"])
    return result["text"]
