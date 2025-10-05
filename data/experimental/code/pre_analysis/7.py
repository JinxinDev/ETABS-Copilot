"""
Generated ETABS Script
Description: Retrieve the height of each story, which represents the typical column height for that story, and list them.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 19:06:43
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined stories in the model.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each retrieved story name, get its corresponding height.
story_heights = {}
for story_name in story_names:
    height, ret = SapModel.Story.GetHeight(story_name)
    story_heights[story_name] = height