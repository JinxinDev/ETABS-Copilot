"""
Generated ETABS Script
Description: The plan outlines the steps to identify and remove all beams oriented in the Y-direction on the 3rd floor of the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 16:16:33
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects (which include both beams and columns) located specifically on the 'Story3' of the model.
story_name = "Story3"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

# Step 2: Iterate through each retrieved frame object. For each object, determine its start and end point coordinates. Based on these coordinates, identify if the frame object is a beam (meaning its Z-coordinates are approximately equal, indicating a horizontal element) and if its primary orientation is along the Y-axis (meaning a significant difference in Y-coordinates between its ends, with minimal differences in X and Z coordinates). Collect the names of all frame objects that meet these criteria as Y-oriented beams on the 3rd floor.
y_oriented_beams_on_story3 = []
coord_tolerance = 0.01 # feet, for comparing coordinates

for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Check if it's a beam (Z-coordinates are approximately equal)
    is_beam = abs(Z1 - Z2) < coord_tolerance

    # Check if its primary orientation is along the Y-axis
    delta_x = abs(X1 - X2)
    delta_y = abs(Y1 - Y2)
    delta_z = abs(Z1 - Z2)

    # A significant difference in Y, with minimal differences in X and Z
    is_y_oriented = (delta_y > coord_tolerance) and (delta_x < coord_tolerance) and (delta_z < coord_tolerance)

    if is_beam and is_y_oriented:
        y_oriented_beams_on_story3.append(frame_ID)

# Step 3: Delete all frame objects that were identified in the previous step as beams oriented in the Y-direction on the 'Story3'.
for beam_ID in y_oriented_beams_on_story3:
    ret = SapModel.FrameObj.Delete(beam_ID)