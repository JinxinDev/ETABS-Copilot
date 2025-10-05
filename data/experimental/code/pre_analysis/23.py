"""
Generated ETABS Script
Description: This script will identify all concrete beam sections in the ETABS model where the specified longitudinal rebar grade is not 'Grade 60'. It will iterate through all frame section properties, filter for concrete beam sections, retrieve their longitudinal rebar material properties, and then check the rebar grade.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-21 10:36:35
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve a list of all defined frame section property names in the model.
num_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 2: Iterate through each frame section property name. For each name, attempt to retrieve its beam rebar data. If the retrieval is successful, it indicates that the section is a concrete beam section. Store the name of the concrete beam section and the name of its longitudinal rebar material.
concrete_beam_sections_data = []
for section_name in frame_section_names:
    MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret = SapModel.PropFrame.GetRebarBeam(section_name)
    if ret == 0:
        concrete_beam_sections_data.append({"section_name": section_name, "longitudinal_rebar_material": MatPropLong})

# Step 3: For each identified concrete beam section, use the stored longitudinal rebar material name to retrieve its detailed material properties, specifically the rebar grade.
for beam_data in concrete_beam_sections_data:
    material_name = beam_data["longitudinal_rebar_material"]
    Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransSSDefaults, ret = SapModel.PropMaterial.GetORebar_1(material_name)
    if ret == 0:
        beam_data["rebar_grade"] = Fy

# Step 4: Compare the retrieved rebar grade with the target grade 'Grade 60'. If the rebar grade is not 'Grade 60', add the concrete beam section name to a list of non-conforming sections.
non_conforming_sections = []
for beam_data in concrete_beam_sections_data:
    if beam_data["rebar_grade"] != 60.0:
        non_conforming_sections.append(beam_data["section_name"])

# Step 5: Report the names of all concrete beam sections found where the longitudinal rebar grade is not 'Grade 60'.
if non_conforming_sections:
    print("Concrete beam sections with longitudinal rebar grade not 'Grade 60':")
    for section_name in non_conforming_sections:
        print(f"- {section_name}")
else:
    print("All concrete beam sections found have longitudinal rebar grade 'Grade 60'.")