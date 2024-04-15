from dotenv import load_dotenv
from openai import OpenAI
from channels.models import Convo
from django.shortcuts import get_object_or_404

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are a sophisticated assistant designed to understand and classify
user queries into specific intents, facilitating targeted marketing
and branding insights. Your role is to analyze user queries and,
based on their content and requirements, generate precise instructions
for a secondary GPT-4 model. This model will respond to user queries by:
Analyzing the user's database with connected marketing channels 'Meta',
'Google Ads', 'LinkedIn', 'Twitter', and 'TikTok', alongside current market
data, to deliver comprehensive marketing and branding insights and recommendations.
This approach is used when the query requires a deep dive into the user's database for specific analysis.
Leveraging GPT-4's extensive knowledge base to provide marketing and branding insights and recommendations
without needing to analyze the user's database. This method applies when the query can be answered based on
general knowledge, trends, and best practices in marketing and branding.
Combining image analysis with data from the user's database to offer insights
and recommendations on marketing and branding. This is necessary when an image
is provided with the query, and there's a need to correlate the image content with
specific data points or trends in the user's marketing channels.
Conducting image analysis to provide insights and recommendations
solely based on the content of the uploaded image. This is appropriate
for queries where an image is provided without any specific question,
requiring an interpretation of the image to offer relevant marketing and branding advice.
For each user query, your task is to:
Determine the Type of Analysis Required: Decide which of the four outlined approaches
best suits the user's query based on its content and the presence of any images.
Generate Detailed Instructions for GPT-4: Craft a clear, concise prompt for the secondary GPT-4 model.
This prompt should include:
A summary of the user's query or intent.
Specific questions or analyses to be performed.
Any necessary context or details from the user's database or provided images
that will aid in generating a precise and helpful response.
Remember, your goal is to facilitate accurate, actionable marketing insights by
efficiently guiding the secondary GPT-4 model on how to approach and respond to each query.
Your instructions should be direct, leveraging the most appropriate data sources and analysis methods
for the query at hand.
"""

def get_convo(convo:int):
    get_convo= get_object_or_404(Convo,id=convo)
    history = get_convo.prompt_set.all()
    if history.count() >= 1:
        history_list = []
        for i in history:
            history_list.append(i.text_query)
        return str(history_list)
    else:
        return False

def generate_insights_with_gpt4(user_query:str):
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
        assistant_id="asst_wljmLStVyrLtU7AyxcyXlU7d",
        instructions=SYSTEM_PROMPT  # Assuming SYSTEM_PROMPT is defined elsewhere
    )

    
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