import time
import threading
import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
import numpy as np


# Ticks per beat
TPB = 480

def beats_to_ticks(beats):
    return int(beats * TPB)

def events_to_midi(events, filename="output.mid", tempo_bpm=120):
    """
    events: (note, velocity, duration_beats, start_beats)
    """

    mid = MidiFile(ticks_per_beat=TPB)
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = bpm2tempo(tempo_bpm)
    # track.append(Message('program_change', program=0, time=0))
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    # track.append(Message('set_tempo', tempo=tempo, time=0))

    messages = []

    # expand to absolute time events 
    for note, velocity, duration, start in events:
        start_t = beats_to_ticks(start)
        end_t = beats_to_ticks(start + duration)

        messages.append((start_t, Message('note_on', note=note, velocity=velocity, time=0)))
        messages.append((end_t, Message('note_off', note=note, velocity=0, time=0)))

    # sort by time
    messages.sort(key=lambda x: x[0])

    # convert to delta time
    last = 0
    for t, msg in messages:
        msg.time = t - last
        track.append(msg)
        last = t

    mid.save(filename)
    return filename


def _play_single_note(port, pitch, velocity, duration, start_time, t0):
    """
    Runs inside its own thread so notes can overlap.
    """

    # wait until scheduled onset
    now = time.time() - t0
    if start_time > now:
        time.sleep(start_time - now)

    # NOTE ON
    port.send(mido.Message('note_on', note=pitch, velocity=velocity, channel=1))

    # HOLD
    time.sleep(duration)

    # NOTE OFF
    port.send(mido.Message('note_off', note=pitch, velocity=0, channel=1))



def play_event_tuples(events, port_name="IAC Driver Bus 1"):
    """
    events: list of (pitch, velocity, duration, start_time)
    """

    events = sorted(events, key=lambda e: e[3])

    t0 = time.time()
    threads = []

    # OPEN ONCE (important fix)
    with mido.open_output(port_name) as port:

        for pitch, velocity, duration, start_time in events:
            th = threading.Thread(
                target=_play_single_note,
                args=(port, pitch, velocity, duration, start_time, t0)
            )
            th.daemon = True
            th.start()
            threads.append(th)

        for th in threads:
            th.join()



#  Melodic Utils

# Define φ_S: maps [0, 1) → [0, 1) by stretching space
# in essence giving index space
def phi_S(x, pcs):
    # Normalize pitch class set to [0, 1)    
    x = np.asarray(x)    
    return pcs[int(np.floor(x * len(pcs)))]



def harmonic_quantize(x, pcs):
    # Apply quantization
    octaves = np.floor(x / 12)
    residual = (x % 12) / 12
    warped = phi_S(residual, pcs)
    midi_val = (12 * octaves) + (warped)    
    return int(midi_val)            