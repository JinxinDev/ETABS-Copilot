"""
Generated ETABS Script
Description: Define three new stories, 'Lobby', 'Office1', and 'Office2', each with a height of 14 feet, and set their properties in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 20:07:01
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Set the story data for the current tower to include 'Lobby' (height 14 feet, elevation 0 feet), 'Office1' (height 14 feet, elevation 14 feet), and 'Office2' (height 14 feet, elevation 28 feet). All stories will be designated as master stories and not similar to any other story. The story heights will be retained, and elevations will be calculated accordingly.
base_elevation = 0.0
story_names = ['Lobby', 'Office1', 'Office2']
story_heights = [14.0, 14.0, 14.0]
is_master_story = [True, True, True]
similar_to_story = ['None', 'None', 'None']
splice_above = [False, False, False]
splice_height = [0.0, 0.0, 0.0]
color = [0, 0, 0] # Default color
num_stories = len(story_names)

(ret_story_names, ret_story_heights, ret_is_master_story, ret_similar_to_story, ret_splice_above, ret_splice_height, ret_color, ret) = SapModel.Story.SetStories_2(base_elevation, num_stories, story_names, story_heights, is_master_story, similar_to_story, splice_above, splice_height, color)