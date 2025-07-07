#--kind python:default
#--web true
#--param OLLAMA_API_HOST "$OLLAMA_API_HOST"
#--param OLLAMA_CHAT_MODEL "$OLLAMA_CHAT_MODEL"

import chat
def main(args):
  return { "body": chat.chat(args) }
