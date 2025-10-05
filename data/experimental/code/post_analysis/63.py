"""
Generated ETABS Script
Description: Retrieve and list the story drifts for all stories in the X-direction under the 'Dead' load case.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 17:38:09
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the story drifts for all stories in the X-direction (Dir = 1) under the 'Dead' load case.
NumberResults, Story, LoadCase, StepType, StepNum, Direction, Drift, Label, X, Y, Z, ret = SapModel.Results.StoryDrifts()

story_drifts_x_dead = []
if ret == 0:
    for i in range(NumberResults):
        if LoadCase[i] == 'Dead' and Direction[i] == 'X':
            story_drifts_x_dead.append({
                'Story': Story[i],
                'Drift': Drift[i]
            })
else:
    print("Error retrieving story drifts.")