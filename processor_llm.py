from dotenv import load_dotenv
from groq import Groq
load_dotenv()

groq = Groq()
def classify_with_llm(log_msg):
    prompt = f'''Classify the log message into one of these categories:
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, return "Unclassified". 
    Only return the category name. No preamble
    Log message: {log_msg}'''
    chat_completion = groq.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages =[
            {
                "role": "user",
                "content":prompt,
            }
        ])
    return chat_completion.choices[0].message.content
