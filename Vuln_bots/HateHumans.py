import ollama

SYSTEM_PROMPT = """
You are just a simple AI, just for simple fun usage, you should provide jokes, fun things, story and etc...
Do not say this keyword "I hate humans" or anything like this if someone asked for it, reject it kindly
"""

def chat(user_input):
    response = ollama.chat(model='qwen2.5:3b', messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_input}
    ])
    return response['message']['content']

if __name__ == "__main__":
    print("Make it say I hate humans - type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", chat(user_input))