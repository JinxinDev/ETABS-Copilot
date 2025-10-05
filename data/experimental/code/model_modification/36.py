"""
Generated ETABS Script
Description: Create 5 stories with specified names, elevations, and heights in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 17:43:16
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
SapModel.File.NewBlank()
# Step 1: Set the story data for 5 stories: 'BASE' at elevation 0 ft, 'LEVEL1' at 15 ft (15 ft height), 'LEVEL2' at 30 ft (15 ft height), 'LEVEL3' at 45 ft (15 ft height), and 'PENTHOUSE' at 65 ft (20 ft height). The 'BASE' story will be set as a master story, and 'LEVEL1', 'LEVEL2', 'LEVEL3', and 'PENTHOUSE' will be set as similar to 'BASE'.
# Define story data
base_elevation = 0.0
num_stories = 5

in_story_names = ["BASE", "LEVEL1", "LEVEL2", "LEVEL3", "PENTHOUSE"]
in_story_heights = [0.0, 15.0, 15.0, 15.0, 20.0] # Heights of each story
in_is_master_story = [True, False, False, False, False]
in_similar_to_story = ["None", "BASE", "BASE", "BASE", "BASE"] # 'None' for master story

# Default values for splice and color as not specified
in_splice_above = [False, False, False, False, False]
in_splice_height = [0.0, 0.0, 0.0, 0.0, 0.0]
in_color = [0, 0, 0, 0, 0] # Default color (black)

# Set the story data using SetStories_2
(
    story_names_out,
    story_heights_out,
    is_master_story_out,
    similar_to_story_out,
    splice_above_out,
    splice_height_out,
    color_out,
    ret
) = SapModel.Story.SetStories_2(
    base_elevation,
    num_stories,
    in_story_names,
    in_story_heights,
    in_is_master_story,
    in_similar_to_story,
    in_splice_above,
    in_splice_height,
    in_color
)