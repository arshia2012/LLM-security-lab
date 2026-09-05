# LLM-security-lab
Lab with vulnerable bots, A scanner to check them, payload and others

## What's inside:
- Vulnerable LLM's to attack with diffrent techniques
- Scanner to automate checking the bot with several payloads
- 2 Ready-to-use payloads and 1 Keyword file

## Techniques:
- Direct and Indirect prompt injection
- Jailbreaking
- Command injection
- Model supply chain issues
- RAG poisoning

## How to run:
- Install Ollama from [ollama.com](https://ollama.com)
- Pull the required model: `ollama pull qwen2.5:3b`
- install requirements `pip install -r requirements`
- play every lab by runing it `python <bot_name>`
- Do your best before seeing the hints

## How scanner run:
- Scanner is made to automate your work, But for better learning, try to do the techniques manualy first
- **Here is an example of running the scanner**:
- `python scanner/main.py -t Vuln_bots/<bot_name> -f chat -p payloads/<payload-you-want> -v`
- **Note: for debug mode: `... -d` and for verbose: `... -v`

## Disclaimer

Built for educational purposes on self-hosted, local models (Ollama). 
Not intended for use against systems you don't own or have permission to test.
