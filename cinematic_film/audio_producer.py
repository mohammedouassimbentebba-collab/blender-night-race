"""High-Octane Cinematic Audio Producer & Sequencer for Blender 5.2.
Synthesizes professional engine roars, turbo flutters, tire screeches, launch countdowns,
and action rhythm, and places them into Blender's Video Sequence Editor (VSE).
"""
import os
import math
import struct
import wave
import bpy

def generate_tone(filepath, duration_sec, freq_start, freq_end, sample_rate=44100, volume=0.8, harmonics=True):
    """Generates a dynamic frequency-swept waveform (e.g., accelerating engine)."""
    n_samples = int(duration_sec * sample_rate)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(2) # Stereo
        wav.setsampwidth(2) # 16-bit
        wav.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Linear frequency sweep
            freq = freq_start + (freq_end - freq_start) * (t / duration_sec)
            phase = 2 * math.pi * freq * t

            # Rich automotive harmonics (W16 / Flat-6 acoustic profile)
            val = math.sin(phase)
            if harmonics:
                val += 0.5 * math.sin(phase * 2) + 0.25 * math.sin(phase * 3) + 0.15 * math.sin(phase * 4)
                val /= 1.9

            # Fade in/out to prevent clicks
            envelope = min(t * 10, 1.0) * min((duration_sec - t) * 10, 1.0)
            sample = int(val * volume * envelope * 32767)
            sample = max(-32768, min(32767, sample))

            # Pack stereo left & right
            frames.extend(struct.pack('<hh', sample, sample))

        wav.writeframes(frames)
    return filepath

def generate_tire_screech(filepath, duration_sec=1.8, sample_rate=44100, volume=0.7):
    """Generates a high-friction tire screech / drift smoke sound effect."""
    n_samples = int(duration_sec * sample_rate)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        import random
        for i in range(n_samples):
            t = i / sample_rate
            # High frequency resonance + white noise
            noise = (random.random() * 2 - 1)
            resonance = math.sin(2 * math.pi * 1250 * t) + 0.5 * math.sin(2 * math.pi * 1850 * t)
            val = (noise * 0.4 + resonance * 0.6)

            envelope = min(t * 8, 1.0) * min((duration_sec - t) * 6, 1.0)
            sample = int(val * volume * envelope * 32767)
            sample = max(-32768, min(32767, sample))
            frames.extend(struct.pack('<hh', sample, sample))

        wav.writeframes(frames)
    return filepath

def generate_countdown(filepath, sample_rate=44100):
    """Generates the starting race lights countdown beeps (Beep, Beep, Beep, GO!)."""
    duration_sec = 2.0
    n_samples = int(duration_sec * sample_rate)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            val = 0.0
            # 3 warning beeps at 0.0s, 0.5s, 1.0s (440Hz), GO beep at 1.5s (880Hz)
            for beep_time, freq, dur in [(0.0, 440, 0.15), (0.5, 440, 0.15), (1.0, 440, 0.15), (1.5, 880, 0.4)]:
                if beep_time <= t < beep_time + dur:
                    sub_t = t - beep_time
                    env = math.sin(math.pi * (sub_t / dur))
                    val = math.sin(2 * math.pi * freq * sub_t) * env * 0.8
                    break

            sample = int(val * 32767)
            sample = max(-32768, min(32767, sample))
            frames.extend(struct.pack('<hh', sample, sample))

        wav.writeframes(frames)
    return filepath

def generate_cinematic_music_beat(filepath, duration_sec=6.5, sample_rate=44100):
    """Generates a dark driving cyberpunk / synthwave bass pulse track."""
    n_samples = int(duration_sec * sample_rate)
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        bpm = 135.0
        beat_dur = 60.0 / bpm
        for i in range(n_samples):
            t = i / sample_rate
            beat_phase = (t % beat_dur) / beat_dur

            # 4-on-the-floor kick drum
            kick_env = max(0, 1.0 - beat_phase * 5.0)
            kick = math.sin(2 * math.pi * (55.0 + 80.0 * kick_env) * beat_phase * beat_dur) * kick_env * 0.85

            # Rolling synth bassline (E-minor drive)
            bass_freq = 65.41 if (int(t / (beat_dur * 4)) % 2 == 0) else 58.27
            bass_phase = 2 * math.pi * bass_freq * t
            bass = (math.sin(bass_phase) + 0.4 * math.sin(bass_phase * 2)) * 0.45

            val = kick + bass
            # Master volume envelope
            master_env = min(t * 2, 1.0) * min((duration_sec - t) * 1.5, 1.0)
            sample = int(val * 0.7 * master_env * 32767)
            sample = max(-32768, min(32767, sample))
            frames.extend(struct.pack('<hh', sample, sample))

        wav.writeframes(frames)
    return filepath

def setup_vse_audio(audio_dir):
    """Generates all sound clips and places them onto Blender's VSE timeline."""
    os.makedirs(audio_dir, exist_ok=True)
    scene = bpy.context.scene

    if not scene.sequence_editor:
        scene.sequence_editor_create()

    seq = getattr(scene.sequence_editor, "strips", None)
    if seq is None:
        seq = getattr(scene.sequence_editor, "sequences", None)

    # 1. Engine Startup & Idle (Frames 1 to 70)
    p_engine_start = os.path.join(audio_dir, "engine_start.wav")
    generate_tone(p_engine_start, duration_sec=1.2, freq_start=60, freq_end=120, volume=0.85)
    seq.new_sound(name="Engine_Startup", filepath=p_engine_start, channel=1, frame_start=1)

    # 2. Race Countdown Beeps (Frames 80 to 130)
    p_countdown = os.path.join(audio_dir, "countdown.wav")
    generate_countdown(p_countdown)
    seq.new_sound(name="Race_Countdown", filepath=p_countdown, channel=2, frame_start=80)

    # 3. High-RPM Acceleration Roar (Frames 110 to 220)
    p_accel = os.path.join(audio_dir, "engine_accel.wav")
    generate_tone(p_accel, duration_sec=2.2, freq_start=110, freq_end=580, volume=0.9)
    seq.new_sound(name="Engine_Acceleration", filepath=p_accel, channel=1, frame_start=110)

    # 4. Tire Screech on Drift Curve (Frames 220 to 290)
    p_screech = os.path.join(audio_dir, "tire_screech.wav")
    generate_tire_screech(p_screech, duration_sec=1.5, volume=0.75)
    seq.new_sound(name="Drift_Screech", filepath=p_screech, channel=3, frame_start=220)

    # 5. Top-Speed W16 Redline & Flyby (Frames 280 to 360)
    p_flyby = os.path.join(audio_dir, "top_speed_flyby.wav")
    generate_tone(p_flyby, duration_sec=1.6, freq_start=450, freq_end=720, volume=0.95)
    seq.new_sound(name="Top_Speed_Flyby", filepath=p_flyby, channel=1, frame_start=280)

    # 6. Cinematic Action Synth Soundtrack (Frames 1 to 360)
    p_music = os.path.join(audio_dir, "cinematic_soundtrack.wav")
    generate_cinematic_music_beat(p_music, duration_sec=6.2)
    music_strip = seq.new_sound(name="Cinematic_Soundtrack", filepath=p_music, channel=4, frame_start=1)
    music_strip.volume = 0.65

    print("✅ All sound effects generated and synchronized into Blender timeline!")
