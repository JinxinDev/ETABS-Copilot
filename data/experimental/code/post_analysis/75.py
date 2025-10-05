"""
Generated ETABS Script
Description: Identify beams on Story3 where the major moment (M3) exceeds 200 kip-ft and the maximum vertical displacement at any of its joints is greater than 1 inch.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 22:25:04
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects located on 'Story3'.
story_name = "Story3"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

# Step 2: For each frame object identified on 'Story3', determine if it is a beam (horizontal element) and retrieve its end joint names. This step assumes the code can differentiate beams from columns and link frame objects to their end joints.
beam_data = []
for frame_ID in frame_ID_tuple:
    NumberResults, Obj, Elm, PointElm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3, ret = SapModel.Results.FrameJointForce(frame_ID, 0)

    if ret == 0 and NumberResults == 2:
        joint1_name = PointElm[0]
        joint2_name = PointElm[1]
        
        # NOTE: The provided Just-in-Time Knowledge does not include methods to
        # geometrically differentiate between beams (horizontal) and columns (vertical).
        # Therefore, this code retrieves end joint names for all frame objects on 'Story3'
        # without applying the beam/column differentiation.
        
        beam_data.append({
            "frame_ID": frame_ID,
            "end_joints": (joint1_name, joint2_name)
        })
    elif ret != 0:
        # In a full script, robust error handling would be implemented here.
        pass

# Step 3: For each identified beam, retrieve the frame forces, specifically the major moment (M3), for a relevant load case or combination. The threshold for M3 is 200 kip-ft.
m3_threshold = 200.0
load_case_to_check = "DEAD" # Example: Check for 'DEAD' load case. This could be a combo too.

beams_exceeding_m3 = []

for beam_info in beam_data:
    frame_ID = beam_info["frame_ID"]

    # Retrieve frame force results for the current beam
    # ItemType = 0 (Objects)
    NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret = SapModel.Results.FrameForce(frame_ID, 0)

    if ret == 0 and NumberResults > 0:
        for i in range(NumberResults):
            if LoadCase[i] == load_case_to_check:
                current_m3 = M3[i]
                if abs(current_m3) > m3_threshold:
                    beams_exceeding_m3.append({
                        "frame_ID": frame_ID,
                        "load_case": LoadCase[i],
                        "station": ObjSta[i],
                        "M3_value": current_m3
                    })
    # In a full script, robust error handling would be implemented here for ret != 0

# Step 4: For each end joint associated with the beams, retrieve the vertical displacement (Uz) for a relevant load case or combination. The threshold for vertical displacement is 1 inch.
uz_threshold_inches = 1.0
uz_threshold_feet = uz_threshold_inches / 12.0 # Convert 1 inch to feet

joints_exceeding_uz = []
unique_joint_names = set()

# Collect all unique end joint names from the identified beams
for beam_info in beam_data:
    unique_joint_names.add(beam_info["end_joints"][0])
    unique_joint_names.add(beam_info["end_joints"][1])

# Retrieve vertical displacement for each unique joint
for joint_name in unique_joint_names:
    # ItemType = 0 (Objects)
    NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret = SapModel.Results.JointDispl(joint_name, 0)

    if ret == 0 and NumberResults > 0:
        for i in range(NumberResults):
            if LoadCase[i] == load_case_to_check:
                current_uz = U3[i]
                if abs(current_uz) > uz_threshold_feet:
                    joints_exceeding_uz.append({
                        "joint_name": joint_name,
                        "load_case": LoadCase[i],
                        "Uz_value": current_uz # Value is in feet
                    })
    # In a full script, robust error handling would be implemented here for ret != 0

# Step 5: Filter the beams to identify those that satisfy both conditions: the major moment (M3) exceeds 200 kip-ft AND the maximum vertical displacement at any of its joints is greater than 1 inch.
# Create a lookup for beam_data by frame_ID to get end joints
beam_data_lookup = {item["frame_ID"]: item["end_joints"] for item in beam_data}

# Create a set of joint names that exceeded the Uz threshold for efficient lookup
exceeding_uz_joint_names_set = {item["joint_name"] for item in joints_exceeding_uz}

# Use a set to store unique frame_IDs that satisfy both conditions
final_filtered_beams_set = set()

# Iterate through beams that had M3 exceeding the threshold
for beam_m3_info in beams_exceeding_m3:
    frame_ID = beam_m3_info["frame_ID"]
    
    # Get the end joints for this frame_ID
    end_joints = beam_data_lookup.get(frame_ID)

    if end_joints: # Ensure end_joints were found for this frame_ID
        joint1_name, joint2_name = end_joints
        
        # Check if either end joint exceeded the Uz threshold
        if joint1_name in exceeding_uz_joint_names_set or joint2_name in exceeding_uz_joint_names_set:
            # This beam (frame_ID) satisfies both conditions
            final_filtered_beams_set.add(frame_ID)

# Convert the set to a list for the final output
final_filtered_beams = list(final_filtered_beams_set)
print(final_filtered_beams)