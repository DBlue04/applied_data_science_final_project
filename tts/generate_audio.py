import sys
import requests

API = "http://localhost:7860/tts"

text = " ".join(sys.argv[1:]) or "The answer is H₂O. Water’s formula, H₂O, might look simple, but it unlocks a world of wonders: two tiny hydrogen atoms bound to a heftier oxygen, creating a bent molecule with a slight positive charge on the hydrogens and a negative charge on the oxygen. This polarity lets water molecules cling together in hydrogen-bonded networks, giving rise to its famous surface tension—so strong that some insects stride across ponds as if on solid ground. Deep inside every drop, those hydrogen bonds constantly break and reform, absorbing or releasing heat without dramatic temperature swings. That high heat capacity keeps Earth’s climate stable, oceans temperate, and even your morning coffee at just the right warmth. When water freezes, its molecules lock into a crystalline lattice that’s less dense than the liquid state—ice floats, insulating lakes and protecting marine life through frigid winters. beyond physics, H₂O is life’s ultimate shuttle. Its polarity pulls apart salts and sugars, ferrying minerals to plant roots, carrying nutrients in our bloodstream, and dissolving oxygen for fish to breathe. From carving Grand Canyon canyons to sustaining every cell in your body, H₂O truly is the humble superhero of molecules—silent, versatile, and utterly essential."


try:
    r = requests.post(API, json={"text": text})
    r.raise_for_status()

    with open("output.wav", "wb") as f:
        f.write(r.content)

    print(f"File saved locally as output.wav (size: {len(r.content)} bytes)")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
