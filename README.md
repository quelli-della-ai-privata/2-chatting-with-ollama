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

# Deploy the list models

- Create Action
`ops tools new models ollama`
- Write Action Code
- Add to the index
- Deploy
`ops ide deploy`
- Invoke
`ops invoke ollama/models`