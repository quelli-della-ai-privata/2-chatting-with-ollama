import os, requests

def models(args):
  
  # url = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
  # if not url:
  url = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
  url_models = f"{url}/api/tags"

  # listo i mdels
  models = requests.get(url_models).json()
  names = [ i.get("name") for i in models.get("models")]
  out =  "\n".join(names)

  return {
    "output": out
  }
  