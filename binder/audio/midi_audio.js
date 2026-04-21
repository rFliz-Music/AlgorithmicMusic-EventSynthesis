window.midiAudio = (() => {

    const bpm = 120;

    function midiToFreq(m) {
        return 440 * Math.pow(2, (m - 69) / 12);
    }

    function playNote(ctx, freq, velocity, start, duration) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.value = freq;

        gain.gain.value = velocity;

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(start);
        osc.stop(start + duration);
    }

    function playEvents(events, bpmOverride = null) {
        const localBpm = bpmOverride || bpm;
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const now = ctx.currentTime;

        const beatToSeconds = (b) => (60 / localBpm) * b;

        for (const e of events) {
            const [pitch, velocity, startBeats, durBeats] = e;

            const startTime = now + beatToSeconds(startBeats);
            const duration = beatToSeconds(durBeats);

            playNote(
                ctx,
                midiToFreq(pitch),
                velocity / 127,
                startTime,
                duration
            );
        }
    }

    return { playEvents };

})();