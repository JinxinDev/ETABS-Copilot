"""
Generated ETABS Script
Description: Create a 5-story building with specific story elevations and a Cartesian grid system.
Session Mode: CREATE_NEW
Generated: 2025-09-11 21:00:42
Steps: 2
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

# Step 1: Create a new grid-only model with 5 stories, a typical story height of 15 ft, a Cartesian grid system named 'GS1' with 4 bays at 25 ft spacing in the X-direction (Lines A-E), and 3 bays at 30 ft spacing in the Y-direction (Lines 1-4).
ret = SapModel.File.NewGridOnly(5, 15.0, 15.0, 5, 4, 25.0, 30.0)

# Step 2: Set the story data for the 5-story building. The stories will be named 'Story5', 'Story4', 'Story3', 'Story2', and 'Ground'. Their respective elevations will be 60 ft, 45 ft, 30 ft, 15 ft, and 0 ft. Each story will have a height of 15 ft.
# Define story data from bottom to top
story_names = ['Ground', 'Story2', 'Story3', 'Story4', 'Story5']
story_heights = [15.0, 15.0, 15.0, 15.0, 15.0]

# Default values for other story properties as no specific instructions were given
is_master_story = [False] * 5
similar_to_story = [''] * 5
splice_above = [False] * 5
splice_height = [0.0] * 5
color = [0] * 5 # Default color (e.g., black)

# The base elevation of the lowest story ('Ground')
base_elevation = 0.0
num_stories = 5

# Set the story data for the tower using SetStories_2
# The method returns various story properties, but we only need the return code (ret)
(
    _, # story_names_out
    _, # story_heights_out
    _, # is_master_story_out
    _, # similar_to_story_out
    _, # splice_above_out
    _, # splice_height_out
    _, # color_out
    ret,
) = SapModel.Story.SetStories_2(
    base_elevation,
    num_stories,
    story_names,
    story_heights,
    is_master_story,
    similar_to_story,
    splice_above,
    splice_height,
    color
)