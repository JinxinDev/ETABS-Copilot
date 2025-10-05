"""
Generated ETABS Script
Description: Standardize the naming convention for all concrete beam section properties in the ETABS model to follow the format 'CB_DepthxWidth', where Depth and Width are extracted from the existing section names.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 15:37:27
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all defined frame section property names in the model.
num_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 2: Iterate through the retrieved frame section names. For each name that matches the pattern of an existing concrete section (e.g., 'B14x28'), parse the depth and width values. Construct a new name following the format 'CB_WidthxDepth' (e.g., 'B14x28' becomes 'CB_28x14'). Then, change the name of the frame section property to the newly formatted name.
import re

for name in frame_section_names:
    match = re.match(r'B(\d+)x(\d+)', name)
    if match:
        depth = int(match.group(1))
        width = int(match.group(2))
        new_name = f'CB_{width}x{depth}'
        ret = SapModel.PropFrame.ChangeName(name, new_name)
        print(ret)