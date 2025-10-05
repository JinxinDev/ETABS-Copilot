"""
Generated ETABS Script
Description: Identify the longest and shortest beam spans in the entire ETABS model, reporting their lengths and the names of the corresponding frame objects.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 16:37:59
Steps: 8
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

# Step 2: Initialize variables to store the longest and shortest beam lengths found, along with the names of the corresponding beam objects. Set initial values for longest length to 0 and shortest length to a very large number.
longest_beam_length = 0.0
longest_beam_name = ""
shortest_beam_length = float('inf')
shortest_beam_name = ""

# Step 3: Iterate through each frame object. For each frame object, retrieve the names of its start and end point objects.
for frame_name in frame_ID_tuple:
    pass

# Step 4: For each frame object, retrieve the Cartesian coordinates (X, Y, Z) of its start and end point objects.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_name)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

# Step 5: Determine if the current frame object is a beam by checking if its start and end point Z-coordinates are approximately equal (indicating a horizontal element).
    if abs(Z1 - Z2) < 1e-4:
        # This frame object is considered a beam (horizontal element)
        pass

# Step 6: If the frame object is identified as a beam, calculate its length using the Euclidean distance formula based on its start and end point coordinates.
        import math
        beam_length = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)

# Step 7: Compare the calculated beam length with the current longest and shortest lengths. Update the longest length, shortest length, and their corresponding beam object names if a new maximum or minimum is found.
        if beam_length > longest_beam_length:
            longest_beam_length = beam_length
            longest_beam_name = frame_name
        if beam_length < shortest_beam_length:
            shortest_beam_length = beam_length
            shortest_beam_name = frame_name

# Step 8: Report the name of the longest beam and its calculated length. Report the name of the shortest beam and its calculated length.
print(f"Longest beam: {longest_beam_name} with length {longest_beam_length:.2f} ft")
print(f"Shortest beam: {shortest_beam_name} with length {shortest_beam_length:.2f} ft")