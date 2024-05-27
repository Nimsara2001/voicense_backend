import whisper

from note_generator.optimizer import optimize_note,get_overall_topic

model = whisper.load_model("base.en")


def get_transcription():
    print("Transcribing audio")
    result = model.transcribe("resources/audio.mp3", fp16=False)
    with open('resources/transcription.txt', 'w') as f:
        f.write(result["text"])
    print("Transcription complete")
    content_topic = get_overall_topic()
    optimize_note(content_topic)
    print("Note optimized")
