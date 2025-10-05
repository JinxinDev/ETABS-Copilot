"""
Generated ETABS Script
Description: Retrieve and list the total number of load patterns defined in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 16:26:36
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the total number of defined load patterns in the model.
num_of_load_patterns = SapModel.LoadPatterns.Count()