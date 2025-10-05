"""
Generated ETABS Script
Description: Retrieve the torsion force in beam '496' for the 'Dead' load case from the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:38:35
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the frame forces, including torsion, for the beam object named '496' under the 'Dead' load case.
ObjectElm = 0
frame_name = '496'

# Retrieve frame forces for the specified beam object
(NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret) = SapModel.Results.FrameForce(frame_name, ObjectElm)

# Filter results for the 'Dead' load case
dead_load_forces = []
if ret == 0:
    for i in range(NumberResults):
        if LoadCase[i] == 'Dead':
            dead_load_forces.append({
                'Object': Obj[i],
                'ObjectStation': ObjSta[i],
                'Element': Elm[i],
                'ElementStation': ElmSta[i],
                'LoadCase': LoadCase[i],
                'StepType': StepType[i],
                'StepNum': StepNum[i],
                'AxialForce_P': P[i],
                'ShearForce_V2': V2[i],
                'ShearForce_V3': V3[i],
                'Torsion_T': T[i],
                'Moment_M2': M2[i],
                'Moment_M3': M3[i]
            })

# You can now process 'dead_load_forces' which contains the filtered results