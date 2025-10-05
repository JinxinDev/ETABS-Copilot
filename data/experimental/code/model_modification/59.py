"""
Generated ETABS Script
Description: Change the section property of every slab in the model to 'S10'.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 16:19:50
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined area objects in the model, which include slabs.
area_obj_count, area_obj_names, ret = SapModel.AreaObj.GetNameList()

# Step 2: Iterate through each retrieved area object (slab) and assign the section property 'S10' to it.
for area_obj_name in area_obj_names:
    ret = SapModel.AreaObj.SetProperty(area_obj_name, "S10")
    print(ret)