import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Variables to store student data
intended_major = "Computer Science"  # Example data
career_goals = "Software Developer"
learning_style = "Hands-on learning"
interests_hobbies = "Gaming, AI, Programming"

# Data to send to OpenAI
data = f"""
major: {intended_major}
career goal: {career_goals}
learning style: {learning_style}
interests/hobbies: {interests_hobbies}
"""

# Question for GPT, including the instruction for JSON format response
question = """
Generate a personalized learning path for a Penn State student based off the user data provided.
Respond in the following JSON format:
{
    "position": "<Position Name>",
    "description": "<Brief description of the position>",
    "skills": [
        "<Skills needed for the position>",
    ],
    "learning_style": "<Best fit style of learning for this position>"
}
"""

def query_gpt(data, question):
    # Combine data and question into a single prompt
    prompt = f"{data}\n{question}"
    
    # Make the API call to OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates learning paths."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjust max tokens based on your needs
            temperature=0.7  # Control the randomness of the output
        )
        
        # Extract the assistant's response
        completion_text = completion.choices[0].message.content
        
        # Return the JSON response (assuming the response is in JSON format)
        try:
            return json.loads(completion_text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response.", "response": completion_text}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Call the query method
response = query_gpt(data, question)

# Print the response in JSON format
response_json = json.dumps(response, indent=4)
print(response_json)