import whisper

model = whisper.load_model("base.en")


def get_transcription():
    print("Transcribing audio")
    result2 = model.transcribe("note_generator/test.mp3")
    print(result2["text"])
    return {result2["text"]}
