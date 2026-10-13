"""Cinematic Director and Camera Switcher for Blender 5.2.
Manages vehicle physics animations, speed curves, wheel rotations, exhaust flames,
and marker-bound multi-camera cinematography.
"""
import bpy
import math

def set_interpolation_linear(action):
    """Sets keyframes to smooth Bezier interpolation (compatible with legacy & Blender 5.x layered actions)."""
    if not action:
        return
    try:
        if hasattr(action, "fcurves"):
            for fcurve in action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
        elif hasattr(action, "layers"):
            for layer in action.layers:
                for strip in getattr(layer, "strips", []):
                    for bag in getattr(strip, "channelbags", []):
                        for fcurve in getattr(bag, "fcurves", []):
                            for kf in fcurve.keyframe_points:
                                kf.interpolation = 'BEZIER'
    except Exception:
        pass

def animate_cars():
    """Animates Bugatti, Porsche, and BMW across the 360-frame race sequence."""
    bugatti = bpy.data.objects.get("Bugatti_Chiron")
    porsche = bpy.data.objects.get("Porsche_GT3RS")
    bmw = bpy.data.objects.get("BMW_M4_Comp")

    if not bugatti or not porsche or not bmw:
        print("Warning: One or more car objects not found for animation.")
        return

    # Frame 1: Inside Garages
    bugatti.location = (-6.0, -10.0, 0.0)
    porsche.location = (0.0, -10.0, 0.0)
    bmw.location = (6.0, -10.0, 0.0)

    for car in [bugatti, porsche, bmw]:
        car.rotation_euler = (0, 0, 0)
        car.keyframe_insert(data_path="location", frame=1)
        car.keyframe_insert(data_path="rotation_euler", frame=1)

    # Frame 65: Rollout onto Starting Paddock (Y = 15)
    bugatti.location = (-4.0, 15.0, 0.0)
    porsche.location = (0.0, 15.0, 0.0)
    bmw.location = (4.0, 15.0, 0.0)

    for car in [bugatti, porsche, bmw]:
        car.keyframe_insert(data_path="location", frame=65)
        car.keyframe_insert(data_path="rotation_euler", frame=65)

    # Frame 110: Revving at Launch Line (Y = 18..20)
    bugatti.location = (-4.0, 18.0, 0.0)
    porsche.location = (0.0, 18.0, 0.0)
    bmw.location = (4.0, 19.0, 0.0)

    for car in [bugatti, porsche, bmw]:
        car.keyframe_insert(data_path="location", frame=110)
        car.keyframe_insert(data_path="rotation_euler", frame=110)

    # Frame 170: Full Throttle Acceleration Down Avenue
    # BMW takes early lead with quick launch, Porsche close second
    bmw.location = (3.5, 95.0, 0.0)
    porsche.location = (-0.5, 90.0, 0.0)
    bugatti.location = (-3.8, 85.0, 0.0)

    for car in [bugatti, porsche, bmw]:
        car.keyframe_insert(data_path="location", frame=170)
        car.keyframe_insert(data_path="rotation_euler", frame=170)

    # Frame 230: Approaching the Drift Curve
    bmw.location = (2.5, 160.0, 0.0)
    porsche.location = (-1.0, 162.0, 0.0)
    bugatti.location = (-3.2, 158.0, 0.0)

    for car in [bugatti, porsche, bmw]:
        car.keyframe_insert(data_path="location", frame=230)
        car.keyframe_insert(data_path="rotation_euler", frame=230)

    # Frame 275: The Drift - Porsche slides sideways around BMW
    porsche.location = (1.5, 215.0, 0.0)
    porsche.rotation_euler = (0, 0, math.radians(-18)) # Drift angle
    porsche.keyframe_insert(data_path="location", frame=275)
    porsche.keyframe_insert(data_path="rotation_euler", frame=275)

    bmw.location = (-2.0, 210.0, 0.0)
    bmw.rotation_euler = (0, 0, math.radians(10))
    bmw.keyframe_insert(data_path="location", frame=275)
    bmw.keyframe_insert(data_path="rotation_euler", frame=275)

    bugatti.location = (-0.5, 212.0, 0.0)
    bugatti.rotation_euler = (0, 0, math.radians(-8))
    bugatti.keyframe_insert(data_path="location", frame=275)
    bugatti.keyframe_insert(data_path="rotation_euler", frame=275)

    # Frame 320: Straightening Out for Final Drag
    porsche.location = (1.8, 252.0, 0.0)
    porsche.rotation_euler = (0, 0, 0)
    porsche.keyframe_insert(data_path="location", frame=320)
    porsche.keyframe_insert(data_path="rotation_euler", frame=320)

    bugatti.location = (-1.8, 251.0, 0.0)
    bugatti.rotation_euler = (0, 0, 0)
    bugatti.keyframe_insert(data_path="location", frame=320)
    bugatti.keyframe_insert(data_path="rotation_euler", frame=320)

    bmw.location = (4.0, 245.0, 0.0)
    bmw.rotation_euler = (0, 0, 0)
    bmw.keyframe_insert(data_path="location", frame=320)
    bmw.keyframe_insert(data_path="rotation_euler", frame=320)

    # Frame 360: Photo Finish at Finish Arch (Y = 280)
    # Bugatti surges ahead by 0.6m for the thrilling victory!
    bugatti.location = (-1.8, 283.5, 0.0)
    bugatti.keyframe_insert(data_path="location", frame=360)

    porsche.location = (1.8, 282.8, 0.0)
    porsche.keyframe_insert(data_path="location", frame=360)

    bmw.location = (4.0, 276.0, 0.0)
    bmw.keyframe_insert(data_path="location", frame=360)

    for car in [bugatti, porsche, bmw]:
        set_interpolation_linear(car.animation_data.action if car.animation_data else None)

def setup_cinematic_cameras():
    """Sets up 5 cinematic cameras and binds them to timeline markers."""
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 360

    cameras_data = [
        # (CamName, StartFrame, Location, Rotation, FocalLength)
        ("Cam_1_Garages", 1, (0.0, 5.0, 1.8), (math.radians(82), 0, math.radians(180)), 28.0),
        ("Cam_2_StagingLine", 71, (-2.5, 23.0, 0.7), (math.radians(86), 0, math.radians(155)), 50.0),
        ("Cam_3_RocketLaunch", 111, (0.0, 120.0, 0.45), (math.radians(88), 0, math.radians(180)), 35.0),
        ("Cam_4_DriftDrone", 211, (6.0, 195.0, 8.5), (math.radians(65), 0, math.radians(45)), 24.0),
        ("Cam_5_FinishLine", 291, (0.0, 290.0, 1.2), (math.radians(84), 0, math.radians(180)), 85.0),
    ]

    # Clear existing markers
    scene.timeline_markers.clear()

    first_cam = None
    for cam_name, start_frame, loc, rot, focal in cameras_data:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_data.lens = focal
        cam_data.dof.use_dof = True
        cam_data.dof.focus_distance = 12.0
        cam_data.dof.aperture_fstop = 2.8

        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        cam_obj.location = loc
        cam_obj.rotation_euler = rot
        bpy.context.collection.objects.link(cam_obj)

        if not first_cam:
            first_cam = cam_obj
            scene.camera = cam_obj

        # Create marker and bind camera
        marker = scene.timeline_markers.new(name=cam_name, frame=start_frame)
        marker.camera = cam_obj

        # Dynamic subtle dolly animation for each camera
        cam_obj.keyframe_insert(data_path="location", frame=start_frame)
        cam_obj.location.y += 3.0
        cam_obj.keyframe_insert(data_path="location", frame=start_frame + 70)
