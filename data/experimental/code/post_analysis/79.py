"""
Generated ETABS Script
Description: Retrieve all frame objects, identify which ones are beams connected to joint '149', and then report the maximum shear forces for each of those beams.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 00:18:50
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

# Step 2: Iterate through each retrieved frame object. For each frame object, determine its connected point objects using 'FrameJointForce'. Then, retrieve the Cartesian coordinates of these connected point objects using 'GetCoordCartesian'. Based on the Z-coordinates of the connected points, identify if the frame object is a horizontal beam. If it is a beam and one of its connected points is '149', add its name to a list of relevant beams.
relevant_beams = []
z_tolerance = 0.01

for frame_ID in frame_ID_tuple:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    is_horizontal_beam = abs(Z1 - Z2) < z_tolerance

    is_connected_to_149 = (point_1 == '149' or point_2 == '149')

    if is_horizontal_beam and is_connected_to_149:
        relevant_beams.append(frame_ID)

# Step 3: For each beam identified in the previous step as being connected to joint '149', retrieve its frame forces using 'FrameForce'.
beam_forces = {}
ObjectElm = 0

for beam_ID in relevant_beams:
    (NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret) = SapModel.Results.FrameForce(beam_ID, ObjectElm)
    beam_forces[beam_ID] = {
        "NumberResults": NumberResults,
        "Obj": Obj,
        "ObjSta": ObjSta,
        "Elm": Elm,
        "ElmSta": ElmSta,
        "LoadCase": LoadCase,
        "StepType": StepType,
        "StepNum": StepNum,
        "P": P,
        "V2": V2,
        "V3": V3,
        "T": T,
        "M2": M2,
        "M3": M3
    }

# Step 4: For each beam, analyze the retrieved frame forces to find the maximum absolute shear force (V2 or V3) along its length and report this value.
max_shear_forces = {}

for beam_ID, forces_data in beam_forces.items():
    v2_values = forces_data["V2"]
    v3_values = forces_data["V3"]

    all_shear_values = [abs(v) for v in v2_values] + [abs(v) for v in v3_values]

    if all_shear_values:
        max_shear_forces[beam_ID] = max(all_shear_values)
    else:
        max_shear_forces[beam_ID] = 0.0
print(max_shear_forces)
