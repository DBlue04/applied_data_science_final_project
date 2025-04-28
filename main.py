from typing import Optional
import os, time, requests

from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import (
    HTMLResponse, FileResponse, RedirectResponse, JSONResponse
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from llm.lm_client import get_llm_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

TTS_API_URL = "http://localhost:7860/tts"

def generate_and_save_audio(text: str, folder: str, filename: str) -> None:
    """Call F5-TTS once, cache the WAV under static/audio/{folder}/."""
    out_dir = os.path.join("static", "audio", folder)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        return
    r = requests.post(TTS_API_URL, json={"text": text})
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)

questions = [
    {"question": "Who wrote 'Romeo and Juliet'?",
     "options": ["Shakespeare", "Dickens", "Austen", "Hemingway"],
     "answer": "Shakespeare"},
    {"question": "Tallest mountain in the world?",
     "options": ["Everest", "K2", "Kangchenjunga", "Makalu"],
     "answer": "Everest"},
    {"question": "Land of the Rising Sun?",
     "options": ["China", "Korea", "Japan", "India"],
     "answer": "Japan"},
    {"question": "Largest planet?",
     "options": ["Earth", "Jupiter", "Saturn", "Neptune"],
     "answer": "Jupiter"},
    {"question": "Chemical symbol for water?",
     "options": ["H2O", "O2", "CO2", "HO"],
     "answer": "H2O"},
]

# ─────────────────────────────── intro clip ──────────────────────────── #
@app.on_event("startup")
def _intro() -> None:
    intro = ("Welcome to the Quiz Game! I'll ask five questions; "
             "after each answer I'll cheer or tease. Ready? Let's go!")
    generate_and_save_audio(intro, "intro", "intro.wav")

# ─────────────────────────────── routes ──────────────────────────────── #
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/quiz/{qid}", response_class=HTMLResponse)
async def quiz(request: Request, qid: int):
    if not (0 <= qid < len(questions)):
        return RedirectResponse("/")
    q = questions[qid]
    generate_and_save_audio(q["question"], "question", f"question_{qid+1}.wav")
    return templates.TemplateResponse(
        "quiz.html",
        {"request": request,
         "question_id": qid,
         "question":   q["question"],
         "options":    q["options"],
         # no automatic banter on the question page
         "comment_prompt": "", "comment_reply": "", "comment_wav": ""}
    )

@app.post("/quiz/{qid}/answer", response_class=HTMLResponse)
async def check_answer(
    request: Request,
    qid: int,
    selected_option: Optional[str] = Form(None),
):
    if not (0 <= qid < len(questions)):
        return RedirectResponse("/")

    q = questions[qid]

    # ---------- result sentence + WAV ---------------------------------- #
    if selected_option is None:
        result_text = f"Time's up! The correct answer was {q['answer']}."
    else:
        result_text = (
            "Correct!"
            if selected_option == q["answer"]
            else f"Incorrect. The correct answer was {q['answer']}."
        )
    generate_and_save_audio(result_text, "result", f"result_{qid+1}.wav")

    # ---------- NO extra banter generation here ------------------------ #
    # We pass empty strings so the front-end falls back to the latest
    # /chat reply cached in localStorage (audio lives in static/audio/chat/)
    return templates.TemplateResponse(
        "answer_feedback.html",
        {
            "request":        request,
            "question_id":    qid,
            "next_id":        qid + 1,
            "result":         result_text,
            "question":       q["question"],
            "options":        q["options"],
            "correct_answer": q["answer"],
            "selected_option": selected_option,
            "prompt_text":    "",           # ← nothing → no extra chat line
            "reply_text":     "",
            "comment_wav":    "",           # ← force front-end to use cache
        },
    )

# ───────────────────────── live chat endpoint ────────────────────────── #
@app.post("/chat")
async def chat_endpoint(payload: dict = Body(...)):
    qid   = payload.get("question_id", -1)
    user  = payload.get("text", "")
    reply = get_llm_response(user, qid)

    fname = f"chat_q{qid}_{int(time.time())}.wav"
    generate_and_save_audio(reply, "chat", fname)
    return JSONResponse(
        {"reply": reply, "audio_url": f"/static/audio/chat/{fname}"}
    )

# ───────────────────────── serve cached audio ────────────────────────── #
@app.get("/static/audio/{folder}/{filename}")
async def get_audio(folder: str, filename: str):
    path = os.path.join("static", "audio", folder, filename)
    return FileResponse(path) if os.path.exists(path) else {"error": "Not found"}
