"""Video and Audio Compiler.
Compiles rendered 4K/60fps frames and synthesized audio tracks into final_film.mp4.
"""
import os
import subprocess
import glob
import sys

def compile_final_movie():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "output")
    frames_dir = os.path.join(out_dir, "frames")
    audio_file = os.path.join(out_dir, "audio", "cinematic_soundtrack.wav")
    final_mp4 = os.path.join(out_dir, "final_film.mp4")

    # If final_film.mp4 was already created directly by Blender FFMPEG, verify it
    if os.path.exists(final_mp4) and os.path.getsize(final_mp4) > 100000:
        print(f"✅ Final video already rendered at: {final_mp4}")
        return

    # Check for rendered frames
    frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
    if not frames:
        print("⚠️ No rendered frames found in output/frames/.")
        return

    print(f"🎬 Found {len(frames)} rendered frames. Muxing into 60fps MP4 with audio...")

    # Use ffmpeg CLI (available on Linux / Codespaces)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "60",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
    ]
    if os.path.exists(audio_file):
        cmd.extend(["-i", audio_file, "-c:a", "aac", "-b:a", "192k"])

    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18", # High visual quality
        "-preset", "fast",
        final_mp4
    ])

    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"🎉 Final 4K 60FPS Video rendered successfully: {final_mp4} ({os.path.getsize(final_mp4) // 1024} KB)")
    else:
        print(f"FFmpeg error: {res.stderr}")

if __name__ == "__main__":
    compile_final_movie()
