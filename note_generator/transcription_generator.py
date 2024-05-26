import whisper

from note_generator.optimizer import optimize_note

model = whisper.load_model("base.en")


def get_transcription():
    print("Transcribing audio")
    result = model.transcribe("resources/audio.mp3", fp16=False)
    with open('resources/transcription.txt', 'w') as f:
        f.write(result["text"])
    print("Transcription complete")
    optimize_note("Python FastAPI")
    print("Note optimized")
