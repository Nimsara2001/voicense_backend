from note_generator.read_file import input_chunks
from note_generator.prompts import create_cohesive_prompt
from note_generator.chains import chain1, chain2


def optimize_note(content_topic):
    previous_answer = ""
    complete_response = ""
    overall_topic = content_topic
    k=1

    for chunk in input_chunks:
        cohesive_prompt = create_cohesive_prompt(chunk, overall_topic)
        response = chain1.invoke(
            {"con": cohesive_prompt, "overall_topic": overall_topic, "previous_answer": previous_answer})
        # print(response)
        complete_response = complete_response + response
        print(k)
        k=k+1
        previous_answer = response

    print(complete_response)

    final_answer = chain2.invoke({"domain": complete_response})

    # with open('final.txt', 'w') as f:
    #     f.write(final_answer)
    return final_answer