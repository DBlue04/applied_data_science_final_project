# Virtual MC Quiz Game

🎙️ **An interactive quiz game powered by AI, featuring text-to-speech and live chat capabilities.**

---

## 📌 Overview

This project combines a FastAPI-powered web application with a local F5-TTS server and the nyagpt-qwen2-7b-v0.1 model to create an engaging quiz experience. Users can participate in a quiz where questions are read aloud, and they can interact with a witty MC through live chat.

---

## ⚙️ Components

1. **F5-TTS API**: Converts text to speech using a local server.
2. **Web Application**: Serves the quiz interface and handles user interactions.
3. **nyagpt-qwen2-7b-v0.1 Model**: Generates AI-driven responses for the MC.

---

## 🛠️ Setup & Deployment

### 1. Clone the Repository


```bash
https://github.com/DBlue04/applied_data_science_final_project.git
cd virtual_mc_quiz
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate #on Mac device
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Deploy F5-TTS API
```bash
cd f5-tts
uvicorn server:app --host 0.0.0.0 --port 7860
```

### 5. Deploy Web Application
```bash
cd ..
uvicorn main:app --reload
```

## 🧠 Model Configuration
Ensure the ```nyagpt-qwen2-7b-v0.1``` model is accessible at ```http://192.168.1.106:1234``` by activating this model on LM Studio.

## 📁 Project Structure
```
virtual_mc2/
│
├── llm/
│   ├── __pycache__/
│   ├── __init__.py
│   └── lm_client.py
│
├── static/
│   ├── audio/             
│   ├── answer.js
│   └── quiz.js
│
├── templates/
│   ├── answer_feedback.html
│   ├── base.html
│   ├── index.html
│   └── quiz.html
│
├── tts/
│   ├── __pycache__/
│   └── local_f5/          
│		├── check.py
│		├── config.yaml
│		├── generate_audio.py
│		├── output.wav
│		├── server.py
├── main.py
└── requirements.txt
```

## 📄 requirements.txt
```
fastapi==0.95.2
uvicorn==0.22.0
requests==2.31.0
jinja2==3.1.2
torch==2.1.0
torchaudio==2.1.0
transformers==4.31.0
f5-tts==1.1.0
f5-tts-mlx==0.2.6
einops==0.6.1
einx==0.0.1
huggingface_hub==0.15.0
jieba==2.1.1
mlx==0.18.1
numpy==1.25.0
pypinyin==0.48.0
setuptools==67.6.1
sounddevice==0.4.6
soundfile==0.12.1
tqdm==4.65.0
vocos-mlx==0.1.0
```

## 🎮 Usage
1. Navigate to http://localhost:8000 to start the quiz.

2. Answer questions to receive feedback from the AI-powered MC.

3. Use the chat feature to interact with the MC during the quiz.

## 🧪 Testing
To test the F5-TTS API:​

```bash
curl -X 'POST' \
  'http://localhost:7860/tts' \
  -H 'accept: audio/wav' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello, this is a test."
}'
```
To test the web application, navigate to http://localhost:8000 in your browser.

## 🔗 References
[FastAPI Documentation](https://fastapi.tiangolo.com/)

[F5-TTS Server](https://github.com/ValyrianTech/F5-TTS_server)

[nyagpt-qwen2-7b-v0.1](Vtuber-plan/nyagpt-qwen2-7b-v0.1-gguf-q8_0)
