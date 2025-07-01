#--kind python:default
#--web true
#--param OLLAMA_API_HOST $OLLAMA_API_HOST
import chat
def main(args):
  return { "body": chat.chat(args) }
