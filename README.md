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

### Develop a chat application connecting to Ollama

---
# Agenda

1. Connecting to Ollama
2. List models
3. Simple Chat
4. Add streaming

---
# 1. Connecting to Ollama

- Ensure the OLLAMA_API_HOST is correct

```
read -s PASS
export URL=https://demo:$PASS@ollamatest.nuvolaris.io
curl $URL
```

- Connecting to Ollama

```
ops ide login devel http://miniops.me
echo OLLAMA_URL=$URL >.env
```
--- 

# 2. List models

```python
import os, requests
args = {}
url = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
!curl {url}
url_models = f"{url}/api/tags"
!curl {url_models} | jq .
models = requests.get(url_models).json()
names = [ i.get("name") for i in models.get("models")]
```
---

# Create the action and pass the secrets

```
ops tools new models ollama
```

Add in `__main__.py`

```shell
#--param "OLLAMA_URL" "$OLLAMA_URL"
```

Note that if you deploy:

```
ops ide deploy ollama/models
```

there is the option `--param OLLAMA_URL "$OLLAMA_URL"`

---

# Deploy the `models` action

- Create Action
`ops tools new models ollama`
- Write Action Code
- Add to the index
- Deploy `ops ide deploy`
- Invoke `ops invoke ollama/models`

---

# Exercise

- Modify the `models` so you can:
   - Read the input (`args.get("input")`)
   - Show all the informations of a model selected by input

--- 
# 3. Let's chat with Ollama

```python
import os, requests
args = {}
url = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
url_generate = f"{url}/api/generate"
```

You require a post request: 

```python
MODEL = "llama3.1:8b"
PROMPT = "who are you"
msg = {"model":MODEL, "prompt": PROMPT, "stream": False}
res = requests.post(url_generate, json=msg, stream=False).json()
res
print(res.get("response"))
```

---

# Chat action blueprint

- read `input`
- invoke ollama
- return `output`

---

# Exercise

Implement the tests!

- test_models
- test_models_int
- test_chat
- test_chat_int
