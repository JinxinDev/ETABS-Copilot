"""
Generated ETABS Script
Description: Retrieve the full displacement values, including all three translations and rotations, for a specified joint under a specific load case.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:54:24
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Get the full displacement values (translations and rotations) for joint '149' under the 'Dead' load case.
ObjectElm = 0
(NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret) = SapModel.Results.JointDispl('149', ObjectElm)