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

"""
def generate_instructions(user_query, image=None):
    # Simplified intent detection logic
    if "how to improve" in user_query.lower():
        analysis_type = "database_analysis"
    elif image and "analyze this image" in user_query.lower():
        analysis_type = "image_and_database_analysis"
    elif image:
        analysis_type = "image_analysis"
    else:
        analysis_type = "general_knowledge"

    # Generate prompt for GPT-4 based on the analysis type
    if analysis_type == "database_analysis":
        prompt = "Analyze the user's marketing channel data to provide insights on improving their strategy."
    elif analysis_type == "image_and_database_analysis":
        prompt = "Analyze the provided image and the user's marketing channel data to offer branding insights."
    elif analysis_type == "image_analysis":
        prompt = "Analyze the provided image to offer branding insights."
    else:  # general_knowledge
        prompt = "Provide marketing and branding insights based on general knowledge."

    return prompt, analysis_type
"""

def get_convo(convo):
    get_convo= get_object_or_404(Convo,id=convo)
    history = get_convo.prompt_set.all()
    if history.count() >= 1:
        history_list = []
        for i in history:
            history_list.append(i.text_query)
        return str(history_list)
    else:
        return False


def generate_instructions(user_query,convo_id,image=None):
    convo = get_convo(convo_id)
    #fetch = base(user_query,image)
    if not image:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Use the correct identifier for GPT-4
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}, 
                {'role':'system', "content": convo},
                #{"role": "system", "content": fetch["analysis_type"]},
                #{"role" : "user", "content":fetch["prompt"]},
                {"role":"user", "content": user_query}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        insights = response.choices[0].message
        return insights.content.strip()
    else:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",  # Use the correct identifier for GPT-4
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}, 
                {'role':'system', "content": convo},
                #{"role": "system", "content": fetch["analysis_type"]},
                #{"role" : "user", "content":fetch["prompt"]},
                {"role":"user", "content": user_query},
                {'role':'user','content':image}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        insights = response.choices[0].message
        return insights.content.strip()


def generate_insights_with_gpt4(query,convo_id,image=None):
    if image is None:
        data_for_analysis = generate_instructions(query,convo_id)
        prompt_for_gpt4 = f"{query}\\n\\n{data_for_analysis}"

        response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "user", "content": prompt_for_gpt4}
                    ],
                max_tokens=1000,
                temperature=0.5
        )
        return response.choices[0].message.content.strip()
    else:
        data_for_analysis = generate_instructions(query,convo_id,image)
        prompt_for_gpt4 = f"{query}\\n\\n{data_for_analysis}"

        response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[{"role": "user", "content": prompt_for_gpt4}],
                max_tokens=1000,
                temperature=0.5,
        )
        return response.choices[0].message.content.strip()