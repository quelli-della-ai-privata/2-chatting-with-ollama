---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
color: 266089
html: true

---

![width:800px ](https://raw.githubusercontent.com/apache/openserverless/refs/heads/main/assets/logos/png/os-logo-full-horizontal-transparent.png)

# A chat application

### Developing a custom chat interface to Ollama

---
# Agenda

1. Connecting to Ollama
2. Login and Deploy
3. List models
4. A Simple Chat
5. Add Tests

## PLEASE USE THE DEVCONTAINER

---
# 1. Connecting to Ollama

```
read -s PASS
export URL=https://demo:$PASS@ollamatest.nuvolaris.io
````

- Ensure the URL is correct

```
curl $URL
````

- Save the password in `OLLAMA_API_HOST`

```
echo OLLAMA_URL=$URL >.env
```

---
# 2. Login and deploy

```
ops ide login devel http://miniops.me
ops ide deploy
ops  tools test
# default password is GPTmaster
```

## Change the passwords!
```
ops tools user demo --update
ops tools user admin --update
ops ide deploy mastrogpt/login
```


--- 

# 3. List models

- Use the CLI: `ops tools cli`
```python
args = {}
import os, requests
base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
!curl {base}
```

```python
url = f"{base}/api/tags"
!curl -s {url} | jq .
models = requests.get(url).json()
models
names = [ i.get("name") for i in models.get("models")]
names
```

---

# Create the action 

```
ops tools new models exercise
```

Login and Deploy

```shell
ops ide login devel http://miniops.me
ops ide deploy exercise/models
```

Run Tests

```
ops tests
```

---

# Write the `models` action

- Add in `__main__.py`: `#--param "OLLAMA_URL" "$OLLAMA_URL"`
- **Write Action Code**
- Add to the index
- Deploy `ops ide deploy`
- Invoke `ops invoke exercise/models`

---
# `models` blueprint

```python
def models(args):

  # get the url to access ollama models
  #TODO: models - get the url
  url = "???" 

  # list the models
  # TODO: models - get the models
  out =  "models"

  # return the output
  return {
    "output": out
  }
```

--- 
# 4. Let's chat with Ollama

```python
import os, requests
args = {}
base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
url = f"{base}/api/generate"
```

You require a post request: 

```python
MODEL = "llama3.1:8b"
PROMPT = "who are you"
msg = {"model":MODEL, "prompt": PROMPT, "stream": False}
res = requests.post(url, json=msg, stream=False).json()
res
print(res.get("response"))
```

---

# `chat` blueprint:

```python
def chat(args):
  # TODO: default message
  out = "chat"
  inp = args.get("input", "")
  if inp != "":
      # TODO: chat - get the url
      url = "???"
      # TODO: chat - prepare the message 
      msg = {}
      # TODO: chat - send the message ollama
      res = {}
      # TODO: chat: return the response
      out =  "???"
  return { "output": out}
```

---

# Exercise 1

- Modify models so you can see informations of a single model

# Exercise 2

- Modify the chat to be able to change model

