"""
Generated ETABS Script
Description: Identify the beam with the maximum vertical displacement and then determine its maximum bending moment.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:18:01
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all frame objects defined in the ETABS model. This list will be used to identify potential beams.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 2: For each frame object, identify its associated point elements (e.g., start and end points). Then, for each of these points, retrieve its vertical displacement (Uz) from the analysis results. This step implicitly requires a mechanism to map frame objects to their constituent points.
ObjectElm = 0

# Dictionary to store vertical displacements for each point
point_vertical_displacements = {}

# Set to store unique point names associated with frame objects
unique_point_names = set()

# Iterate through each frame object to identify its associated points
for frame_id in frame_ID_tuple:
    # Use FrameJointForce to implicitly get the connected points
    # The PointElm output parameter will contain the names of the joints at the ends of the frame elements
    (
        NumberResults,
        Obj,
        Elm,
        PointElm, # This tuple will contain the names of the points connected to the frame_id
        LoadCase,
        StepType,
        StepNum,
        F1, F2, F3, M1, M2, M3,
        ret
    ) = SapModel.Results.FrameJointForce(frame_id, ObjectElm)

    if ret == 0 and NumberResults > 0:
        for point_name in PointElm:
            unique_point_names.add(point_name)

# Now, for each unique point, retrieve its vertical displacement (Uz)
for point_name in unique_point_names:
    (
        NumberResults,
        Obj,
        Elm,
        LoadCase,
        StepType,
        StepNum,
        U1, U2, U3, R1, R2, R3, # U3 is the vertical displacement
        ret
    ) = SapModel.Results.JointDispl(point_name, ObjectElm)

    if ret == 0 and NumberResults > 0:
        # Store all Uz results for the current point, including load case details
        displacements_for_point = []
        for i in range(NumberResults):
            displacements_for_point.append({
                "LoadCase": LoadCase[i],
                "StepType": StepType[i],
                "StepNum": StepNum[i],
                "Uz": U3[i] # Vertical displacement
            })
        point_vertical_displacements[point_name] = displacements_for_point

# The 'point_vertical_displacements' dictionary now holds the Uz for each unique point.

# Step 3: Compare the absolute vertical displacements of all points associated with all frame objects to find the maximum value. Identify the specific frame object (beam) to which this point belongs, as this is the beam with the maximum vertical displacement.
# Initialize variables to track the maximum displacement
max_displacement_value = 0.0
max_displacement_point_id = None
max_displacement_loadcase_id = None

# Iterate through all collected point displacements to find the maximum absolute vertical displacement
for point_name, displacements_for_point in point_vertical_displacements.items():
    for disp_info in displacements_for_point:
        current_uz = disp_info["Uz"]
        current_abs_uz = abs(current_uz)

        if current_abs_uz > max_displacement_value:
            max_displacement_value = current_abs_uz
            max_displacement_point_id = point_name
            max_displacement_loadcase_id = disp_info["LoadCase"]

# Now, find the frame object (beam) associated with the point that has the maximum displacement
max_displacement_beam_id = None

if max_displacement_point_id:
    for frame_id in frame_ID_tuple:
        # Use FrameJointForce to get the points connected to this frame_id
        # ObjectElm is already defined as 0 (eItemType::Objects)
        (
            NumberResults,
            Obj,
            Elm,
            PointElm, # This tuple will contain the names of the points connected to the frame_id
            LoadCase,
            StepType,
            StepNum,
            F1, F2, F3, M1, M2, M3,
            ret
        ) = SapModel.Results.FrameJointForce(frame_id, ObjectElm)

        if ret == 0 and NumberResults > 0:
            # Check if the point with max displacement is one of the points connected to this frame
            if max_displacement_point_id in PointElm:
                max_displacement_beam_id = frame_id
                break # Found the beam, no need to check other frames

# The variables max_displacement_beam_id, max_displacement_point_id,
# max_displacement_value, and max_displacement_loadcase_id now hold the required information.

# Step 4: For the beam identified as having the maximum vertical displacement, retrieve its detailed frame forces, including bending moments, from the analysis results.
# Retrieve detailed frame forces for the identified beam
# ObjectElm is already defined as 0 (eItemType::Objects)
(NumberResults_beam_forces,
 Obj_beam_forces,
 ObjSta_beam_forces,
 Elm_beam_forces,
 ElmSta_beam_forces,
 LoadCase_beam_forces,
 StepType_beam_forces,
 StepNum_beam_forces,
 P_beam_forces,
 V2_beam_forces,
 V3_beam_forces,
 T_beam_forces,
 M2_beam_forces,
 M3_beam_forces,
 ret_beam_forces) = SapModel.Results.FrameForce(max_displacement_beam_id, ObjectElm)

# Store the detailed frame forces for the beam
beam_forces_results = []
if ret_beam_forces == 0 and NumberResults_beam_forces > 0:
    for i in range(NumberResults_beam_forces):
        beam_forces_results.append({
            "Object": Obj_beam_forces[i],
            "ObjectStation": ObjSta_beam_forces[i],
            "Element": Elm_beam_forces[i],
            "ElementStation": ElmSta_beam_forces[i],
            "LoadCase": LoadCase_beam_forces[i],
            "StepType": StepType_beam_forces[i],
            "StepNum": StepNum_beam_forces[i],
            "AxialForce_P": P_beam_forces[i],
            "ShearForce_V2": V2_beam_forces[i],
            "ShearForce_V3": V3_beam_forces[i],
            "Torsion_T": T_beam_forces[i],
            "Moment_M2": M2_beam_forces[i],
            "Moment_M3": M3_beam_forces[i]
        })

# The 'beam_forces_results' list now contains the detailed frame forces for the beam with maximum displacement.

# Step 5: From the retrieved frame forces for the beam with the maximum vertical displacement, extract the maximum bending moment (M2 or M3) along its length.
# Initialize variables to track the maximum bending moment
max_bending_moment_value = 0.0
max_bending_moment_loadcase = None
max_bending_moment_station = None
max_bending_moment_type = None # To indicate if it was M2 or M3

# Iterate through the detailed frame forces for the beam
for force_info in beam_forces_results:
    current_m2 = force_info["Moment_M2"]
    current_m3 = force_info["Moment_M3"]
    current_obj_station = force_info["ObjectStation"]
    current_loadcase = force_info["LoadCase"]

    # Check M2
    if abs(current_m2) > max_bending_moment_value:
        max_bending_moment_value = abs(current_m2)
        max_bending_moment_loadcase = current_loadcase
        max_bending_moment_station = current_obj_station
        max_bending_moment_type = "M2"

    # Check M3
    if abs(current_m3) > max_bending_moment_value:
        max_bending_moment_value = abs(current_m3)
        max_bending_moment_loadcase = current_loadcase
        max_bending_moment_station = current_obj_station
        max_bending_moment_type = "M3"

# The variables max_bending_moment_value, max_bending_moment_loadcase,
# max_bending_moment_station, and max_bending_moment_type now hold the
# maximum bending moment and its associated details for the identified beam.