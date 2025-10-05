"""
Generated ETABS Script
Description: Generate a comprehensive report detailing all defined materials, the frame sections that utilize each material, the frame objects assigned to those sections, and a count of frame objects per story.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 16:46:13
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined material properties in the ETABS model.
num_of_material, material_names, ret = SapModel.PropMaterial.GetNameList()

# Step 2: For each material property name, retrieve its basic material property information and then its specific properties (e.g., concrete, steel, rebar, tendon) to gather full details for the report.
all_material_details = []

for material_name in material_names:
    material_data = {"Name": material_name}

    # Get basic material properties
    # The API returns output parameters followed by the return code.
    mat_type, color, notes, guid, ret = SapModel.PropMaterial.GetMaterial(material_name)
    if ret == 0:
        material_data["MatType"] = mat_type
        material_data["Color"] = color
        material_data["Notes"] = notes
        material_data["GUID"] = guid

        # Get specific material properties based on MatType
        # Assuming standard eMatType enumeration values:
        # eConcrete = 1
        # eSteel = 2
        # eRebar = 3
        # eTendon = 4

        if mat_type == 1:  # Concrete
            fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ret = SapModel.PropMaterial.GetOConcrete_1(material_name)
            if ret == 0:
                material_data["ConcreteProperties"] = {
                    "fc": fc,
                    "IsLightweight": is_lightweight,
                    "fcsFactor": fcs_factor,
                    "SSType": ss_type,
                    "SSHysType": ss_hys_type,
                    "StrainAtfc": strain_at_fc,
                    "StrainUltimate": strain_ultimate,
                    "FinalSlope": final_slope,
                    "FrictionAngle": friction_angle,
                    "DilatationalAngle": dilatational_angle
                }
        elif mat_type == 2:  # Steel
            # Temp is an optional parameter with default 0, so it's omitted in the call.
            fy, fu, efy, efu, ss_type, ss_hys_type, strain_at_hardening, strain_at_max_stress, strain_at_rupture, final_slope, ret = SapModel.PropMaterial.GetOSteel_1(material_name)
            if ret == 0:
                material_data["SteelProperties"] = {
                    "Fy": fy,
                    "Fu": fu,
                    "EFy": efy,
                    "EFu": efu,
                    "SSType": ss_type,
                    "SSHysType": ss_hys_type,
                    "StrainAtHardening": strain_at_hardening,
                    "StrainAtMaxStress": strain_at_max_stress,
                    "StrainAtRupture": strain_at_rupture,
                    "FinalSlope": final_slope
                }
        elif mat_type == 3:  # Rebar
            # The example for GetORebar_1 includes UseCaltransSSDefaults in the return tuple.
            fy, fu, efy, efu, ss_type, ss_hys_type, strain_at_hardening, strain_ultimate, final_slope, use_caltrans_ss_defaults, ret = SapModel.PropMaterial.GetORebar_1(material_name)
            if ret == 0:
                material_data["RebarProperties"] = {
                    "Fy": fy,
                    "Fu": fu,
                    "EFy": efy,
                    "EFu": efu,
                    "SSType": ss_type,
                    "SSHysType": ss_hys_type,
                    "StrainAtHardening": strain_at_hardening,
                    "StrainUltimate": strain_ultimate,
                    "FinalSlope": final_slope,
                    "UseCaltransSSDefaults": use_caltrans_ss_defaults
                }
        elif mat_type == 4:  # Tendon
            # Temp is an optional parameter with default 0, so it's omitted in the call.
            fy, fu, ss_type, ss_hys_type, final_slope, ret = SapModel.PropMaterial.GetOTendon_1(material_name)
            if ret == 0:
                material_data["TendonProperties"] = {
                    "Fy": fy,
                    "Fu": fu,
                    "SSType": ss_type,
                    "SSHysType": ss_hys_type,
                    "FinalSlope": final_slope
                }
        # Other material types (e.g., Aluminum, ColdFormed, NoDesign, Other) are not handled
        # as specific GetO..._1 methods were not provided in the JIT knowledge for them.
    
    all_material_details.append(material_data)

# The 'all_material_details' list now contains all gathered material property information.

# Step 3: Retrieve select data for all frame properties in the model, which includes the material assigned to each frame section. This will establish the link between frame sections and materials.
# Define the mapping for frame property types as shown in the example.
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

# Call the function to get all frame property definitions.
# The API returns output parameters followed by the return code.
# Note: Based on the provided JIT knowledge for GetAllFrameProperties, 
# the material assigned to each frame section is not directly returned by this method.
num_names, my_name, prop_type, t3, t2, tf, tw, t2b, tfb, ret = SapModel.PropFrame.GetAllFrameProperties()

all_frame_section_details = []

if ret == 0:
    for i in range(num_names):
        section_name = my_name[i]
        section_type_code = prop_type[i]
        section_type_name = prop_type_map.get(section_type_code, "Unknown") # Use .get() for robustness
        
        section_data = {
            "Name": section_name,
            "Type": section_type_name,
            "Depth (t3)": t3[i],
            "Width (t2)": t2[i]
        }
        
        # Add flange/web thickness only if it's a relevant shape as per the example (I, Channel, T, DblAngle)
        if section_type_code in [1, 2, 3, 5]: 
            section_data["FlangeThk (tf)"] = tf[i]
            section_data["WebThk (tw)"] = tw[i]
        
        all_frame_section_details.append(section_data)

# The 'all_frame_section_details' list now contains all gathered frame section property information.

# Step 4: Retrieve the names of all defined stories in the ETABS model.
# Step 4: Retrieve the names of all defined stories in the ETABS model.
# The API returns output parameters followed by the return code.
num_stories, story_names, ret = SapModel.Story.GetNameList()

all_story_names = []
if ret == 0:
    all_story_names = list(story_names)

# The 'all_story_names' list now contains the names of all stories.

# Step 5: For each story, retrieve the names of all frame objects located on that story.
# Step 5: For each story, retrieve the names of all frame objects located on that story.
story_frame_objects = {}

for story_name in all_story_names:
    # The API returns output parameters followed by the return code.
    frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    if ret == 0:
        story_frame_objects[story_name] = list(frame_ID_tuple)
    else:
        story_frame_objects[story_name] = [] # Store an empty list if no frames or error

# The 'story_frame_objects' dictionary now maps each story name to a list of frame object names on that story.

# Step 6: For each frame object identified, retrieve the name of the frame section property assigned to it. This will link frame objects to their respective sections.
frame_object_sections = {}

for story_name, frame_ids_on_story in story_frame_objects.items():
    for frame_id in frame_ids_on_story:
        # The API returns output parameters followed by the return code.
        # We are interested in the section_property name.
        section_property, _, ret = SapModel.FrameObj.GetSection(frame_id)
        if ret == 0:
            frame_object_sections[frame_id] = section_property
print(frame_object_sections)
# The 'frame_object_sections' dictionary now maps each frame object name to its assigned section property name.