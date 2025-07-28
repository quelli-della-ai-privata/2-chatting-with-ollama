#--kind python:default
#--web true
#--param OLLAMA_URL "$OLLAMA_URL"

import chat
def main(args):
  return { "body": chat.chat(args) }
