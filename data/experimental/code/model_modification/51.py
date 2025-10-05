"""
Generated ETABS Script
Description: Create a new strength design load combination named '1.2D+1.0L+0.5W' that includes Dead, Live, and Wind-X loads with their respective factors.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 09:38:05
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new load combination named '1.2D+1.0L+0.5W' of type 'Linear Add', incorporating the 'Dead' load pattern with a scale factor of 1.2, the 'Live' load pattern with a scale factor of 1.0, and the 'Wind-X' load pattern with a scale factor of 0.5.
combo_name = "1.2D+1.0L+0.5W"
SapModel.RespCombo.Add(combo_name, 0)
SapModel.RespCombo.SetCaseList_1(combo_name, 0, "Dead", 0, 1.2)
SapModel.RespCombo.SetCaseList_1(combo_name, 0, "Live", 0, 1.0)
SapModel.RespCombo.SetCaseList_1(combo_name, 0, "Wind-X", 0, 0.5)