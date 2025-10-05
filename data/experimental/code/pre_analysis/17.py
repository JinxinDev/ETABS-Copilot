"""
Generated ETABS Script
Description: Compare the total count of beams on Story 2 versus Story 3 and report which story has more beams.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-13 18:02:16
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names and types of all frame objects located on "Story 2".
# Specify the name of the story to analyze.
story_name = "Story2"

# Use the ETABS API to get the names of all frame objects located on the specified story.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

# Initialize lists to store classified frame objects
beam_names = []
column_names = []

# Iterate through each frame name obtained from the story.
for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Classify the frame object as a column or beam based on its coordinates.
    # If X and Y coordinates are the same for both points, it's a vertical element (column).
    if X1 == X2 and Y1 == Y2:
        column_names.append(frame_ID)
    else:
        beam_names.append(frame_ID)

# At this point, 'beam_names' contains all beam IDs on Story 2,
# and 'column_names' contains all column IDs on Story 2.

# Step 2: Count the number of frame objects identified as "Beam" from the list retrieved for "Story 2".
# Count the number of beam objects.
num_beams = len(beam_names)

# Step 3: Retrieve the names and types of all frame objects located on "Story 3".
# Step 3: Retrieve the names and types of all frame objects located on "Story 3".
# Specify the name of the story to analyze.
story_name_story3 = "Story3"

# Use the ETABS API to get the names of all frame objects located on the specified story.
frame_obj_num_story3, frame_ID_tuple_story3, ret = SapModel.FrameObj.GetNameListOnStory(story_name_story3)

# Step 4: Count the number of frame objects identified as "Beam" from the list retrieved for "Story 3".
# Initialize lists to store classified frame objects for Story 3
beam_names_story3 = []
column_names_story3 = []

# Iterate through each frame name obtained from Story 3.
for frame_ID_story3 in frame_ID_tuple_story3:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1_story3, point_2_story3, ret = SapModel.FrameObj.GetPoints(frame_ID_story3)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1_story3, Y1_story3, Z1_story3, ret = SapModel.PointObj.GetCoordCartesian(point_1_story3)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2_story3, Y2_story3, Z2_story3, ret = SapModel.PointObj.GetCoordCartesian(point_2_story3)

    # Classify the frame object as a column or beam based on its coordinates.
    # If X and Y coordinates are the same for both points, it's a vertical element (column).
    if X1_story3 == X2_story3 and Y1_story3 == Y2_story3:
        column_names_story3.append(frame_ID_story3)
    else:
        beam_names_story3.append(frame_ID_story3)

# Count the number of beam objects for Story 3.
num_beams_story3 = len(beam_names_story3)

# Step 5: Compare the total count of beams on Story 2 with the total count of beams on Story 3 and report which story has more beams, or if they have an equal number.
# Compare the total count of beams on Story 2 with Story 3.
if num_beams > num_beams_story3:
    print(f"Story 2 has more beams ({num_beams}) than Story 3 ({num_beams_story3}).")
elif num_beams_story3 > num_beams:
    print(f"Story 3 has more beams ({num_beams_story3}) than Story 2 ({num_beams}).")
else:
    print(f"Story 2 and Story 3 have an equal number of beams ({num_beams}).")