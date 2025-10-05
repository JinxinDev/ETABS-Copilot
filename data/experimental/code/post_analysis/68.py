"""
Generated ETABS Script
Description: Retrieve the total vertical base reaction for the 'Dead' load case from the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:32:19
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Run the analysis to ensure that results are available for querying.
ret = SapModel.Analyze.RunAnalysis()

# Step 2: Retrieve the total base reactions for the 'Dead' load case.
(NumberResults, LoadCase, StepType, StepNum, FX, FY, FZ, MX, MY, MZ, GX, GY, GZ, ret) = SapModel.Results.BaseReact()

dead_case_index = -1
for i, case in enumerate(LoadCase):
    if case == 'Dead':
        dead_case_index = i
        break

if dead_case_index != -1:
    dead_FX = FX[dead_case_index]
    dead_FY = FY[dead_case_index]
    dead_FZ = FZ[dead_case_index]
    dead_MX = MX[dead_case_index]
    dead_MY = MY[dead_case_index]
    dead_MZ = MZ[dead_case_index]
else:
    print("Error: 'Dead' load case not found in base reactions.")