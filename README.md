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
# default password is GPTmaster

```
## Change the passwords!
`ops tools user demo --update`
`ops tools user admin --update`

--- 

# 2. List models

- Use the CLI: `ops tools cli`
```python
args = {}
import os, requests
base = args.get("OLLAMA_URL", os.getenv("OLLAMA_URL"))
!curl {base}
```

```python
url = f"{base}/api/tags"
!curl {url} | jq .
models = requests.get(url).json()
models
names = [ i.get("name") for i in models.get("models")]
names
```

---

# Create the action and pass the secrets

```
!ops tools new models exercise
```

Add in `__main__.py`

```shell
#--param "OLLAMA_URL" "$OLLAMA_URL"
```

Note that if you deploy:

```shell
ops ide login devel http://miniops.me
ops ide deploy ollama/models
```

there is the option `--param OLLAMA_URL "$OLLAMA_URL"`

---

# Write the `models` action

- Create Action
`ops tools new models exercise`
- Write Action Code
- Add to the index
- Deploy `ops ide deploy`
- Invoke `ops invoke exercise/models`

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
