"""
Generated ETABS Script
Description: The script will identify all column elements in the ETABS model, retrieve their axial forces under the 'Dead' load pattern, and then list the names of columns where the axial force exceeds 1000 kips.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:24:49
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined frame section properties in the model.
number_of_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 2: Iterate through all frame section properties and identify which ones are column sections by attempting to retrieve column rebar data. Store the names of these identified column sections.
column_section_names = []
for section_name in frame_section_names:
    # Attempt to retrieve column rebar data. If successful (ret == 0), it's a column section.
    MatPropLong, MatPropConfine, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned, ret = SapModel.PropFrame.GetRebarColumn(section_name)
    if ret == 0:
        column_section_names.append(section_name)

# Step 3: Retrieve the names of all frame objects currently defined in the model.
frame_object_count, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 4: For each frame object, retrieve its assigned frame section property. Filter these frame objects to identify only those that are columns, by checking if their assigned section property is one of the previously identified column sections.
column_frame_objects = []
for frame_name in frame_object_names:
    section_property, _, ret = SapModel.FrameObj.GetSection(frame_name)
    if section_property in column_section_names:
        column_frame_objects.append(frame_name)

# Step 5: For each identified column object, retrieve the axial force (P) from the 'Dead' load pattern. The axial force should be retrieved at one end of the column (e.g., End I).
column_axial_forces_dead = {}
ObjectElm = 0

for column_name in column_frame_objects:
    # Retrieve frame force results for the current column object
    NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret = SapModel.Results.FrameForce(column_name, ObjectElm)

    if ret == 0:
        # Iterate through the results to find the axial force for 'Dead' load pattern at End I (ObjSta = 0.0)
        for i in range(NumberResults):
            if LoadCase[i] == 'Dead' and ObjSta[i] == 0.0:
                column_axial_forces_dead[column_name] = P[i]
                break # Found the axial force at End I for 'Dead' load, move to the next column
    else:
        print(f"Error retrieving frame forces for column: {column_name}, Return code: {ret}")

# Step 6: Iterate through the retrieved axial forces for all columns. Identify and list the names of columns where the axial force from the 'Dead' load is greater than 1000 kips.
columns_with_high_axial_force = []
for column_name, axial_force in column_axial_forces_dead.items():
    if axial_force > 1000:
        columns_with_high_axial_force.append(column_name)
