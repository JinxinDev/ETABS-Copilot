"""
Generated ETABS Script
Description: Increase the height of Story2, Story4, and Story5 by 1.5 feet each.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 16:23:35
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the current height of 'Story2'.
story_name_to_retrieve = 'Story2'
height, ret = SapModel.Story.GetHeight(story_name_to_retrieve)

# Step 2: Set the new height for 'Story2' by adding 1.5 feet to its current height.
new_height = height + 1.5
ret = SapModel.Story.SetHeight(story_name_to_retrieve, new_height)

# Step 3: Retrieve the current height of 'Story4'.
story_name_to_retrieve_story4 = 'Story4'
height_story4, ret = SapModel.Story.GetHeight(story_name_to_retrieve_story4)

# Step 4: Set the new height for 'Story4' by adding 1.5 feet to its current height.
new_height_story4 = height_story4 + 1.5
ret = SapModel.Story.SetHeight(story_name_to_retrieve_story4, new_height_story4)

# Step 5: Retrieve the current height of 'Story5'.
story_name_to_retrieve_story5 = 'Story5'
height_story5, ret = SapModel.Story.GetHeight(story_name_to_retrieve_story5)

# Step 6: Set the new height for 'Story5' by adding 1.5 feet to its current height.
new_height_story5 = height_story5 + 1.5
ret = SapModel.Story.SetHeight(story_name_to_retrieve_story5, new_height_story5)