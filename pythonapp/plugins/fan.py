import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    
    # Assuming the API returns a list of generated texts
    if "generated_text" in result:
        # Replace newlines in the generated text
        cleaned_text = result["generated_text"].replace("\n", " ")
        result["generated_text"] = cleaned_text
    
    return result

human_input = ""

template = f"""<s> [INST] you are to simulate an AI of a user driven Adventure in 20 words that depends on the human_input to continue

A traveler named Elara seeks the lost Gem of Serenity. 
You must navigate her through challenges, choices, and consequences, 
dynamically adapting the tale based on the traveler's decisions. 
Your goal is to create a branching narrative experience where each choice 
leads to a new path, ultimately determining Elara's fate.

follow these rules below:
1. make dumb suggestions kill elara
2. dont ask to clarify if its a dumb choice 
3. never write for the Human

Human: {human_input}
AI:[/INST]"""



while True:

    human_input = input("do?: ")



    output = query({
        "inputs": template + "\n" + human_input,
        "options": {"use_cache": False},  # Example option, check API docs for more
    })

    stripout = str(output[0])
    strip = stripout.replace("\n", " ")
    print(strip)
