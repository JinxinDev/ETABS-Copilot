"""
Generated ETABS Script
Description: Retrieve and report the total base shear in the X and Y directions for the 'Dead' load case from the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 17:24:18
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the total base reactions for the 'Dead' load case.
(NumberResults, LoadCase, StepType, StepNum, FX, FY, FZ, MX, MY, MZ, GX, GY, GZ, ret) = SapModel.Results.BaseReact()

if ret == 0:
    dead_load_case_index = -1
    for i, case in enumerate(LoadCase):
        if case == 'Dead':
            dead_load_case_index = i
            break

    if dead_load_case_index != -1:
        dead_fx = FX[dead_load_case_index]
        dead_fy = FY[dead_load_case_index]
        dead_fz = FZ[dead_load_case_index]
        dead_mx = MX[dead_load_case_index]
        dead_my = MY[dead_load_case_index]
        dead_mz = MZ[dead_load_case_index]

        print(f"Base Reactions for 'Dead' load case:")
        print(f"  FX: {dead_fx} kips")
        print(f"  FY: {dead_fy} kips")
        print(f"  FZ: {dead_fz} kips")
        print(f"  MX: {dead_mx} kip-ft")
        print(f"  MY: {dead_my} kip-ft")
        print(f"  MZ: {dead_mz} kip-ft")
    else:
        print("Error: 'Dead' load case not found in base reactions.")
else:
    print(f"Error retrieving base reactions: {ret}")