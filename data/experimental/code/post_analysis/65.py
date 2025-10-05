"""
Generated ETABS Script
Description: Retrieve all beams on Story2 and identify those where the maximum bending moment exceeds 150 kip-ft.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 17:47:37
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects located on the story named 'Story2'.
story_name = "Story2"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

# Step 2: For each retrieved frame object, get the names of its start and end point objects. Then, for each point object, retrieve its Cartesian coordinates (X, Y, Z) to determine if the frame object is a horizontal beam (i.e., start and end Z-coordinates are approximately equal).
horizontal_beams = []
tolerance = 0.01 # feet, for Z-coordinate comparison

for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Check if the frame object is a horizontal beam (Z-coordinates are approximately equal)
    if abs(Z1 - Z2) < tolerance:
        horizontal_beams.append(frame_ID)

# Step 3: For each identified beam, retrieve the frame forces, specifically the bending moments (M3), for all relevant load cases or combinations. The analysis results should be obtained for the specified line elements (beams).
beam_moments_M3 = {}
ObjectElm = 0 # eItemType::Objects

for beam_ID in horizontal_beams:
    # Retrieve frame force results for the current beam
    (NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret) = SapModel.Results.FrameForce(beam_ID, ObjectElm)
    
    if ret == 0:
        # Store the M3 bending moments for the current beam
        beam_moments_M3[beam_ID] = M3
    else:
        print(f"Error retrieving frame forces for beam: {beam_ID}, Return code: {ret}")

# Step 4: Iterate through the frame force results for each beam. Determine the maximum absolute bending moment (M3) for each beam and compare it against the threshold of 150 kip-ft. Compile a list of beam names that exceed this threshold.
moment_threshold = 150.0 # kip-ft
beams_exceeding_threshold = []

for beam_ID, M3_values in beam_moments_M3.items():
    if M3_values:
        # Find the maximum absolute bending moment (M3) for the current beam
        max_abs_M3 = max(abs(m) for m in M3_values)

        # Check if the maximum absolute M3 exceeds the threshold
        if max_abs_M3 > moment_threshold:
            beams_exceeding_threshold.append(beam_ID)

# Optional: Print the beams that exceed the threshold
# if beams_exceeding_threshold:
#     print(f"Beams exceeding the M3 moment threshold of {moment_threshold} kip-ft: {beams_exceeding_threshold}")
# else:
#     print(f"No beams found exceeding the M3 moment threshold of {moment_threshold} kip-ft.")

# Step 5: Print the names of all beams on 'Story2' where the maximum bending moment exceeds 150 kip-ft.
if beams_exceeding_threshold:
    print(f"Beams on 'Story2' exceeding the M3 moment threshold of {moment_threshold} kip-ft: {beams_exceeding_threshold}")
else:
    print(f"No beams on 'Story2' found exceeding the M3 moment threshold of {moment_threshold} kip-ft.")