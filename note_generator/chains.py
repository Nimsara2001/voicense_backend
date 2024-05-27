import os
from note_generator.prompts import promptM1,promptR1,promptTE
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser

# Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyANwPvr4Stl9iMnonsaRpeAScB5WSjMlkY"

model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

output_parser = StrOutputParser()

chain0 = promptTE | model | output_parser
chain1 = promptM1 | model | output_parser
chain2 = promptR1 | model | output_parser