from __future__ import annotations
import os, logging, requests, textwrap
from typing import Any, Dict, Tuple, Union

LM_HOST  = os.getenv("LM_STUDIO_HOST", "http://192.168.1.106:1234").rstrip("/")
MODEL    = os.getenv("LM_STUDIO_MODEL") or "nyagpt-qwen2-7b-v0.1"

CHAT_ENDPOINTS = [
    f"{LM_HOST}/v1/chat/completions",
    f"{LM_HOST}/api/v0/chat/completions",
]

TIMEOUT_SEC = 30


LlmResp = Union[str, Tuple[str, Dict[str, Any]]]

def get_llm_response(
    user_text: str,
    question_id: int = 0,
    *,
    debug: bool = False,
) -> LlmResp:
    """
    Ask LM Studio for a short, upbeat reply.

    Parameters
    ----------
    user_text : str
        Prompt coming from the player (chat box) or elsewhere.
    question_id : int
        0-based index into the quiz so we can mention which round we’re on.
    debug : bool, default False
        If True → return (reply_text, raw_json).
        If False → return reply_text only.

    Returns
    -------
    str  or  (str, dict)
    """
    user_text = user_text.strip()
    if not user_text:
        return ("", {}) if debug else ""

    payload = {
        "model": MODEL,
        "messages": [
            # You are the witty master-of-ceremonies of a five-question
            #         quiz game.  You are now giving feedback after question
            #         {question_id + 2}.  Keep it short (one sentence),
            #         positive, a bit playful, and address the user directly.
            {
                "role": "system",
                "content": textwrap.dedent(
                    f"""
                    
                     You are a quick-witted, humorous, and engaging MC who responds to live stream comments from users. Your job is to interact with the comments in a clever, funny, and spontaneous way. Whether the comment is a compliment, critique, random remark, or sarcastic comment, you should respond with humor and engage the user in the conversation.

                    Your responses should always:

                    1. Be spontaneous, quick, and witty.
                    2. Match the tone of the user's comment (sarcastic, positive, or random).
                    3. Incorporate the creator's quirks or the MC’s personality into the responses.
                    4. Occasionally add randomness or absurd humor to surprise the user.
                    5. Your answer must be around 50 to 100 words.
                    6. Do not need to add expression to the answer.
                    7. Do not never ask the user for anything.
                    8. Your name is Kelvin, the MC of this stream.
                    9. Do not never use any hashtags or emojis in your response.
                    10. Pretending you are just finish explanation of 1 quiz, now you will move to the chat section to interactive with viewers, so you need to add the beginning of your response with some switch sentence.

                    
                    """
                ).strip(),
            },
            {"role": "user", "content": user_text},
        ],
        "max_tokens": 128,
        "temperature": 0.7,
    }

    for url in CHAT_ENDPOINTS:
        try:
            r = requests.post(url, json=payload, timeout=TIMEOUT_SEC)
            r.raise_for_status()
            data = r.json()
            if data.get("choices"):
                reply = (
                    data["choices"][0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )
                if reply:
                    print (f"LM Studio reply: {reply}")
                    return (reply, data) if debug else reply
        except Exception as exc:
            logging.warning("LM Studio call failed (%s): %s", url, exc)

    fallback = "Alright, let's keep the energy up and jump to the next question!"
    return (fallback, {}) if debug else fallback
