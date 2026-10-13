"""Dark Rainy Night City Environment for Blender 5.2.
Builds the wet reflective street, skyscrapers, neon billboards, streetlights,
start/finish gantry arches, and 3 distinct car garages.
"""
import bpy
import math
import random
from . import materials

def build_garage(name, location, width=4.5, depth=8.0, height=3.5):
    """Builds an underground/industrial garage stall with overhead lighting and roll-up door."""
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    garage_root = bpy.context.active_object
    garage_root.name = f"Garage_{name}_Root"

    conc_mat = materials.make_concrete()
    shutter_mat = materials.make_metal_shutter()
    light_mat = materials.make_emission(f"Garage_{name}_TubeMat", (0.9, 0.95, 1.0, 1.0), strength=25.0)

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=1.0, scale=(width, depth, 1.0), location=(0, 0, 0.01))
    floor = bpy.context.active_object
    floor.name = f"Garage_{name}_Floor"
    floor.data.materials.append(materials.make_wet_asphalt(f"Garage_{name}_WetFloor"))
    floor.parent = garage_root

    # Back Wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(width, 0.3, height), location=(0, -depth/2, height/2))
    back_wall = bpy.context.active_object
    back_wall.name = f"Garage_{name}_BackWall"
    back_wall.data.materials.append(conc_mat)
    back_wall.parent = garage_root

    # Left & Right Walls
    for side, sign in [("Left", -1), ("Right", 1)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(0.3, depth, height), location=(sign * width/2, 0, height/2))
        wall = bpy.context.active_object
        wall.name = f"Garage_{name}_{side}Wall"
        wall.data.materials.append(conc_mat)
        wall.parent = garage_root

    # Ceiling
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(width, depth, 0.2), location=(0, 0, height))
    ceiling = bpy.context.active_object
    ceiling.name = f"Garage_{name}_Ceiling"
    ceiling.data.materials.append(conc_mat)
    ceiling.parent = garage_root

    # Overhead Industrial Light Fixture
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.08, depth=depth * 0.6,
        location=(0, 0, height - 0.2),
        rotation=(math.radians(90), 0, 0)
    )
    light_tube = bpy.context.active_object
    light_tube.name = f"Garage_{name}_LightTube"
    light_tube.data.materials.append(light_mat)
    light_tube.parent = garage_root

    # Garage Area Spotlight
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, height - 0.25), rotation=(0, 0, 0))
    spot = bpy.context.active_object
    spot.name = f"Garage_{name}_Spot"
    spot.data.energy = 1500.0
    spot.data.spot_size = math.radians(75)
    spot.data.color = (0.88, 0.94, 1.0)
    spot.parent = garage_root

    # Roll-up Shutter Door (animated upward)
    bpy.ops.mesh.primitive_cube_add(size=1.0, scale=(width * 0.95, 0.08, height * 0.95), location=(0, depth/2, height * 0.48))
    shutter = bpy.context.active_object
    shutter.name = f"Garage_{name}_Shutter"
    shutter.data.materials.append(shutter_mat)
    shutter.parent = garage_root

    # Shutter opening animation (Frames 1 to 60)
    shutter.keyframe_insert(data_path="location", frame=1)
    shutter.location.z = height + 1.2
    shutter.keyframe_insert(data_path="location", frame=50)

    return garage_root

def build_city_environment(road_length=350.0, road_width=16.0):
    """Builds the complete wet street boulevard, skyscrapers, neons, street lamps, and gantries."""
    city_root_name = "City_Environment"
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    city_root = bpy.context.active_object
    city_root.name = city_root_name

    wet_asphalt = materials.make_wet_asphalt("Boulevard_WetAsphalt")
    marking_white = materials.make_emission("Marking_White", (0.9, 0.9, 0.95, 1.0), strength=2.0)
    marking_yellow = materials.make_emission("Marking_Yellow", (1.0, 0.8, 0.05, 1.0), strength=2.5)
    sidewalk_mat = materials.make_concrete("Sidewalk_Mat")
    barrier_mat = materials.make_alloy_rim("CrashBarrier_Mat", (0.35, 0.35, 0.38, 1.0))

    # 1. Main Asphalt Road
    bpy.ops.mesh.primitive_plane_add(
        size=1.0, scale=(road_width, road_length, 1.0),
        location=(0, road_length / 2, 0)
    )
    road = bpy.context.active_object
    road.name = "Main_Asphalt_Road"
    road.data.materials.append(wet_asphalt)
    road.parent = city_root

    # Center Double Yellow Lines
    for y_offset in [-0.15, 0.15]:
        bpy.ops.mesh.primitive_plane_add(
            size=1.0, scale=(0.12, road_length, 1.0),
            location=(y_offset, road_length / 2, 0.005)
        )
        line = bpy.context.active_object
        line.name = f"Center_Line_{'R' if y_offset > 0 else 'L'}"
        line.data.materials.append(marking_yellow)
        line.parent = city_root

    # White Dashed Lane Dividers
    dash_length = 3.5
    dash_gap = 4.0
    for lane_x in [-road_width * 0.25, road_width * 0.25]:
        y_pos = 0.0
        while y_pos < road_length:
            bpy.ops.mesh.primitive_plane_add(
                size=1.0, scale=(0.15, dash_length, 1.0),
                location=(lane_x, y_pos + dash_length / 2, 0.005)
            )
            dash = bpy.context.active_object
            dash.name = f"LaneDash_{int(lane_x)}_{int(y_pos)}"
            dash.data.materials.append(marking_white)
            dash.parent = city_root
            y_pos += dash_length + dash_gap

    # 2. Sidewalks & Crash Guardrails
    for side, sign in [("Left", -1), ("Right", 1)]:
        sidewalk_x = sign * (road_width / 2 + 2.0)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(4.0, road_length, 0.3),
            location=(sidewalk_x, road_length / 2, 0.15)
        )
        sidewalk = bpy.context.active_object
        sidewalk.name = f"Sidewalk_{side}"
        sidewalk.data.materials.append(sidewalk_mat)
        sidewalk.parent = city_root

        # Metal Guardrail Barrier
        barrier_x = sign * (road_width / 2 + 0.3)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(0.2, road_length, 0.75),
            location=(barrier_x, road_length / 2, 0.45)
        )
        barrier = bpy.context.active_object
        barrier.name = f"Guardrail_{side}"
        barrier.data.materials.append(barrier_mat)
        barrier.parent = city_root

    # 3. Street Light Poles & Downward Cones
    pole_interval = 35.0
    y_lamp = 10.0
    lamp_mat = materials.make_emission("StreetLamp_Emiss", (1.0, 0.85, 0.6, 1.0), strength=20.0)
    while y_lamp < road_length:
        for side, sign in [("Left", -1), ("Right", 1)]:
            lamp_x = sign * (road_width / 2 + 1.2)
            # Vertical pole
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12, radius=0.09, depth=8.0,
                location=(lamp_x, y_lamp, 4.0)
            )
            pole = bpy.context.active_object
            pole.name = f"LampPole_{side}_{int(y_lamp)}"
            pole.data.materials.append(barrier_mat)
            pole.parent = city_root

            # Horizontal arm
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12, radius=0.06, depth=2.2,
                location=(lamp_x - sign * 0.9, y_lamp, 8.0),
                rotation=(0, math.radians(sign * 90), 0)
            )
            arm = bpy.context.active_object
            arm.data.materials.append(barrier_mat)
            arm.parent = city_root

            # Emissive bulb head
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16, radius=0.25, depth=0.15,
                location=(lamp_x - sign * 1.8, y_lamp, 7.85)
            )
            bulb = bpy.context.active_object
            bulb.data.materials.append(lamp_mat)
            bulb.parent = city_root

            # Volumetric Spotlight cone
            bpy.ops.object.light_add(
                type='SPOT',
                location=(lamp_x - sign * 1.8, y_lamp, 7.8),
                rotation=(0, 0, 0)
            )
            spot = bpy.context.active_object
            spot.name = f"LampLight_{side}_{int(y_lamp)}"
            spot.data.energy = 2200.0
            spot.data.spot_size = math.radians(65)
            spot.data.color = (1.0, 0.88, 0.65)
            spot.parent = city_root

        y_lamp += pole_interval

    # 4. Skyscrapers with Illuminated Windows & Rooftop Neons
    neon_colors = [
        (1.0, 0.05, 0.55, 1.0),  # Neon Pink / Magenta
        (0.05, 0.85, 1.0, 1.0),  # Cyberpunk Cyan
        (0.98, 0.55, 0.05, 1.0), # Neon Orange
        (0.55, 0.1, 1.0, 1.0),   # Neon Purple
        (0.1, 1.0, 0.45, 1.0)    # Acid Neon Green
    ]

    building_y = 5.0
    b_idx = 0
    glass_facade = materials.make_car_paint("Skyscraper_Glass", (0.02, 0.03, 0.05, 1.0), metallic=0.98, roughness=0.08)

    while building_y < road_length:
        for side, sign in [("Left", -1), ("Right", 1)]:
            bx = sign * (road_width / 2 + 18.0 + random.uniform(0, 5))
            b_width = random.uniform(16.0, 24.0)
            b_depth = random.uniform(18.0, 26.0)
            b_height = random.uniform(45.0, 95.0)

            bpy.ops.mesh.primitive_cube_add(
                size=1.0, scale=(b_width, b_depth, b_height),
                location=(bx, building_y + b_depth / 2, b_height / 2)
            )
            bldg = bpy.context.active_object
            bldg.name = f"Building_{side}_{b_idx}"
            bldg.data.materials.append(glass_facade)
            bldg.parent = city_root

            # Neon Billboard on Facade facing the road
            billboard_color = random.choice(neon_colors)
            billboard_mat = materials.make_neon_sign(f"NeonSign_{side}_{b_idx}", billboard_color, strength=30.0)
            billboard_x = sign * (road_width / 2 + 7.5)
            bpy.ops.mesh.primitive_plane_add(
                size=1.0, scale=(0.1, random.uniform(6.0, 10.0), random.uniform(3.0, 5.0)),
                location=(billboard_x, building_y + b_depth / 2, random.uniform(8.0, 20.0)),
                rotation=(math.radians(90), 0, math.radians(sign * 90))
            )
            billboard = bpy.context.active_object
            billboard.name = f"NeonBillboard_{side}_{b_idx}"
            billboard.data.materials.append(billboard_mat)
            billboard.parent = city_root

        building_y += 32.0
        b_idx += 1

    # 5. Start / Finish Line Overhead Arch Gantry (with Countdown Signals)
    gantry_positions = [("StartArch", 25.0), ("FinishArch", 280.0)]
    for g_name, gy in gantry_positions:
        # Crossbar
        bpy.ops.mesh.primitive_cube_add(
            size=1.0, scale=(road_width + 6.0, 1.2, 0.8),
            location=(0, gy, 8.5)
        )
        crossbar = bpy.context.active_object
        crossbar.name = f"{g_name}_Crossbar"
        crossbar.data.materials.append(barrier_mat)
        crossbar.parent = city_root

        # Support Pillars
        for side, sign in [("L", -1), ("R", 1)]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16, radius=0.4, depth=8.5,
                location=(sign * (road_width / 2 + 2.5), gy, 4.25)
            )
            pillar = bpy.context.active_object
            pillar.name = f"{g_name}_Pillar_{side}"
            pillar.data.materials.append(barrier_mat)
            pillar.parent = city_root

        # Digital Race Lights (Red / Yellow / Green signals)
        light_types = [
            ("Red", (1.0, 0.05, 0.05, 1.0), -2.5),
            ("Yellow", (1.0, 0.85, 0.05, 1.0), 0.0),
            ("Green", (0.05, 1.0, 0.15, 1.0), 2.5),
        ]
        for l_type, l_color, lx in light_types:
            sig_mat = materials.make_emission(f"{g_name}_Signal_{l_type}", l_color, strength=30.0)
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16, radius=0.35, depth=0.2,
                location=(lx, gy + 0.65, 8.5),
                rotation=(math.radians(90), 0, 0)
            )
            signal = bpy.context.active_object
            signal.name = f"{g_name}_Signal_{l_type}"
            signal.data.materials.append(sig_mat)
            signal.parent = city_root

    # 6. Build the 3 Garages at the starting paddock (before Y=0)
    garage_spacing = 6.0
    garages = [
        ("Bugatti", (-garage_spacing, -10.0, 0)),
        ("Porsche", (0.0, -10.0, 0)),
        ("BMW", (garage_spacing, -10.0, 0))
    ]
    for g_id, g_pos in garages:
        build_garage(g_id, g_pos)

    # 7. World Environment Setup (Midnight atmosphere)
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("Night_World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.005, 0.008, 0.015, 1.0) # Deep midnight ambient
        bg.inputs["Strength"].default_value = 0.4

    return city_root
