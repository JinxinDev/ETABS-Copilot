"""
Generated ETABS Script
Description: Report the displacement of a specified joint and the axial force in all frame members connected to it.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 17:01:17
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the displacement results (U1, U2, U3, R1, R2, R3) for the joint named '154' for all available load cases or combinations.
ObjectElm = 0
(NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret) = SapModel.Results.JointDispl('154', ObjectElm)

# Step 2: Identify all frame objects connected to joint '154' and then retrieve the axial force for each of these connected frame objects for all available load cases or combinations.
# Identify all frame objects connected to joint '154'
(
    NumberItems_FJ,
    ObjNames_FJ, 
    ElmNames_FJ, 
    PointElm_FJ,
    LoadCase_FJ,
    StepType_FJ,
    StepNum_FJ,
    F1_FJ, F2_FJ, F3_FJ, M1_FJ, M2_FJ, M3_FJ,
    ret_FJ
) = SapModel.Results.FrameJointForce('154', ObjectElm)

# Get unique frame object names from the connected objects
unique_connected_frame_objects = list(set(ObjNames_FJ))

# Retrieve the axial force for each of these connected frame objects for all available load cases or combinations
all_frame_axial_forces_results = {}
for frame_obj_name in unique_connected_frame_objects:
    (
        NumberItems_FF,
        ObjNames_FF,
        ObjSta_FF,
        ElmNames_FF,
        ElmSta_FF,
        LoadCase_FF,
        StepType_FF,
        StepNum_FF,
        P_FF, 
        V2_FF, V3_FF, T_FF, M2_FF, M3_FF,
        ret_FF
    ) = SapModel.Results.FrameForce(frame_obj_name, ObjectElm)

    # Store the axial forces for this frame object
    frame_axial_forces_data = []
    for i in range(NumberItems_FF):
        frame_axial_forces_data.append({
            'LoadCase': LoadCase_FF[i],
            'StepType': StepType_FF[i],
            'StepNum': StepNum_FF[i],
            'ObjectStation': ObjSta_FF[i],
            'ElementStation': ElmSta_FF[i],
            'AxialForce_P': P_FF[i]
        })
    all_frame_axial_forces_results[frame_obj_name] = frame_axial_forces_data

# The 'all_frame_axial_forces_results' dictionary now contains the axial forces
# for each frame object connected to joint '154', organized by frame object name.