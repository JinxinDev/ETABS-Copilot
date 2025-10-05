"""
Generated ETABS Script
Description: Identify the top 10 columns with the highest axial load from the 'Dead' load case in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 17:42:27
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects defined in the model.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 2: For each frame object, determine if it is a column by checking its assigned section property. This involves retrieving the section property name for each frame object and then attempting to get column-specific rebar data for that section. If the operation succeeds, the frame object is considered a column.
column_frame_IDs = []

for frame_ID in frame_ID_tuple:
    section_property, _, ret = SapModel.FrameObj.GetSection(frame_ID)
    
    # Attempt to get column rebar data for the section property
    # The return value 'ret_rebar' will be 0 if it's a concrete column section with rebar data
    _, _, _, _, _, _, _, _, _, _, _, _, _, _, ret_rebar = SapModel.PropFrame.GetRebarColumn(section_property)
    
    if ret_rebar == 0:
        column_frame_IDs.append(frame_ID)

# Step 3: Retrieve the axial forces for all identified column objects under the 'Dead' load case. The axial force (P) at the I-end or J-end of each column will be considered for comparison.
column_axial_forces = {}
for frame_ID in column_frame_IDs:
    # Retrieve frame force results for the current column under the 'Dead' load case
    # ObjectElm = 0 indicates that results are requested for the object itself
    NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret = SapModel.Results.FrameForce(frame_ID, 0)
    # Filter results for the 'Dead' load case and store the axial force (P)
    # We are interested in the axial force at either end (I-end or J-end), so we can take the first P value if multiple are returned.
    # The P values are typically negative for compression in columns.
    axial_forces_for_column = []
    for i in range(NumberResults):
        if LoadCase[i] == 'Dead':
            axial_forces_for_column.append(P[i])
    
    if axial_forces_for_column:
        # Store the first axial force found for the 'Dead' load case for this column
        # This assumes we only need one representative axial force (e.g., at the I-end or J-end)
        column_axial_forces[frame_ID] = axial_forces_for_column[0]

# Step 4: Process the retrieved axial forces, sort the columns in descending order based on their axial load, and identify the top 10 columns with the highest axial load.
sorted_columns = sorted(column_axial_forces.items(), key=lambda item: abs(item[1]), reverse=True)
top_10_columns = sorted_columns[:10]
