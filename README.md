# Voice AI API – Documentation

This documentation provides clear instructions to build, Dockerize, test, and deploy the Speech AI application.

---

## Project Overview

This project is a **Flask-based API** providing:

1. **Speech-to-Text (STT)** using **OpenAI Whisper**.
2. **Text-to-Speech (TTS)** using **gTTS (Google Text-to-Speech)**.

---

## Project Structure

```
speech-ai-app/
├── app.py
├── Dockerfile
├── requirements.txt
├── uploads/         # Auto-created for audio file uploads
└── outputs/         # Auto-created for generated TTS files
```

---

## Prerequisites

* Install **Docker**: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
* Install **Postman** for API testing: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

---

## Dockerizing the Application

### 1. Create `requirements.txt`

```plaintext
Flask
whisper
torch
gTTS
```

### 2. Create `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5040

CMD ["python", "app.py"]
```

---

## Building Docker Image (Single Architecture)

```bash
docker build -t speech-ai-app:latest .
```

### Run Locally:

```bash
docker run -p 5040:5040 speech-ai-app:latest
```

### Test Locally in Postman:

* **Health Check:**
  `GET` → `http://localhost:5040/health` → Should return `OK`

* **Speech-to-Text:**
  `POST` → `http://localhost:5040/api/speech-to-text`

  * Set **Body → form-data**
  * Key: `audio` → Choose File (.wav file)

* **Text-to-Speech:**
  `POST` → `http://localhost:5040/api/text-to-speech`

  * Body: **raw** → **JSON**:

  ```json
  {
    "text": "Hello, this is a test speech"
  }
  ```

  * The response will be an MP3 file download.

---

## Building Multi-Architecture Image (amd64 + arm64)

### Step 1: Create and Use Buildx Builder (if not already)

```bash
docker buildx create --use
```

### Step 2: Build & Push Multi-Arch Image:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ranga2024/speech-ai-app:latest --push .
```

This ensures your image works on both Intel/AMD and ARM architectures (like Apple M1, Raspberry Pi, etc.).

---

## Pulling and Running from Docker Hub

### Step 1: Pull Image

```bash
docker pull ranga2024/speech-ai-app:latest
```

### Step 2: Run the Container

```bash
docker run -p 5040:5040 ranga2024/speech-ai-app:latest
```

Test in Postman exactly as described earlier.

---

## Full Local Testing Flow (Summary)

| Step           | Command/Action                                                                                              |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| Build          | `docker build -t speech-ai-app:latest .`                                                                    |
| Run            | `docker run -p 5040:5040 speech-ai-app:latest`                                                              |
| Health Check   | `GET` [http://localhost:5040/health](http://localhost:5040/health)                                          |
| Speech-to-Text | `POST` [http://localhost:5040/api/speech-to-text](http://localhost:5040/api/speech-to-text) with audio file |
| Text-to-Speech | `POST` [http://localhost:5040/api/text-to-speech](http://localhost:5040/api/text-to-speech) with JSON body  |

---

## Pushing to Docker Hub

### Step 1: Tag (if not using same name):

```bash
docker tag speech-ai-app:latest ranga2024/speech-ai-app:latest
```

### Step 2: Push:

```bash
docker push ranga2024/speech-ai-app:latest
```

---

## Pull & Test Anywhere (Including Servers)

```bash
docker pull ranga2024/speech-ai-app:latest
docker run -p 5040:5040 ranga2024/speech-ai-app:latest
```

Test via Postman using `<your-server-ip>:5040` in place of `localhost`.

---

## Azure Deployment

*Refer to the Youtube Channel, Do it as guided!.*


