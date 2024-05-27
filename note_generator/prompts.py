from langchain.prompts import PromptTemplate


def create_cohesive_prompt(chunk, overall_topic):
    prompt = (f"This transcript is a timestamped raw transcription of a lecture on {overall_topic}."
              f" Use this transcription to extract information as much as possible from it. "
              f"Then generate a note using every last bit of extracted information transcription starts now.{chunk}")
    return prompt


promptM1 = PromptTemplate(
    input_variables=['con', 'overall_topic'],
    template="This transcript is a raw transcription of a lecture on {overall_topic}. Identify the key points, main ideas, and all subject relevant details, including but not limited to: definitions, derivations, proofs, examples, and counter-examples. Include any mathematical equations mentioned in the transcription (e.g., differential, integral, algebraic equations) and special functions mentioned in the lecture. Ensure Clarity: Explain concepts clearly and concisely and Define technical terms where necessary.Transcript: {con}"
)

promptR1 = PromptTemplate(
    input_variables=['domain'],
    template="These are notes created from a different parts of a same lecture on {domain}. Your task is to join these notes into one big note.but do not brief the content. just join them accordinglsy, organize them and keep the flow. Add equations and tables when necessary. Ensure the resulting document is well-organized.word count should be around 1500 and in MD format"
)

promptTE = PromptTemplate(
    input_variables=['transcript'],
    template="This trancription is a raw transcription is a raw transcription of some particular topic {transcript}. based on the transcription, guess the broader topic of the discussion and return only that topic name"
)