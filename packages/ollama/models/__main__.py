#--kind python:default
#--web true
#--param OLLAMA_URL "$OLLAMA_URL"
import models
def main(args):
  return { "body": models.models(args) }
