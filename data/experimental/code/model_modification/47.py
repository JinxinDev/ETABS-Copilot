"""
Generated ETABS Script
Description: Define a new rectangular concrete beam section named 'B14x28' with specified dimensions and concrete material properties.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 19:46:43
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add the concrete material 'f'c 4000 psi' to the model from the United States Customary standard library.
material_name_to_add = "f'c 4000 psi"
mat_type_concrete = 2 # 2 = Concrete
region = "United States"
standard = "Customary"
grade_to_import = "f'c 4000 psi"

# Add the concrete material from the standard library
material_name_returned, ret_code = SapModel.PropMaterial.AddMaterial(material_name_to_add, mat_type_concrete, region, standard, grade_to_import)

# Step 2: Define a new solid rectangular frame section named 'B14x28' with a depth of 28 inches, a width of 14 inches, and assign the 'f'c 4000 psi' concrete material to it.
section_name = "B14x28"
depth_in = 28
width_in = 14
depth_ft = depth_in / 12.0
width_ft = width_in / 12.0
ret_code = SapModel.PropFrame.SetRectangle(section_name, material_name_returned, depth_ft, width_ft)

# Step 3: Assign beam rebar data to the 'B14x28' frame section, specifying it as a concrete beam.
material_name_to_add_rebar = "ASTM A615 Grade 60"
mat_type_rebar = 3
region_rebar = "United States"
standard_rebar = "ASTM"
grade_rebar = "Grade 60"

rebar_material_name_returned, ret_code = SapModel.PropMaterial.AddMaterial(material_name_to_add_rebar, mat_type_rebar, region_rebar, standard_rebar, grade_rebar)

cover_top_in = 2.5
cover_bottom_in = 2.5

cover_top_ft = cover_top_in / 12.0
cover_bottom_ft = cover_bottom_in / 12.0

top_left_rebar_area_sq_in = 2.0
top_right_rebar_area_sq_in = 2.0
bottom_left_rebar_area_sq_in = 3.0
bottom_right_rebar_area_sq_in = 3.0

top_left_rebar_area_sq_ft = top_left_rebar_area_sq_in / (12.0 * 12.0)
top_right_rebar_area_sq_ft = top_right_rebar_area_sq_in / (12.0 * 12.0)
bottom_left_rebar_area_sq_ft = bottom_left_rebar_area_sq_in / (12.0 * 12.0)
bottom_right_rebar_area_sq_ft = bottom_right_rebar_area_sq_in / (12.0 * 12.0)

ret_code = SapModel.PropFrame.SetRebarBeam(section_name, rebar_material_name_returned, rebar_material_name_returned, cover_top_ft, cover_bottom_ft, top_left_rebar_area_sq_ft, top_right_rebar_area_sq_ft, bottom_left_rebar_area_sq_ft, bottom_right_rebar_area_sq_ft)
