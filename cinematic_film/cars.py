"""Detailed Procedural Supercar Modeler for Blender 5.2.
Builds Bugatti Chiron, Porsche 911 GT3 RS, and BMW M4 Competition with authentic silhouettes,
aerodynamics, wheels, lighting, and materials.
"""
import bpy
import math
from . import materials

def create_wheel(name_prefix, radius=0.36, width=0.26, rim_color=(0.1, 0.1, 0.1, 1.0), caliper_color=(1.0, 0.1, 0.0, 1.0)):
    """Creates a complete high-fidelity sports wheel with tire, rim, brake disc, and caliper."""
    # Root wheel empty for rotation animation
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    wheel_root = bpy.context.active_object
    wheel_root.name = f"{name_prefix}_Root"

    # Tire
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, radius=radius, depth=width,
        rotation=(0, math.radians(90), 0)
    )
    tire = bpy.context.active_object
    tire.name = f"{name_prefix}_Tire"
    tire.data.materials.append(materials.make_tire_rubber())
    tire.parent = wheel_root

    # Rim
    rim_radius = radius * 0.72
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24, radius=rim_radius, depth=width * 0.92,
        rotation=(0, math.radians(90), 0)
    )
    rim = bpy.context.active_object
    rim.name = f"{name_prefix}_Rim"
    rim.data.materials.append(materials.make_alloy_rim(f"{name_prefix}_RimMat", rim_color))
    rim.parent = wheel_root

    # Spokes detail (cross pattern)
    for i in range(5):
        angle = math.radians(i * 72)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            scale=(width * 0.9, rim_radius * 0.15, rim_radius * 0.85),
            rotation=(angle, 0, 0)
        )
        spoke = bpy.context.active_object
        spoke.name = f"{name_prefix}_Spoke_{i}"
        spoke.data.materials.append(materials.make_alloy_rim(f"{name_prefix}_RimMat", rim_color))
        spoke.parent = wheel_root

    # Brake Disc
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24, radius=rim_radius * 0.75, depth=width * 0.25,
        rotation=(0, math.radians(90), 0)
    )
    disc = bpy.context.active_object
    disc.name = f"{name_prefix}_BrakeDisc"
    disc.data.materials.append(materials.make_brake_disc())
    disc.parent = wheel_root

    # Brake Caliper (static, parented to wheel root or car body)
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        scale=(width * 0.35, rim_radius * 0.3, rim_radius * 0.45),
        location=(0, 0, rim_radius * 0.55)
    )
    caliper = bpy.context.active_object
    caliper.name = f"{name_prefix}_Caliper"
    caliper.data.materials.append(materials.make_brake_caliper(f"{name_prefix}_CalMat", caliper_color))
    caliper.parent = wheel_root

    return wheel_root

def build_bugatti_chiron(location=(0, 0, 0), rotation=(0, 0, 0)):
    """Builds the Bugatti Chiron with signature two-tone paint, horseshoe grille, and C-bar."""
    car_name = "Bugatti_Chiron"
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location, rotation=rotation)
    car_root = bpy.context.active_object
    car_root.name = car_name

    # Materials
    paint_blue = materials.make_car_paint("Bugatti_FrenchBlue", (0.04, 0.28, 0.95, 1.0), metallic=0.95, roughness=0.1)
    carbon_black = materials.make_carbon_fiber("Bugatti_Carbon")
    glass_mat = materials.make_car_glass("Bugatti_Glass")
    headlight_mat = materials.make_emission("Bugatti_QuadLED", (0.85, 0.95, 1.0, 1.0), strength=35.0)
    taillight_mat = materials.make_emission("Bugatti_TailStrip", (1.0, 0.02, 0.02, 1.0), strength=25.0)
    grille_mat = materials.make_alloy_rim("Bugatti_ChromeGrille", (0.8, 0.8, 0.8, 1.0))

    # 1. Main Lower Body / Aerodynamic Monocoque
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(2.04, 4.54, 0.65), location=(0, 0, 0.48))
    chassis = bpy.context.active_object
    chassis.name = f"{car_name}_Chassis"
    chassis.data.materials.append(paint_blue)
    chassis.parent = car_root

    # Front Hood Slanted Nose
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.95, 1.8, 0.35), location=(0, 1.45, 0.55), rotation=(math.radians(-8), 0, 0))
    hood = bpy.context.active_object
    hood.name = f"{car_name}_Hood"
    hood.data.materials.append(paint_blue)
    hood.parent = car_root

    # 2. Cabin / Glasshouse Teardrop
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.6, 2.1, 0.58), location=(0, -0.15, 0.96), rotation=(math.radians(-5), 0, 0))
    cabin = bpy.context.active_object
    cabin.name = f"{car_name}_Cabin"
    cabin.data.materials.append(glass_mat)
    cabin.parent = car_root

    # Carbon Fiber Roof & Rear Deck (Two-tone section)
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.55, 1.6, 0.1), location=(0, -0.3, 1.25))
    roof = bpy.context.active_object
    roof.name = f"{car_name}_Roof"
    roof.data.materials.append(carbon_black)
    roof.parent = car_root

    # Rear W16 Engine Cover & Fenders
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.98, 1.7, 0.55), location=(0, -1.45, 0.65))
    rear_deck = bpy.context.active_object
    rear_deck.name = f"{car_name}_RearDeck"
    rear_deck.data.materials.append(carbon_black)
    rear_deck.parent = car_root

    # 3. Signature Bugatti C-Line (Side Aero curves)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.9, minor_radius=0.06,
            location=(side * 0.98, -0.1, 0.75),
            rotation=(0, math.radians(90), 0)
        )
        c_curve = bpy.context.active_object
        c_curve.name = f"{car_name}_CLine_{'R' if side > 0 else 'L'}"
        c_curve.scale = (1.0, 1.35, 0.75)
        c_curve.data.materials.append(grille_mat)
        c_curve.parent = car_root

    # 4. Horseshoe Grille (Front Center)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.35, depth=0.15,
        location=(0, 2.3, 0.42),
        rotation=(math.radians(90), 0, 0)
    )
    grille = bpy.context.active_object
    grille.name = f"{car_name}_HorseshoeGrille"
    grille.scale = (1.0, 1.0, 1.3)
    grille.data.materials.append(grille_mat)
    grille.parent = car_root

    # 5. Quad-LED Headlights (4 crystal square projectors per side)
    for side in [-1, 1]:
        for i in range(4):
            bpy.ops.mesh.primitive_cube_add(
                size=1.0, scale=(0.08, 0.08, 0.06),
                location=(side * (0.58 + i * 0.11), 2.22, 0.62 - i * 0.02)
            )
            led = bpy.context.active_object
            led.name = f"{car_name}_LED_{'R' if side > 0 else 'L'}_{i}"
            led.data.materials.append(headlight_mat)
            led.parent = car_root

        # Front Headlight Spotlight cone
        bpy.ops.object.light_add(
            type='SPOT',
            location=(side * 0.75, 2.3, 0.6),
            rotation=(math.radians(-85), 0, math.radians(side * -2))
        )
        spot = bpy.context.active_object
        spot.name = f"{car_name}_HeadlightSpot_{'R' if side > 0 else 'L'}"
        spot.data.energy = 800.0
        spot.data.spot_size = math.radians(55)
        spot.data.color = (0.9, 0.95, 1.0)
        spot.parent = car_root

    # 6. Full-Width Rear LED Light Bar
    bpy.ops.mesh.primitive_cube_add(
        size=1.0, scale=(1.85, 0.08, 0.05),
        location=(0, -2.28, 0.74)
    )
    rear_strip = bpy.context.active_object
    rear_strip.name = f"{car_name}_TailLightStrip"
    rear_strip.data.materials.append(taillight_mat)
    rear_strip.parent = car_root

    # 7. Active Rear Wing / Spoiler
    bpy.ops.mesh.primitive_cube_add(
        size=1.0, scale=(1.8, 0.38, 0.06),
        location=(0, -2.15, 1.05),
        rotation=(math.radians(-6), 0, 0)
    )
    wing = bpy.context.active_object
    wing.name = f"{car_name}_ActiveWing"
    wing.data.materials.append(carbon_black)
    wing.parent = car_root

    # 8. Wheels Installation
    wheelbase = 1.35
    track_width = 0.95
    wheel_positions = [
        ("FL", -track_width, wheelbase),
        ("FR", track_width, wheelbase),
        ("RL", -track_width, -wheelbase),
        ("RR", track_width, -wheelbase),
    ]
    for w_name, wx, wy in wheel_positions:
        wheel = create_wheel(f"{car_name}_{w_name}", radius=0.38, width=0.28, rim_color=(0.08, 0.08, 0.08, 1.0), caliper_color=(0.0, 0.35, 1.0, 1.0))
        wheel.location = (wx, wy, 0.38)
        if wx > 0:
            wheel.rotation_euler = (0, 0, math.radians(180))
        wheel.parent = car_root

    return car_root

def build_porsche_gt3rs(location=(0, 0, 0), rotation=(0, 0, 0)):
    """Builds the Porsche 911 GT3 RS with swan-neck wing, hood nostrils, and teardrop profile."""
    car_name = "Porsche_GT3RS"
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location, rotation=rotation)
    car_root = bpy.context.active_object
    car_root.name = car_name

    paint_green = materials.make_car_paint("Porsche_LizardGreen", (0.12, 0.78, 0.08, 1.0), metallic=0.92, roughness=0.12)
    carbon_black = materials.make_carbon_fiber("Porsche_CarbonWeissach")
    glass_mat = materials.make_car_glass("Porsche_Glass")
    headlight_mat = materials.make_emission("Porsche_4PointLED", (0.9, 0.98, 1.0, 1.0), strength=35.0)
    taillight_mat = materials.make_emission("Porsche_Taillight", (1.0, 0.05, 0.05, 1.0), strength=25.0)

    # 1. Main Sculpted Body & Wide Rear Haunches
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.92, 4.45, 0.58), location=(0, 0, 0.44))
    chassis = bpy.context.active_object
    chassis.name = f"{car_name}_Chassis"
    chassis.data.materials.append(paint_green)
    chassis.parent = car_root

    # Wide Rear Wheel Arches
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(2.05, 1.6, 0.62), location=(0, -1.2, 0.46))
    rear_arches = bpy.context.active_object
    rear_arches.name = f"{car_name}_RearArches"
    rear_arches.data.materials.append(paint_green)
    rear_arches.parent = car_root

    # Slanted Hood with Dual Extraction Nostrils
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.75, 1.7, 0.3), location=(0, 1.35, 0.52), rotation=(math.radians(-10), 0, 0))
    hood = bpy.context.active_object
    hood.name = f"{car_name}_Hood"
    hood.data.materials.append(paint_green)
    hood.parent = car_root

    # Hood Carbon Air Nostrils
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(0.28, 0.5, 0.08), location=(side * 0.42, 1.25, 0.68), rotation=(math.radians(-10), 0, 0))
        nostril = bpy.context.active_object
        nostril.name = f"{car_name}_Nostril_{'R' if side > 0 else 'L'}"
        nostril.data.materials.append(carbon_black)
        nostril.parent = car_root

    # 2. Teardrop 911 Roof & Greenhouse
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.5, 2.2, 0.62), location=(0, -0.2, 0.98), rotation=(math.radians(-8), 0, 0))
    cabin = bpy.context.active_object
    cabin.name = f"{car_name}_Cabin"
    cabin.data.materials.append(glass_mat)
    cabin.parent = car_root

    # Carbon Roof
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.45, 1.8, 0.08), location=(0, -0.3, 1.28), rotation=(math.radians(-8), 0, 0))
    roof = bpy.context.active_object
    roof.name = f"{car_name}_Roof"
    roof.data.materials.append(carbon_black)
    roof.parent = car_root

    # 3. Massive GT3 RS Swan-Neck Rear Wing
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.95, 0.45, 0.07), location=(0, -2.15, 1.45), rotation=(math.radians(-12), 0, 0))
    main_wing = bpy.context.active_object
    main_wing.name = f"{car_name}_SwanNeckWing"
    main_wing.data.materials.append(carbon_black)
    main_wing.parent = car_root

    # Swan-neck Vertical Mounts
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(0.06, 0.15, 0.55), location=(side * 0.5, -2.0, 1.15))
        mount = bpy.context.active_object
        mount.name = f"{car_name}_WingMount_{'R' if side > 0 else 'L'}"
        mount.data.materials.append(carbon_black)
        mount.parent = car_root

    # Wing Endplates
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(0.05, 0.55, 0.35), location=(side * 1.0, -2.15, 1.45))
        endplate = bpy.context.active_object
        endplate.name = f"{car_name}_WingEndplate_{'R' if side > 0 else 'L'}"
        endplate.data.materials.append(carbon_black)
        endplate.parent = car_root

    # 4. Classic 911 Oval Headlights (with 4-point LED DRLs)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=20, radius=0.22, depth=0.1,
            location=(side * 0.72, 2.05, 0.68),
            rotation=(math.radians(-35), math.radians(side * 12), 0)
        )
        light = bpy.context.active_object
        light.name = f"{car_name}_Headlight_{'R' if side > 0 else 'L'}"
        light.data.materials.append(headlight_mat)
        light.parent = car_root

        # Spotlight cone
        bpy.ops.object.light_add(
            type='SPOT',
            location=(side * 0.72, 2.15, 0.68),
            rotation=(math.radians(-85), 0, math.radians(side * -2))
        )
        spot = bpy.context.active_object
        spot.name = f"{car_name}_HeadlightSpot_{'R' if side > 0 else 'L'}"
        spot.data.energy = 850.0
        spot.data.spot_size = math.radians(52)
        spot.data.color = (0.92, 0.98, 1.0)
        spot.parent = car_root

    # 5. Rear Taillight Continuous Ribbon
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.75, 0.08, 0.04), location=(0, -2.22, 0.72))
    taillight = bpy.context.active_object
    taillight.name = f"{car_name}_TaillightStrip"
    taillight.data.materials.append(taillight_mat)
    taillight.parent = car_root

    # 6. Wheels (Lightweight center-lock with yellow PCCB calipers)
    wheelbase = 1.28
    track_width = 0.92
    wheel_positions = [
        ("FL", -track_width, wheelbase),
        ("FR", track_width, wheelbase),
        ("RL", -track_width * 1.05, -wheelbase),
        ("RR", track_width * 1.05, -wheelbase),
    ]
    for w_name, wx, wy in wheel_positions:
        wheel = create_wheel(f"{car_name}_{w_name}", radius=0.37, width=0.27, rim_color=(0.15, 0.15, 0.15, 1.0), caliper_color=(1.0, 0.85, 0.0, 1.0))
        wheel.location = (wx, wy, 0.37)
        if wx > 0:
            wheel.rotation_euler = (0, 0, math.radians(180))
        wheel.parent = car_root

    return car_root

def build_bmw_m4(location=(0, 0, 0), rotation=(0, 0, 0)):
    """Builds the BMW M4 Competition with aggressive vertical kidney grilles and quad exhausts."""
    car_name = "BMW_M4_Comp"
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location, rotation=rotation)
    car_root = bpy.context.active_object
    car_root.name = car_name

    paint_frozen = materials.make_car_paint("BMW_FrozenGreen", (0.02, 0.18, 0.12, 1.0), metallic=0.88, roughness=0.22)
    carbon_black = materials.make_carbon_fiber("BMW_CarbonRoof")
    glass_mat = materials.make_car_glass("BMW_Glass")
    headlight_mat = materials.make_emission("BMW_LaserLight", (0.8, 0.95, 1.0, 1.0), strength=35.0)
    taillight_mat = materials.make_emission("BMW_TailOLED", (1.0, 0.02, 0.02, 1.0), strength=25.0)
    grille_black = materials.make_alloy_rim("BMW_GlossBlack", (0.02, 0.02, 0.02, 1.0))

    # 1. Muscular Coupe Chassis
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.94, 4.65, 0.62), location=(0, 0, 0.46))
    chassis = bpy.context.active_object
    chassis.name = f"{car_name}_Chassis"
    chassis.data.materials.append(paint_frozen)
    chassis.parent = car_root

    # Power-dome Hood
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.8, 1.85, 0.32), location=(0, 1.45, 0.58), rotation=(math.radians(-6), 0, 0))
    hood = bpy.context.active_object
    hood.name = f"{car_name}_Hood"
    hood.data.materials.append(paint_frozen)
    hood.parent = car_root

    # 2. Signature Tall Vertical Twin-Kidney Grille
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(0.28, 0.12, 0.45),
            location=(side * 0.32, 2.34, 0.45)
        )
        kidney = bpy.context.active_object
        kidney.name = f"{car_name}_KidneyGrille_{'R' if side > 0 else 'L'}"
        kidney.data.materials.append(grille_black)
        kidney.parent = car_root

    # 3. Aggressive Sharp Laser Headlights
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(0.42, 0.15, 0.1),
            location=(side * 0.78, 2.22, 0.62),
            rotation=(0, 0, math.radians(side * -18))
        )
        headlight = bpy.context.active_object
        headlight.name = f"{car_name}_Headlight_{'R' if side > 0 else 'L'}"
        headlight.data.materials.append(headlight_mat)
        headlight.parent = car_root

        # Spotlight cone
        bpy.ops.object.light_add(
            type='SPOT',
            location=(side * 0.78, 2.3, 0.62),
            rotation=(math.radians(-85), 0, math.radians(side * -2))
        )
        spot = bpy.context.active_object
        spot.name = f"{car_name}_HeadlightSpot_{'R' if side > 0 else 'L'}"
        spot.data.energy = 820.0
        spot.data.spot_size = math.radians(50)
        spot.data.color = (0.88, 0.95, 1.0)
        spot.parent = car_root

    # 4. Greenhouse & Carbon M Roof
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.55, 2.3, 0.62), location=(0, -0.1, 1.02), rotation=(math.radians(-4), 0, 0))
    cabin = bpy.context.active_object
    cabin.name = f"{car_name}_Cabin"
    cabin.data.materials.append(glass_mat)
    cabin.parent = car_root

    # Carbon Roof with Double-Bubble Indentation
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.48, 1.9, 0.08), location=(0, -0.2, 1.32))
    roof = bpy.context.active_object
    roof.name = f"{car_name}_Roof"
    roof.data.materials.append(carbon_black)
    roof.parent = car_root

    # 5. Rear Lip Spoiler & L-shaped Taillights
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(1.55, 0.22, 0.08), location=(0, -2.25, 0.88))
    lip_spoiler = bpy.context.active_object
    lip_spoiler.name = f"{car_name}_LipSpoiler"
    lip_spoiler.data.materials.append(carbon_black)
    lip_spoiler.parent = car_root

    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(0.45, 0.1, 0.08),
            location=(side * 0.72, -2.3, 0.72),
            rotation=(0, 0, math.radians(side * 14))
        )
        tail = bpy.context.active_object
        tail.name = f"{car_name}_Taillight_{'R' if side > 0 else 'L'}"
        tail.data.materials.append(taillight_mat)
        tail.parent = car_root

    # 6. Quad Exhaust Tips
    for side in [-1, 1]:
        for i in range(2):
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16, radius=0.07, depth=0.18,
                location=(side * (0.35 + i * 0.16), -2.35, 0.3),
                rotation=(math.radians(90), 0, 0)
            )
            exhaust = bpy.context.active_object
            exhaust.name = f"{car_name}_Exhaust_{'R' if side > 0 else 'L'}_{i}"
            exhaust.data.materials.append(materials.make_chrome() if hasattr(materials, "make_chrome") else carbon_black)
            exhaust.parent = car_root

    # 7. Wheels (M-Compound Alloy)
    wheelbase = 1.38
    track_width = 0.94
    wheel_positions = [
        ("FL", -track_width, wheelbase),
        ("FR", track_width, wheelbase),
        ("RL", -track_width, -wheelbase),
        ("RR", track_width, -wheelbase),
    ]
    for w_name, wx, wy in wheel_positions:
        wheel = create_wheel(f"{car_name}_{w_name}", radius=0.38, width=0.28, rim_color=(0.12, 0.12, 0.12, 1.0), caliper_color=(0.0, 0.25, 0.85, 1.0))
        wheel.location = (wx, wy, 0.38)
        if wx > 0:
            wheel.rotation_euler = (0, 0, math.radians(180))
        wheel.parent = car_root

    return car_root
