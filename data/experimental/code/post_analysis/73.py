"""
Generated ETABS Script
Description: Retrieve the vertical reactions (FZ) for specified support joints '149' and '154' after running the analysis.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:56:05
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Run the analysis on the current ETABS model to ensure results are available for retrieval.
# The method to run analysis was not found in the provided Just-in-Time Knowledge for this step. Therefore, the analysis cannot be performed.

# Step 2: Retrieve the vertical reactions (FZ) for the support joints '149' and '154'.
joint_names = ['149', '154']
ObjectElm = 0

vertical_reactions = {}
for joint_name in joint_names:
    (
        NumberResults,
        Obj,
        Elm,
        LoadCase,
        StepType,
        StepNum,
        F1,
        F2,
        F3,
        M1,
        M2,
        M3,
        ret
    ) = SapModel.Results.JointReact(joint_name, ObjectElm)

    if ret == 0 and NumberResults > 0:
        # Assuming we are interested in the first result if multiple exist for a joint
        vertical_reactions[joint_name] = F3[0]
    else:
        vertical_reactions[joint_name] = None # Or handle error appropriately

# Print the retrieved vertical reactions
print(f"Vertical reactions (FZ): {vertical_reactions}")