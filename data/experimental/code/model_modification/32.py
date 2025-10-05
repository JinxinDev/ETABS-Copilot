"""
Generated ETABS Script
Description: Create a new ETABS model with a specified grid system and story data.
Session Mode: CREATE_NEW
Generated: 2025-09-11 16:57:32
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
SapModel = EtabsObject.SapModel
ret = EtabsObject.ApplicationStart()
ret = SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)  # Set units to kip_ft_F
print("ETABS connection established")

# Step 1: Create a new grid-only model with 5 bays in the X-direction and 4 bays in the Y-direction, both with 25-foot spacing. The model should also include 6 stories, each 12 feet high, starting from an elevation of 0 feet.
ret = SapModel.File.NewGridOnly(6, 12.0, 12.0, 6, 5, 25.0, 25.0)