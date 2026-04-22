from IPython.display import Javascript, display
from pathlib import Path

_initialized = False

# def init_audio():
#     global _initialized
#     if _initialized:
#         return

#     # Load Tone.js
#     display(Javascript("""
#     const script = document.createElement('script');
#     script.src = "https://unpkg.com/tone@14.8.49/build/Tone.js";
#     document.head.appendChild(script);
#     """))

#     # Load your audio engine
#     js = Path("midi_audio.js").read_text()
#     display(Javascript(js))

#     _initialized = True



def init_audio():
    global _initialized
    if _initialized:
        return

    # Load Tone.js
    display(Javascript("""
    const script = document.createElement('script');
    script.src = "https://unpkg.com/tone@14.8.49/build/Tone.js";
    document.head.appendChild(script);
    """))

    base = Path(__file__).resolve().parent
    js_path = base / "midi_audio.js"

    js = js_path.read_text()
    display(Javascript(js))