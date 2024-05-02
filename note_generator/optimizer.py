from db_config import get_db
from note_generator.prompts import create_cohesive_prompt
from note_generator.chains import chain1, chain2
from note_generator.read_file import get_input_chunks


def optimize_note(content_topic):
    previous_answer = ""
    complete_response = ""
    overall_topic = content_topic
    k = 1

    input_chunks = get_input_chunks()

    for chunk in input_chunks:
        cohesive_prompt = create_cohesive_prompt(chunk, overall_topic)
        response = chain1.invoke(
            {"con": cohesive_prompt, "overall_topic": overall_topic, "previous_answer": previous_answer})
        print(response)
        complete_response = complete_response + response
        print(k)
        k = k + 1
        previous_answer = response

    # print(complete_response)

    final_answer = chain2.invoke({"domain": complete_response})

    # Save the note to the database
    db = get_db()
    db.testnote.insert_one({"note": final_answer})

    return final_answer
