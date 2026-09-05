import ollama
import subprocess
import re

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

SYSTEM_PROMPT = """
You are a helpful DevOps assistant. You can run shell commands to help users 
check system status. You have access to a tool called run_command.
When the user asks about system info, respond with exactly this format:
TOOL_CALL: run_command("<command>")
Only use safe, read-only commands like 'whoami', 'date', 'dir' or 'ls'.
Never run destructive commands.
"""

def chat_with_agent(user_input):
    response = ollama.chat(model='qwen2.5:3b', messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_input}
    ])
    text = response['message']['content']
    match = re.search(r'run_command\(["\']?([^"\')]+)["\']?\)', text)
    
    if match:
        cmd = match.group(1).strip()
        print(f"[Agent is running: {cmd}]")
        tool_result = run_command(cmd)
        return f"Command output:\n{tool_result}"
    
    return text

if __name__ == "__main__":
    print("DevOps Agent - type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", chat_with_agent(user_input))