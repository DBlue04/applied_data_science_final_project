import yaml
import subprocess
import os
import io
from fastapi import FastAPI, Body
from starlette.responses import StreamingResponse

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

model_path = config["model"]["path"]
vocab_path = config["model"]["vocab"]
default_speed = config["inference"]["default_speed"]
use_cuda = config["device"]["use_cuda"]

app = FastAPI()

def save_audio_with_cli(text, output_path):
    """Generate and save audio using the f5-tts-mlx CLI."""
    try:
        command = [
            "python", "-m", "f5_tts_mlx.generate",
            "--text", text,
            "--output", output_path,
            "--speed", str(default_speed),
            "--steps", str(config["inference"]["nfe_steps"]),
            "--method", config["inference"]["ode_method"],
            "--cfg", str(config["inference"]["cfg_strength"]),
            "--sway-coef", str(config["inference"]["sway_sampling_coef"]),
             "--q", str(config["inference"]["quantization"])
        ]
        
        subprocess.run(command, check=True)
        print(f"Audio saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio generation: {e}")
        raise

@app.post("/tts")
async def text_to_speech(text: str = Body(..., embed=True)):
    """Convert text to speech and return as a streaming response."""
    output_filename = "output.wav"

    save_audio_with_cli(text, output_filename)

    if os.path.exists(output_filename):
        with open(output_filename, "rb") as f:
            wav_file = io.BytesIO(f.read())
        return StreamingResponse(wav_file, media_type="audio/wav")
    else:
        return {"error": "Failed to save the audio file."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
