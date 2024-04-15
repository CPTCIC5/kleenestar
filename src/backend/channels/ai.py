from dotenv import load_dotenv
from openai import OpenAI
from channels.models import Convo
from django.shortcuts import get_object_or_404

load_dotenv()

client = OpenAI()




def get_convo_prompts(convo:int):
    get_convo= get_object_or_404(Convo,id=convo)
    history = get_convo.prompt_set.all()
    return history
    
def send_history(convo_id:int):
    history = get_convo_prompts(convo_id)
    if history.count() >= 1:
        history_list = []
        for i in history:
            history_list.append(i.text_query)
        return str(history_list)
    else:
        return False



def generate_insights_with_gpt4(user_query:str,convo:int):
    # Creating a new conversation thread
    thread = client.beta.threads.create()

    # Posting user's query as a message in the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )

    # Initiating a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_wljmLStVyrLtU7AyxcyXlU7d"
    )
    print(run.instructions)


    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")
            break

    # Retrieve messages added by the Assistant to the thread
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Print the messages from the user and the assistant
    print("###################################################### \n")
    print(f"USER: {message.content[0].text.value}")
    print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")