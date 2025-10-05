"""
Generated ETABS Script
Description: This script will verify that all concrete frame objects in the ETABS model use a material with a compressive strength of at least 4000 psi and will flag any that do not meet this criterion.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-19 16:56:15
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve a list of all frame object names currently defined in the ETABS model.
frame_obj_count, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 2: Create a mapping (dictionary) from frame section property names to their assigned material names. This involves retrieving all frame section properties and their associated material data.
# Retrieve all frame section properties
num_names, my_name, prop_type, t3, t2, tf, tw, t2b, tfb, ret = SapModel.PropFrame.GetAllFrameProperties()

# Create a mapping from section type codes to names for easier identification
prop_type_map = {
    1: "I",
    2: "Channel",
    3: "T",
    4: "Angle",
    5: "DblAngle",
    6: "Box",
    7: "Pipe",
    8: "Rectangular",
    9: "Circle",
    10: "General"
}

# Initialize the dictionary to store frame section name to material name mapping
frame_section_material_map = {}

# Iterate through each frame section property
for i in range(num_names):
    section_name = my_name[i]
    section_type_code = prop_type[i]
    section_type_name = prop_type_map.get(section_type_code, "Unknown")

    # The provided knowledge only includes GetISection_1 for retrieving material properties.
    # Therefore, material names can only be retrieved for I-sections.
    if section_type_code == 1:  # I-section
        # Retrieve detailed properties for the I-section, including its material
        # The parameters for GetISection_1 are: Name (input), FileName, MatProp, T3, T2, Tf, Tw, T2b, Tfb, FilletRadius, Color, Notes, GUID (all outputs)
        file_name, material_name, section_t3, section_t2, section_tf, section_tw, section_t2b, section_tfb, fillet_radius, color, notes, guid, ret = SapModel.PropFrame.GetISection_1(section_name)
        
        if ret == 0: # Check for successful retrieval
            frame_section_material_map[section_name] = material_name
        else:
            # Handle error or log that material could not be retrieved
            frame_section_material_map[section_name] = "Error: Material not retrieved"
    else:
        # For other section types, material retrieval is not supported by the provided knowledge.
        frame_section_material_map[section_name] = f"N/A (Type: {section_type_name}, No specific Get method in knowledge)"

# The frame_section_material_map now contains the mapping for I-sections and placeholders for others.

# Step 3: Create a mapping (dictionary) from material names to their concrete compressive strength (Fc) for all concrete materials in the model. First, get a list of all defined material names. Then, for each material, determine its type. If it is a concrete material, retrieve its specific concrete properties, including the Fc value.
# Initialize the dictionary to store concrete material name to Fc mapping
concrete_material_fc_map = {}

# Retrieve a list of all defined material names
num_of_material, material_names, ret = SapModel.PropMaterial.GetNameList()

# Iterate through each material name
for material_name in material_names:
    # Retrieve basic material properties to determine its type
    # The parameters for GetMaterial are: Name (input), MatType, Color, Notes, GUID (all outputs)
    mat_type, color, notes, guid, ret = SapModel.PropMaterial.GetMaterial(material_name)
    
    # Check if the material type is concrete (eMatType = 2, based on example)
    if ret == 0 and mat_type == 2: # 2 is assumed to be the eMatType for Concrete
        # Retrieve other material property data for concrete materials
        # The parameters for GetOConcrete_1 are: Name (input), Fc, IsLightweight, fcsFactor, SSType, SSHysType, StrainAtFc, StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle (all outputs)
        fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ret = SapModel.PropMaterial.GetOConcrete_1(material_name)
        
        if ret == 0:
            concrete_material_fc_map[material_name] = fc
        else:
            concrete_material_fc_map[material_name] = "Error: Fc not retrieved"
    elif ret != 0:
        concrete_material_fc_map[material_name] = "Error: Material type not retrieved"
    # For non-concrete materials, we don't add them to this specific map


# Step 4: Initialize an empty list to store the names of concrete frame objects that do not meet the 4000 psi compressive strength requirement.
non_compliant_concrete_frames = []

# Step 5: Iterate through each frame object name. For each frame object, get its assigned frame section property. Then, use the section-to-material mapping to find the material name. Check if this material is concrete and if its compressive strength (Fc) is less than 4000 psi. If it is, add the frame object's name to the non-compliant list.
for frame_obj_name in frame_object_names:
    # Get the assigned section property for the current frame object
    # The parameters for GetSection are: Name (input), PropName, Suffix (all outputs)
    section_prop_name, suffix, ret = SapModel.FrameObj.GetSection(frame_obj_name)

    if ret == 0: # Check for successful retrieval
        # Use the section-to-material mapping to find the material name
        material_name = frame_section_material_map.get(section_prop_name)

        # Check if the material name is valid and exists in the concrete Fc map
        if material_name and material_name in concrete_material_fc_map:
            fc_value = concrete_material_fc_map.get(material_name)

            # Ensure fc_value is a number before comparison
            if isinstance(fc_value, (int, float)):
                # Convert 4000 psi to ksf for comparison (1 kip = 1000 lb, 1 ft^2 = 144 in^2)
                # 4000 psi = 4000 lb/in^2 = (4000/1000) kip / (1/144) ft^2 = 4 * 144 ksf = 576 ksf
                required_fc_ksf = 576.0 # 4000 psi converted to ksf
                
                if fc_value < required_fc_ksf:
                    non_compliant_concrete_frames.append(frame_obj_name)
print(concrete_material_fc_map)
# Step 6: Report the names of all frame objects found in the non-compliant list, indicating which concrete frame objects use materials with less than 4000 psi compressive strength.
if non_compliant_concrete_frames:
    print("\nNon-compliant concrete frame objects (Fc < 4000 psi):")
    for frame_name in non_compliant_concrete_frames:
        print(f"- {frame_name}")
else:
    print("\nAll concrete frame objects meet the 4000 psi compressive strength requirement.")