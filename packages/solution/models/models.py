import os, requests

def models(args):
  
  # get the url to access ollama models
  base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
  url = f"{base}/api/tags"

  # list the models
  models = requests.get(url).json()
  names = [ i.get("name") for i in models.get("models")]
  out =  "\n".join(names)

  # return the output
  return {
    "output": out
  }
  