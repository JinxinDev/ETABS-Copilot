"""
Generated ETABS Script
Description: Retrieve the frame joint forces at both ends of the specified beam element.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:50:34
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Get the frame joint forces at both ends of the beam named '506'.
ObjectElm = 0
(NumberResults, Obj, Elm, PointElm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3, ret) = SapModel.Results.FrameJointForce('506', ObjectElm)