from langchain.text_splitter import RecursiveCharacterTextSplitter

file_path = "note_generator/text3.txt"  # Replace with your file path
CHUNK_SIZE = 20000 # Adjust based on transcript length and model limits
CHUNK_OVERLAP =250

try:
    with open(file_path, 'r') as file:
        file_content = file.read()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False
        )
    chunks = text_splitter.split_text(file_content)
    input_chunks = chunks


except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")