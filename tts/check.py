import yaml
import torch

# Load the configuration file
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

# Load the model manually using torch
model_path = cfg["model"]["path"]
try:
    model = torch.load(model_path)
    print("Model loaded successfully:", type(model))
except Exception as e:
    print(f"Error loading model: {e}")
