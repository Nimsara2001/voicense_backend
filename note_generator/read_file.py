from langchain.text_splitter import RecursiveCharacterTextSplitter

file_path = "resources/transcription.txt"
CHUNK_SIZE = 20000  # Adjust based on transcript length and model limits
CHUNK_OVERLAP = 250


def get_input_chunks():
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                length_function=len,
                is_separator_regex=False
            )
        print(file_content)
        chunks = text_splitter.split_text(file_content)
        return chunks

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_file_content(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        return file_content

def get_file_path():
    return file_path