from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 20000  # Adjust based on transcript length and model limits
CHUNK_OVERLAP = 250


def get_input_chunks(transcription):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False
        )

        chunks = text_splitter.split_text(transcription)
        return chunks
    except:
        print("An error occurred while trying to split the text.")
