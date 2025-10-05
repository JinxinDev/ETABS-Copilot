"""
Generated ETABS Script
Description: A sequential plan to retrieve all beam span lengths in the ETABS model by calculating the distance between their end point coordinates, excluding columns.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 16:59:14
Steps: 4
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

# Step 2: For each retrieved frame object, get the names of its two end point objects. This is a necessary step to access the geometric definition of the frame.
# The necessary API method to retrieve the end point names (Point1, Point2) for an existing frame object (e.g., SapModel.FrameObj.GetPoints) is not present in the provided 'Just-in-Time Knowledge for This Step'. Therefore, this step cannot be fully implemented with the given information.

# Step 3: For each of the two end point objects associated with a frame, retrieve its Cartesian coordinates (X, Y, Z) in the present units.
frame_coordinates = {}
for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Store the retrieved coordinates, associating them with the frame object.
    frame_coordinates[frame_ID] = {
        "Point1": {"X": X1, "Y": Y1, "Z": Z1},
        "Point2": {"X": X2, "Y": Y2, "Z": Z2}
    }

# Step 4: Calculate the Euclidean distance between the two end points for each frame object to determine its length. To filter out columns, check if the absolute difference in the Z-coordinates of the end points is below a small tolerance (indicating a horizontal member, i.e., a beam). If it is a beam, record its calculated span length.
import math

beam_spans = {}
Z_tolerance = 0.01 # feet, to determine if a member is horizontal (a beam)

for frame_ID, coords in frame_coordinates.items():
    X1 = coords["Point1"]["X"]
    Y1 = coords["Point1"]["Y"]
    Z1 = coords["Point1"]["Z"]
    X2 = coords["Point2"]["X"]
    Y2 = coords["Point2"]["Y"]
    Z2 = coords["Point2"]["Z"]

    # Calculate Euclidean distance (length of the frame)
    span_length = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)

    # Check if it's a beam (horizontal member)
    if abs(Z2 - Z1) < Z_tolerance:
        beam_spans[frame_ID] = span_length
print(beam_spans)