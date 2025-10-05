"""
Generated ETABS Script
Description: This script will count the total number of structural elements by type: columns, beams, and slabs, present in the active ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-19 16:50:23
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects defined in the model.
frame_obj_num, frame_names, ret = SapModel.FrameObj.GetNameList()

# Step 2: Initialize counters for columns and beams to zero.
column_count = 0
beam_count = 0

# Step 3: Iterate through each retrieved frame object. For each frame object, determine its defining point objects and retrieve their Cartesian coordinates (X, Y, Z). Compare the Z-coordinates of the start and end points to classify the frame object: if the absolute difference in Z-coordinates is significant (indicating a vertical element), increment the column counter; otherwise (indicating a horizontal element), increment the beam counter.
for frame_ID in frame_names:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Define a small tolerance for Z-coordinate difference to classify as vertical/horizontal
    z_tolerance = 0.1 # feet

    if abs(Z1 - Z2) > z_tolerance:
        column_count += 1
    else:
        beam_count += 1

# Step 4: Retrieve the names of all area objects defined in the model.
area_obj_num, area_names, ret = SapModel.AreaObj.GetNameList()

# Step 5: Initialize a counter for slabs to zero.
slab_count = 0

# Step 6: Iterate through each retrieved area object. For each area object, get the name of its assigned property. Then, attempt to retrieve the slab property data for that property name. If the retrieval is successful, it indicates the area object is a slab, and the slab counter should be incremented.
for area_ID in area_names:
    prop_name, ret = SapModel.AreaObj.GetProperty(area_ID)
    # Attempt to get slab property data. If successful, it's a slab.
    # We don't need the actual data, just the success/failure of the call.
    SlabType, ShellType, MatProp, Thickness, color, notes, GUID, ret = SapModel.PropArea.GetSlab(prop_name)
    if ret == 0:
        slab_count += 1

# Step 7: Report the final counts for columns, beams, and slabs.
print("Number of columns:", column_count)
print("Number of beams:", beam_count)
print("Number of slabs:", slab_count)