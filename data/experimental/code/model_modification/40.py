"""
Generated ETABS Script
Description: Create a new custom concrete material, then define three rectangular concrete sections (columns, beams, and slabs) using this new material, and assign Grade 60 rebar to the frame sections.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-12 11:07:57
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add the 'Grade 60' rebar material to the model from the standard library. The region is 'United States', standard is 'ASTM A615/A615M', and grade is 'Grade 60'.
rebar_material_name = "Grade 60"
mat_type_rebar = 6 # 6 = Rebar
region = "United States"
standard = "ASTM A615/A615M"
grade = "Grade 60"

material_name_added, ret_code = SapModel.PropMaterial.AddMaterial(
    rebar_material_name,
    mat_type_rebar,
    region,
    standard,
    grade
)

if ret_code == 0:
    print(f"Successfully added rebar material: {material_name_added}")
else:
    print(f"Error adding rebar material {rebar_material_name}. Return code: {ret_code}")

# Step 2: Initialize a new user-defined concrete material named 'CONC_4.5ksi'.
concrete_material_name = "CONC_4.5ksi"
mat_type_concrete = 2 # 2 = Concrete

ret_code = SapModel.PropMaterial.SetMaterial(
    concrete_material_name,
    mat_type_concrete
)

if ret_code == 0:
    print(f"Successfully initialized concrete material: {concrete_material_name}")
else:
    print(f"Error initializing concrete material {concrete_material_name}. Return code: {ret_code}")

# Step 3: Set the properties for the 'CONC_4.5ksi' concrete material, including fc = 4.5 ksi, Ec = 4030 ksi, and unit weight = 0.15 kcf.
# Step 3: Set the properties for the 'CONC_4.5ksi' concrete material.
# Note: Based on the provided Just-in-Time Knowledge, only Fc and other stress-strain curve parameters can be set using SetOConcrete_1.
# Properties like Ec and unit weight are not available through this specific method in the provided knowledge.
fc_value = 4.5 # ksi

# Default values for other parameters are taken from the provided examples, as they were not specified in the prompt.
is_lightweight = False
fcs_factor = 0.0
ss_type = 1 # Parametric - Simple
ss_hys_type = 2 # Takeda
strain_at_fc = 0.0022
strain_ultimate = 0.0052
final_slope = -0.1
friction_angle = 0.0
dilatational_angle = 0.0

ret_code = SapModel.PropMaterial.SetOConcrete_1(
    concrete_material_name,
    fc_value,
    is_lightweight,
    fcs_factor,
    ss_type,
    ss_hys_type,
    strain_at_fc,
    strain_ultimate,
    final_slope,
    friction_angle,
    dilatational_angle
)

if ret_code == 0:
    print(f"Successfully set properties for concrete material: {concrete_material_name} (Fc={fc_value} ksi)")
else:
    print(f"Error setting properties for concrete material {concrete_material_name}. Return code: {ret_code}")

# Step 4: Initialize a new solid rectangular frame section property named 'COL_18x24' with a depth of 24 inches and a width of 18 inches, assigning the 'CONC_4.5ksi' material.
# Step 4: Initialize a new solid rectangular frame section property named 'COL_18x24'.
section_name_column = "COL_18x24"
depth_column_in = 24 # inches
width_column_in = 18 # inches

# Convert dimensions from inches to feet for ETABS API (kip_ft_F unit system)
depth_column_ft = depth_column_in / 12.0
width_column_ft = width_column_in / 12.0

ret_code = SapModel.PropFrame.SetRectangle(
    section_name_column,
    concrete_material_name, # Material name from Step 2
    depth_column_ft,        # Depth in feet
    width_column_ft         # Width in feet
)

if ret_code == 0:
    print(f"Successfully initialized rectangular frame section: {section_name_column} (Depth={depth_column_in}in, Width={width_column_in}in) with material {concrete_material_name}")
elif ret_code == 1:
    print(f"Warning: Rectangular frame section {section_name_column} already exists and was reset. Return code: {ret_code}")
else:
    print(f"Error initializing rectangular frame section {section_name_column}. Return code: {ret_code}")

# Step 5: Assign 'Grade 60' rebar to the 'COL_18x24' column section.
# Step 5: Assign 'Grade 60' rebar to the 'COL_18x24' column section.
# Define rebar properties for the column section.
rebar_pattern = 1              # 1 = Rectangular
confinement_type = 1           # 1 = Ties
cover_to_ties_in = 1.5         # inches

# Convert cover to feet for ETABS API (kip_ft_F unit system)
cover_to_ties_ft = cover_to_ties_in / 12.0

# Assuming typical reinforcement for an 18x24 column
num_bars_along_3_face = 4      # Number of bars along the 24" depth (3-axis)
num_bars_along_2_face = 3      # Number of bars along the 18" width (2-axis)
longitudinal_bar_size = "#8"
tie_bar_size = "#3"
tie_spacing_in = 6.0            # inches

# Convert tie spacing to feet
tie_spacing_ft = tie_spacing_in / 12.0

num_tie_legs_in_2_dir = 2      # Assuming a simple perimeter tie (2 legs)
num_tie_legs_in_3_dir = 2      # Assuming a simple perimeter tie (2 legs)
to_be_designed = False         # False = Check section (rebar is provided)

ret_code = SapModel.PropFrame.SetRebarColumn(
    section_name_column,       # Name of the frame section
    material_name_added,       # MatPropLong (Longitudinal rebar material)
    material_name_added,       # MatPropConfine (Confinement rebar material)
    rebar_pattern,             # Pattern (1=Rectangular)
    confinement_type,          # ConfineType (1=Ties)
    cover_to_ties_ft,          # Cover (Clear cover to confinement steel in feet)
    0,                         # NumberCBars (MUST be 0 for rectangular pattern)
    num_bars_along_3_face,     # NumberR3Bars (Bars along 3-axis face)
    num_bars_along_2_face,     # NumberR2Bars (Bars along 2-axis face)
    longitudinal_bar_size,     # RebarSize (Longitudinal bar size)
    tie_bar_size,              # TieSize (Confinement bar size)
    tie_spacing_ft,            # TieSpacingLongit (Longitudinal tie spacing in feet)
    num_tie_legs_in_2_dir,     # Number2DirTieBars (Tie legs in 2-direction)
    num_tie_legs_in_3_dir,     # Number3DirTieBars (Tie legs in 3-direction)
    to_be_designed             # ToBeDesigned (False for checking)
)

if ret_code == 0:
    print(f"Successfully assigned rebar to column section: {section_name_column} with material {rebar_material_name}")
else:
    print(f"Error assigning rebar to column section {section_name_column}. Return code: {ret_code}")

# Step 6: Initialize a new solid rectangular frame section property named 'BEAM_14x30' with a depth of 30 inches and a width of 14 inches, assigning the 'CONC_4.5ksi' material.
# Step 6: Initialize a new solid rectangular frame section property named 'BEAM_14x30' with a depth of 30 inches and a width of 14 inches, assigning the 'CONC_4.5ksi' material.
section_name_beam = "BEAM_14x30"
depth_beam_in = 30 # inches
width_beam_in = 14 # inches

# Convert dimensions from inches to feet for ETABS API (kip_ft_F unit system)
depth_beam_ft = depth_beam_in / 12.0
width_beam_ft = width_beam_in / 12.0

ret_code = SapModel.PropFrame.SetRectangle(
    section_name_beam,
    concrete_material_name, # Material name from Step 2
    depth_beam_ft,          # Depth in feet (T3)
    width_beam_ft           # Width in feet (T2)
)

if ret_code == 0:
    print(f"Successfully initialized rectangular frame section: {section_name_beam} (Depth={depth_beam_in}in, Width={width_beam_in}in) with material {concrete_material_name}")
elif ret_code == 1:
    print(f"Warning: Rectangular frame section {section_name_beam} already exists and was reset. Return code: {ret_code}")
else:
    print(f"Error initializing rectangular frame section {section_name_beam}. Return code: {ret_code}")

# Step 7: Assign 'Grade 60' rebar to the 'BEAM_14x30' beam section.
# Step 7: Assign 'Grade 60' rebar to the 'BEAM_14x30' beam section.
# Define rebar properties for the beam section.
cover_top_in = 2.5                 # inches (clear cover to top longitudinal rebar)
cover_bottom_in = 2.5              # inches (clear cover to bottom longitudinal rebar)

# Convert cover to feet for ETABS API (kip_ft_F unit system)
cover_top_ft = cover_top_in / 12.0
cover_bottom_ft = cover_bottom_in / 12.0

# Typical rebar areas (square inches) - these are example values and should be adjusted based on design.
# Convert to square feet for ETABS API (kip_ft_F unit system)
top_left_rebar_area_sqin = 2.0     # Top reinforcement at left end
top_right_rebar_area_sqin = 2.0    # Top reinforcement at right end
bottom_left_rebar_area_sqin = 3.0  # Bottom reinforcement at left end
bottom_right_rebar_area_sqin = 3.0 # Bottom reinforcement at right end

top_left_rebar_area_sqft = top_left_rebar_area_sqin / 144.0
top_right_rebar_area_sqft = top_right_rebar_area_sqin / 144.0
bottom_left_rebar_area_sqft = bottom_left_rebar_area_sqin / 144.0
bottom_right_rebar_area_sqft = bottom_right_rebar_area_sqin / 144.0

ret_code = SapModel.PropFrame.SetRebarBeam(
    section_name_beam,             # Name of the frame section
    material_name_added,           # MatPropLong (Longitudinal rebar material)
    material_name_added,           # MatPropConfine (Confinement rebar material - stirrups)
    cover_top_ft,                  # CoverTop (Distance from top of beam to centroid of top rebar)
    cover_bottom_ft,               # CoverBot (Distance from bottom of beam to centroid of bottom rebar)
    top_left_rebar_area_sqft,      # TopLeftArea (Total area of top rebar at left end)
    top_right_rebar_area_sqft,     # TopRightArea (Total area of top rebar at right end)
    bottom_left_rebar_area_sqft,   # BotLeftArea (Total area of bottom rebar at left end)
    bottom_right_rebar_area_sqft   # BotRightArea (Total area of bottom rebar at right end)
)

if ret_code == 0:
    print(f"Successfully assigned rebar to beam section: {section_name_beam} with material {rebar_material_name}")
else:
    print(f"Error assigning rebar to beam section {section_name_beam}. Return code: {ret_code}")

# Step 8: Initialize a new slab property named 'SLAB_8in' with a thickness of 8 inches, assigning the 'CONC_4.5ksi' material.
# Step 8: Initialize a new slab property named 'SLAB_8in' with a thickness of 8 inches, assigning the 'CONC_4.5ksi' material.
slab_name = "SLAB_8in"
slab_thickness_in = 8 # inches

# Convert thickness from inches to feet for ETABS API (kip_ft_F unit system)
slab_thickness_ft = slab_thickness_in / 12.0

# Define slab type and shell type based on ETABS enums
ESLABTYPE_SLAB = 0 # From provided knowledge
ESHELLTYPE_SHELLTHIN = 1 # From provided knowledge

ret_code = SapModel.PropArea.SetSlab(
    slab_name,
    ESLABTYPE_SLAB,
    ESHELLTYPE_SHELLTHIN,
    concrete_material_name, # Material name from Step 2
    slab_thickness_ft
)

if ret_code == 0:
    print(f"Successfully initialized slab property: {slab_name} (Thickness={slab_thickness_in}in) with material {concrete_material_name}")
elif ret_code == 1:
    print(f"Warning: Slab property {slab_name} already exists and was reset. Return code: {ret_code}")
else:
    print(f"Error initializing slab property {slab_name}. Return code: {ret_code}")