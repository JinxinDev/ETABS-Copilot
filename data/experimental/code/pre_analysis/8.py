"""
Generated ETABS Script
Description: A sequential plan to identify and list all unique reinforcement bar sizes and grades used in the ETABS model by inspecting material properties and frame section rebar assignments.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 20:28:19
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all material property names defined in the ETABS model.
num_of_material, material_names, ret = SapModel.PropMaterial.GetNameList()

# Step 2: Iterate through each material property name. For each material, attempt to retrieve its rebar properties. If the material is a rebar type, extract its grade and add it to a collection of unique rebar grades.
rebar_grades = set()
for material_name in material_names:
    # Attempt to retrieve rebar properties
    # The GetORebar_1 method returns Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransSSDefaults, ret
    # We are interested in Fy (the first return value) and ret (the last return value)
    Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransSSDefaults, ret = SapModel.PropMaterial.GetORebar_1(material_name)
    
    # If ret is 0, the material is a rebar type and properties were successfully retrieved
    if ret == 0:
        rebar_grades.add(Fy)

# Step 3: Retrieve a list of all frame section property names defined in the ETABS model.
num_of_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 4: Iterate through each frame section property name. For each section, attempt to retrieve its beam rebar data and column rebar data. From the successful retrievals, extract the reinforcement bar sizes (e.g., TopBarSize, BotBarSize, TieBarSize, LongitudinalBarSize, TieBarSize) and add them to a collection of unique rebar bar sizes.
rebar_bar_sizes = set()
for frame_section_name in frame_section_names:
    # Attempt to retrieve beam rebar data
    # Note: GetRebarBeam returns areas, not specific bar sizes like '#8'.
    # The provided knowledge does not show how to extract bar sizes from beam rebar data.
    MatPropLong_beam, MatPropConfine_beam, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret_beam = SapModel.PropFrame.GetRebarBeam(frame_section_name)
    
    # Attempt to retrieve column rebar data
    MatPropLong_col, MatPropConfine_col, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned, ret_col = SapModel.PropFrame.GetRebarColumn(frame_section_name)
    
    # If column rebar data was successfully retrieved
    if ret_col == 0:
        if RebarSize and RebarSize != "":
            rebar_bar_sizes.add(RebarSize)
        if TieSize and TieSize != "":
            rebar_bar_sizes.add(TieSize)

# Step 5: Display the unique reinforcement bar grades and bar sizes found throughout the structure.
# Step 5: Display the unique reinforcement bar grades and bar sizes found.
print("\nUnique Rebar Grades Found (Fy in kip):")
if rebar_grades:
    for grade in sorted(list(rebar_grades)):
        print(f"- {grade:.2f} kip")
else:
    print("- No rebar grades found.")

print("\nUnique Rebar Bar Sizes Found:")
if rebar_bar_sizes:
    for size in sorted(list(rebar_bar_sizes)):
        print(f"- {size}")
else:
    print("- No rebar bar sizes found.")