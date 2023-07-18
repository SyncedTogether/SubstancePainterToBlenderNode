import bpy
import os

# Function to create a new material with the given name
def create_material(name):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    return material

# Set the directory containing the texture sets
image_directory = r"D:\!3D\Maps\mp_market\v4\buildings\torch"

# Get a list of image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Create dictionaries to organize the textures by their names
textures_by_name = {}
for image_file in image_files:
    name = os.path.splitext(image_file)[0].split("_")[0]
    if name not in textures_by_name:
        textures_by_name[name] = []
    textures_by_name[name].append(image_file)
    
print(f"Found {len(image_files)} image files in the directory.")

# Iterate through each texture set and create materials
for name, textures in textures_by_name.items():
    # Generate the material name with "Gen_" prefix
    material_name = "Gen_" + name
    
    print(f"Creating material: {material_name}")

    # Create a new material
    material = create_material(material_name)

    # Create Principled BSDF node
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    if principled_bsdf is None:
        principled_bsdf = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf.location = (0, 0)

    # Create Texture nodes for base_color and mixed_ao
    base_color_texture = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    base_color_texture.location = (-300, 0)
    base_color_texture.image = bpy.data.images.load(os.path.join(image_directory, textures[0]))
    base_color_texture.image.colorspace_settings.name = 'sRGB'

    mixed_ao_texture = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    mixed_ao_texture.location = (-300, -200)
    mixed_ao_texture.image = bpy.data.images.load(os.path.join(image_directory, textures[3]))
    mixed_ao_texture.image.colorspace_settings.name = 'Non-Color'

    # Create MixRGB node for color blending
    color_mix = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
    color_mix.location = (300, 0)
    color_mix.blend_type = 'MULTIPLY'

    # Connect Base Color and Mixed AO to Color Mix node
    material.node_tree.links.new(base_color_texture.outputs["Color"], color_mix.inputs[1])
    material.node_tree.links.new(mixed_ao_texture.outputs["Color"], color_mix.inputs[2])

    # Connect Color Mix output to Principled BSDF Base Color
    material.node_tree.links.new(color_mix.outputs["Color"], principled_bsdf.inputs["Base Color"])

    # Create Metallic and Roughness inputs (set color space as needed)
    metallic_texture = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    metallic_texture.location = (-300, -400)
    metallic_texture.image = bpy.data.images.load(os.path.join(image_directory, textures[2]))
    metallic_texture.image.colorspace_settings.name = 'Non-Color'

    roughness_texture = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    roughness_texture.location = (-300, -600)
    roughness_texture.image = bpy.data.images.load(os.path.join(image_directory, textures[6]))
    roughness_texture.image.colorspace_settings.name = 'Non-Color'

    # Connect Metallic and Roughness inputs
    material.node_tree.links.new(metallic_texture.outputs["Color"], principled_bsdf.inputs["Metallic"])
    material.node_tree.links.new(roughness_texture.outputs["Color"], principled_bsdf.inputs["Roughness"])

    # Create Normal Map node and set color space
    normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.location = (0, -800)

    # Use the Normal_OpenGL.jpg as the normal map
    normal_map_texture = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    normal_map_texture.location = (-300, -800)
    normal_map_texture.image = bpy.data.images.load(os.path.join(image_directory, textures[5]))
    normal_map_texture.image.colorspace_settings.name = 'Non-Color'

    # Connect Normal Map to Normal Map node to Principled BSDF
    material.node_tree.links.new(normal_map_texture.outputs["Color"], normal_map_node.inputs["Color"])
    material.node_tree.links.new(normal_map_node.outputs["Normal"], principled_bsdf.inputs["Normal"])

    # Create Material Output node
    material_output = material.node_tree.nodes.get("Material Output")
    if material_output is None:
        material_output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (600, 0)
    material.node_tree.links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])
    
    print(f"Material {material_name} created with the following textures:")
    print(f"Base Color: {textures[0]}")
    print(f"Mixed AO: {textures[3]}")
    print(f"Metallic: {textures[2]}")
    print(f"Roughness: {textures[6]}")
    print(f"Normal Map: {textures[5]}")
    print()

print("All materials created successfully.")
