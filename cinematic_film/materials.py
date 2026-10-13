"""PBR Material Library for Blender 5.2 Cinematic Race."""
import bpy

def get_or_create_material(name):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
    return mat

def get_bsdf(mat):
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        output = nodes.get("Material Output")
        if not output:
            output = nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return bsdf

def set_bsdf_input(bsdf, input_name, value):
    inp = bsdf.inputs.get(input_name)
    if inp:
        inp.default_value = value

def make_car_paint(name, base_color, metallic=0.95, roughness=0.12, coat=1.0):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", base_color)
    set_bsdf_input(bsdf, "Metallic", metallic)
    set_bsdf_input(bsdf, "Roughness", roughness)
    set_bsdf_input(bsdf, "Coat Weight", coat)
    set_bsdf_input(bsdf, "Coat Roughness", 0.05)
    set_bsdf_input(bsdf, "Specular IOR Level", 0.6)
    return mat

def make_car_glass(name="CarGlass", tint=(0.02, 0.03, 0.05, 1.0)):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", tint)
    set_bsdf_input(bsdf, "Metallic", 0.1)
    set_bsdf_input(bsdf, "Roughness", 0.02)
    set_bsdf_input(bsdf, "Transmission Weight", 0.85)
    set_bsdf_input(bsdf, "IOR", 1.45)
    return mat

def make_carbon_fiber(name="CarbonFiber"):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", (0.04, 0.04, 0.04, 1.0))
    set_bsdf_input(bsdf, "Metallic", 0.4)
    set_bsdf_input(bsdf, "Roughness", 0.3)
    set_bsdf_input(bsdf, "Coat Weight", 0.8)
    set_bsdf_input(bsdf, "Coat Roughness", 0.1)
    return mat

def make_tire_rubber(name="TireRubber"):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", (0.03, 0.03, 0.03, 1.0))
    set_bsdf_input(bsdf, "Metallic", 0.0)
    set_bsdf_input(bsdf, "Roughness", 0.85)
    return mat

def make_alloy_rim(name="AlloyRim", color=(0.15, 0.15, 0.15, 1.0)):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", color)
    set_bsdf_input(bsdf, "Metallic", 0.95)
    set_bsdf_input(bsdf, "Roughness", 0.2)
    return mat

def make_brake_disc(name="BrakeDisc"):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", (0.6, 0.6, 0.6, 1.0))
    set_bsdf_input(bsdf, "Metallic", 0.98)
    set_bsdf_input(bsdf, "Roughness", 0.25)
    return mat

def make_brake_caliper(name="BrakeCaliper", color=(1.0, 0.08, 0.0, 1.0)):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", color)
    set_bsdf_input(bsdf, "Metallic", 0.5)
    set_bsdf_input(bsdf, "Roughness", 0.2)
    return mat

def make_emission(name, color, strength=10.0):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", color)
    set_bsdf_input(bsdf, "Emission Color", color)
    set_bsdf_input(bsdf, "Emission Strength", strength)
    return mat

def make_wet_asphalt(name="WetAsphalt"):
    mat = get_or_create_material(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    # Base dark asphalt
    bsdf.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.05

    # Procedural puddle noise texture
    tex_noise = nodes.new(type="ShaderNodeTexNoise")
    tex_noise.inputs["Scale"].default_value = 15.0
    tex_noise.inputs["Detail"].default_value = 4.0
    tex_noise.inputs["Roughness"].default_value = 0.6

    color_ramp = nodes.new(type="ShaderNodeValToRGB")
    color_ramp.color_ramp.elements[0].position = 0.4
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0) # Wet puddle (smooth)
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (0.65, 0.65, 0.65, 1.0) # Dry asphalt

    links.new(tex_noise.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], bsdf.inputs["Roughness"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.75

    return mat

def make_neon_sign(name, color, strength=25.0):
    return make_emission(name, color, strength)

def make_concrete(name="GarageConcrete"):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", (0.12, 0.12, 0.13, 1.0))
    set_bsdf_input(bsdf, "Metallic", 0.0)
    set_bsdf_input(bsdf, "Roughness", 0.75)
    return mat

def make_metal_shutter(name="MetalShutter"):
    mat = get_or_create_material(name)
    bsdf = get_bsdf(mat)
    set_bsdf_input(bsdf, "Base Color", (0.2, 0.22, 0.25, 1.0))
    set_bsdf_input(bsdf, "Metallic", 0.85)
    set_bsdf_input(bsdf, "Roughness", 0.35)
    return mat
