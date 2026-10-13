"""Blender automation and execution manager."""
import os
import subprocess
import json
import sys

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def get_blender_path():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            path = cfg.get("blender_path")
            if path and os.path.exists(path):
                return path
    default_path = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
    if os.path.exists(default_path):
        return default_path
    raise FileNotFoundError("Blender executable not found. Please verify config.json.")

def run_blender_script(script_path, blend_file=None, background=True, script_args=None):
    """
    Run a Python script inside Blender.
    
    :param script_path: Path to the .py script to execute inside Blender
    :param blend_file: Optional .blend file to open
    :param background: If True, runs headlessly in background
    :param script_args: Optional list of arguments to pass after '--'
    """
    blender_exe = get_blender_path()
    cmd = [blender_exe]
    
    if background:
        cmd.append("--background")
        
    if blend_file:
        cmd.append(blend_file)
        
    cmd.extend(["--python", script_path])
    
    if script_args:
        cmd.append("--")
        cmd.extend(script_args)
        
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result

def render_scene(blend_file, output_image_path, frame=1):
    """
    Render a single frame of a .blend file to an image.
    """
    blender_exe = get_blender_path()
    cmd = [
        blender_exe,
        "--background",
        blend_file,
        "--render-output", output_image_path,
        "--render-frame", str(frame)
    ]
    print(f"Rendering frame {frame} of {blend_file}...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result

def launch_blender_gui(blend_file=None):
    """
    Launch Blender in normal interactive GUI mode.
    """
    blender_exe = get_blender_path()
    cmd = [blender_exe]
    if blend_file:
        cmd.append(blend_file)
    return subprocess.Popen(cmd)

if __name__ == "__main__":
    blender = get_blender_path()
    print(f"Blender path detected: {blender}")
    res = subprocess.run([blender, "--version"], capture_output=True, text=True, errors="replace")
    print(res.stdout.splitlines()[0] if res.stdout else "Blender ready")
