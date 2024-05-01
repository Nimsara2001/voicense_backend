import whisper

model = whisper.load_model("base.en")


def get_transcription():
    print("Transcribing audio")
    result2 = model.transcribe("note_generator/array_jenny.mp3", fp16=False)
    print(result2["text"])
    return {result2["text"]}
