"""Master Scene Builder for 3D Cinematic Supercar Night Race Film.
Constructs the complete 4K 60fps scene in Blender 5.2:
- Bugatti Chiron, Porsche 911 GT3 RS, BMW M4 Competition
- Wet reflective cyberpunk city boulevard with neon lights and garages
- Multi-camera dynamic cinematography with speed ramping and camera shakes
- Synchronized automotive sound design and music
"""
import bpy
import os
import sys

# Ensure cinematic_film package is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from cinematic_film import materials, cars, city, director, audio_producer

def build_entire_production(resolution_x=3840, resolution_y=2160, fps=60):
    """Orchestrates the entire 3D film production in Blender."""
    print("==========================================================")
    print("🎬 Building Cinematic 3D Supercar Night Race Film...")
    print(f"📐 Target Resolution: {resolution_x}x{resolution_y} (4K Ultra HD) @ {fps} FPS")
    print("==========================================================")

    # 1. Clear out default startup scene objects
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # 2. Render Settings (EEVEE Next / Raytraced Reflections)
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = 100
    scene.render.fps = fps

    scene.frame_start = 1
    scene.frame_end = 360  # 6 seconds of continuous, high-speed multi-cut action

    # Enable Motion Blur for high-speed sensation
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5

    # Color Management (Filmic/AgX for cinematic dynamic range)
    if hasattr(scene.view_settings, "view_transform"):
        scene.view_settings.view_transform = 'AgX' if 'AgX' in [e.identifier for e in scene.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    scene.view_settings.look = 'High Contrast'

    # Set Output path & format
    out_dir = os.path.join(current_dir, "output")
    os.makedirs(out_dir, exist_ok=True)
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Configure output format
    format_items = [e.identifier for e in scene.render.image_settings.bl_rna.properties['file_format'].enum_items]
    if 'FFMPEG' in format_items:
        try:
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.ffmpeg.format = 'MPEG4'
            scene.render.ffmpeg.codec = 'H264'
            scene.render.ffmpeg.constant_rate_factor = 'HIGH'
            scene.render.ffmpeg.audio_codec = 'AAC'
            scene.render.filepath = os.path.join(out_dir, "final_film.mp4")
            print("🎥 Output format: Direct MP4 Video with AAC Audio")
        except Exception:
            scene.render.image_settings.file_format = 'PNG'
            scene.render.filepath = os.path.join(frames_dir, "frame_")
            print("🖼️ Output format: High-Quality 4K PNG Frames Sequence")
    else:
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = os.path.join(frames_dir, "frame_")
        print("🖼️ Output format: High-Quality 4K PNG Frames Sequence")

    # 3. Build City Environment (Street, Wet Road, Skyscrapers, Neons, Garages)
    print("🏙️ Generating wet night city & garage stalls...")
    city.build_city_environment(road_length=350.0, road_width=16.0)

    # 4. Build The 3 Hero Supercars
    print("🏎️ Constructing Bugatti Chiron (French Racing Blue / Carbon)...")
    cars.build_bugatti_chiron(location=(-6.0, -10.0, 0.0))

    print("🏎️ Constructing Porsche 911 GT3 RS (Lizard Green / Swan-Neck Wing)...")
    cars.build_porsche_gt3rs(location=(0.0, -10.0, 0.0))

    print("🏎️ Constructing BMW M4 Competition (Frozen Dark Green / Laser Lights)...")
    cars.build_bmw_m4(location=(6.0, -10.0, 0.0))

    # 5. Direct Vehicle Choreography & Racing Animations
    print("⏱️ Keyframing vehicle launch, acceleration, drift, and photo finish...")
    director.animate_cars()

    # 6. Setup 5 Multi-Camera Cinematic Angles
    print("🎥 Directing 5 marker-bound cinematic cameras...")
    director.setup_cinematic_cameras()

    # 7. Generate & Synchronize Audio Effects and Music
    print("🔊 Synthesizing engine sounds, turbos, screeches, and soundtrack...")
    audio_dir = os.path.join(out_dir, "audio")
    audio_producer.setup_vse_audio(audio_dir)

    # Samples configuration
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 32  # Crisp and fast EEVEE Next rendering

    # 8. Save Complete Blender Project File
    blend_path = os.path.join(out_dir, "cinematic_race.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"💾 Scene successfully saved to: {blend_path}")
    print("==========================================================")
    print("🎉 3D Cinematic Race Film is fully constructed and ready for render!")
    print("==========================================================")
    return blend_path

if __name__ == "__main__":
    res_x, res_y = 3840, 2160  # Default 4K Ultra HD
    fps = 60
    if "--1080p" in sys.argv:
        res_x, res_y = 1920, 1080
    if "--120fps" in sys.argv:
        fps = 120
    build_entire_production(resolution_x=res_x, resolution_y=res_y, fps=fps)
