"""
Generated ETABS Script
Description: A sequential plan to create custom concrete and rebar materials, define multiple rectangular concrete frame sections using the custom concrete, and then assign rebar reinforcement to one of the column sections.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-12 10:31:11
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
sap_model = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Initialize a new user-defined concrete material named 'C4000'.
ret = sap_model.PropMaterial.SetMaterial("C4000", 2)

# Step 2: Set the properties for the 'C4000' concrete material, including a compressive strength of 4.0 ksi, an elastic modulus of 3605 ksi, and a unit weight of 0.15 kip/ft³.
ret = sap_model.PropMaterial.SetOConcrete_1("C4000", 576.0, False, 0, 1, 2, 0.0022, 0.0052, -0.1, 0, 0)

# Step 3: Add a standard Grade 60 rebar material from the ETABS library. The region should be 'United States', the standard 'ASTM A615', and the grade 'Grade 60'. This material will have a yield strength of 60 ksi and an elastic modulus of 29000 ksi.
ret = sap_model.PropMaterial.AddMaterial("Rebar_Grade60", 6, "United States", "ASTM A615", "Grade 60")

# Step 4: Create a new rectangular frame section named '18x18COL' with dimensions 18 inches by 18 inches, using the 'C4000' concrete material.
section_name = "18x18COL"
concrete_material_name = "C4000"
depth_ft = 18.0 / 12.0
width_ft = 18.0 / 12.0

ret = sap_model.PropFrame.SetRectangle(section_name, concrete_material_name, depth_ft, width_ft)

# Step 5: Create a new rectangular frame section named '12x24BEAM' with dimensions 12 inches by 24 inches, using the 'C4000' concrete material.
section_name_beam = "12x24BEAM"
concrete_material_name = "C4000"
depth_beam_ft = 24.0 / 12.0
width_beam_ft = 12.0 / 12.0

ret = sap_model.PropFrame.SetRectangle(section_name_beam, concrete_material_name, depth_beam_ft, width_beam_ft)

# Step 6: Create a new rectangular frame section named '16x20COL' with dimensions 16 inches by 20 inches, using the 'C4000' concrete material.
section_name_col_new = "16x20COL"
depth_col_new_ft = 20.0 / 12.0
width_col_new_ft = 16.0 / 12.0

ret = sap_model.PropFrame.SetRectangle(section_name_col_new, concrete_material_name, depth_col_new_ft, width_col_new_ft)

# Step 7: Assign default column rebar reinforcement to the '18x18COL' section. This will use the previously defined rebar material and default reinforcement parameters.
# Assign default column rebar reinforcement to the '18x18COL' section.
# Use the previously defined rebar material and default reinforcement parameters.

rebar_material_name = "Rebar_Grade60"

# Reinforcement parameters (consistent with kip_ft_F units)
rebar_pattern = 1              # 1 = Rectangular
confinement_type = 1           # 1 = Ties
cover_to_ties_ft = 1.5 / 12.0  # Clear cover in feet (1.5 inches)
num_bars_along_3_face = 4      # Number of bars along the 3-axis face
num_bars_along_2_face = 4      # Number of bars along the 2-axis face
longitudinal_bar_size = "#8"
tie_bar_size = "#3"
tie_spacing_longit_ft = 6.0 / 12.0 # Longitudinal spacing of ties in feet (6 inches)
num_tie_legs_in_2_dir = 2      # Number of tie legs in the local 2-axis direction
num_tie_legs_in_3_dir = 2      # Number of tie legs in the local 3-axis direction
to_be_designed = False         # False = Check section, True = Design section

ret = sap_model.PropFrame.SetRebarColumn(
    section_name,              # Name: '18x18COL' from Step 4
    rebar_material_name,       # MatPropLong
    rebar_material_name,       # MatPropConfine
    rebar_pattern,
    confinement_type,
    cover_to_ties_ft,
    0,                         # NumberCBars (must be 0 for rectangular pattern)
    num_bars_along_3_face,
    num_bars_along_2_face,
    longitudinal_bar_size,
    tie_bar_size,
    tie_spacing_longit_ft,
    num_tie_legs_in_2_dir,
    num_tie_legs_in_3_dir,
    to_be_designed
)