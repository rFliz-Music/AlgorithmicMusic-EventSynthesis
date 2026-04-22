window.midiAudio = (() => {

    const volume = new Tone.Volume(0).toDestination();

    const synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sine" },
        envelope: {
            attack: 0.01,
            decay: 0.1,
            sustain: 0.6,
            release: 0.4
        }
    });

    synth.connect(volume);

    function midiToFreq(m) {
        return Tone.Frequency(m, "midi");
    }

    function setVolume(db) {
        volume.volume.value = db; // in decibels
    }

    function playEvents(events, bpm = 120) {            
        Tone.Transport.stop();
        Tone.Transport.cancel(0);   // clears ALL scheduled events
        Tone.Transport.position = 0;
    
        Tone.Transport.bpm.value = bpm;
    
        Tone.start();
    
        for (const [pitch, vel, dur, start] of events) {
            Tone.Transport.schedule((time) => {
                synth.triggerAttackRelease(
                    midiToFreq(pitch),
                    dur * (60 / bpm),
                    time,
                    vel / 127
                );
            }, start * (60 / bpm));
        }
    
        Tone.Transport.start();
    }

    return {
        playEvents,
        setVolume
    };

})();









// window.midiAudio = (() => {

//     const bpm = 120;

//     function midiToFreq(m) {
//         return 440 * Math.pow(2, (m - 69) / 12);
//     }

//     function playNote(ctx, freq, velocity, start, duration) {
//         const osc = ctx.createOscillator();
//         const gain = ctx.createGain();

//         osc.type = "sine";
//         osc.frequency.value = freq;

//         gain.gain.value = velocity;

//         osc.connect(gain);
//         gain.connect(ctx.destination);

//         osc.start(start);
//         osc.stop(start + duration);
//     }

//     function playEvents(events, bpmOverride = null) {
//         const localBpm = bpmOverride || bpm;
//         const ctx = new (window.AudioContext || window.webkitAudioContext)();
//         const now = ctx.currentTime;

//         const beatToSeconds = (b) => (60 / localBpm) * b;

//         for (const e of events) {
//             const [pitch, velocity, startBeats, durBeats] = e;

//             const startTime = now + beatToSeconds(startBeats);
//             const duration = beatToSeconds(durBeats);

//             playNote(
//                 ctx,
//                 midiToFreq(pitch),
//                 velocity / 127,
//                 startTime,
//                 duration
//             );
//         }
//     }

//     return { playEvents };

// })();


