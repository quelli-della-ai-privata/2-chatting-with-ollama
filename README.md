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

# MastroGPT starter kit 

### Build your serverless Private AI applications


---
# Agenda
1. Install `ops`
2. Install `miniops.me`
3. Deploy locally the starter kit on `miniops.me`
4. Configure Ollama
5. Change passwords
6. Deploy the starter kit in production

---

# Install `ops`, the CLI

## Linux/Mac

# `curl -sL bit.ly/get-ops | bash`

## Windows

## `powershell -c "irm bit.ly/get-ops-exe | iex"`

---

# Install  `miniops.me`, the local server

## 1. Dowload **Docker Desktop**

## 2. `ops setup mini`

## That's it. Really.
#### Just be patient as it can take several minutes to install.

--- 

# Deploy the starter kit

## 1. `ops ide login devel http://miniops.me`

### Password is in `.ops/devel.password` in your home

## 2. `ops ide deploy`

### This will deploy the starter kit

## 3. `http://devel.miniops.me`

### Default with `admin/GPTmaster`

---

# Configure an Ollama server

### `ops env add OLLAMA_API_HOST=<url>`
If you have a local Ollama use: 

#### `http://host.docker.internal:11434`

#### Repeat the login to pick the secrets and  redeploy

```
ops ide login devel http://miniops.me
ops ide deploy
```

---
# Change the passwords

```
# list the user
ops tools user
# update the user password
ops tools user admin --update
# also demo and chat
```

## Redeploy the login action

### `ops ide deploy mastrogpt/login`

---
# Deploy in production

You need an account on a production server

```
$ ops ide login
*** Configuring Access to OpenServerless ***
Enter Apihost: https://nuvolaris.org
Enter Username: qdaip
Enter Password: 
Successfully logged in as qdaip.
ok: whisk auth set. Run 'wsk property get --auth' to see the new value.
ok: whisk API host set to https://nuvolaris.org
OpenServerless host and auth set successfully. You are now ready to use ops!
````
Assuming Ollama is configured, `https://qdaip.nuvolaris.org`