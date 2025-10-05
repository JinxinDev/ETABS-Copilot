"""
Generated ETABS Script
Description: Identify all beams in the model that are shorter than 10 feet and update their section property to 'B12x20'.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 15:34:08
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects currently defined in the model.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 2: For each frame object, determine if it is a beam (horizontal element) and retrieve the coordinates of its start and end points to calculate its length. This step assumes a mechanism to get the point names associated with each frame object.
import math

beam_data = {}
tolerance_z = 0.001 # feet, for checking if Z coordinates are approximately equal

for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Determine if it's a beam (horizontal element) by checking Z-coordinates
    if abs(Z1 - Z2) < tolerance_z:
        # Calculate the length of the beam
        length = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)
        beam_data[frame_ID] = {
            "length": length,
            "start_coords": (X1, Y1, Z1),
            "end_coords": (X2, Y2, Z2)
        }

# Step 3: Iterate through the identified beams, calculate their lengths, and if a beam's length is shorter than 10 feet, change its section property to 'B12x20'.
for frame_ID, data in beam_data.items():
    if data["length"] < 10.0:
        #print(frame_ID)
        # Change the section property to 'B12x20'
        ret = SapModel.FrameObj.SetSection(frame_ID, "B12x20")