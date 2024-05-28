from note_generator.prompts import create_cohesive_prompt
from note_generator.chains import chain1, chain2, chain0
from note_generator.read_file import get_input_chunks


def optimize_note(transcription):
    previous_answer = ""
    complete_response = ""
    overall_topic = get_overall_topic(transcription)
    k = 1

    input_chunks = get_input_chunks(transcription)

    for chunk in input_chunks:
        cohesive_prompt = create_cohesive_prompt(chunk, overall_topic)
        response = chain1.invoke(
            {"con": cohesive_prompt, "overall_topic": overall_topic, "previous_answer": previous_answer})
        # print(response)
        complete_response = complete_response + response
        print(k)
        k = k + 1
        previous_answer = response

    # print(complete_response)
    print("starting invoking chain 2..")

    final_answer = chain2.invoke({"domain": complete_response})

    return final_answer


def get_overall_topic(transcription):
    print("starting topic generation...")
    topic = chain0.invoke({"transcript": transcription})
    print(topic)
    return topic
