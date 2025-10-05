"""
Generated ETABS Script
Description: Identify stories with a height greater than 15 feet, then find all column elements on those stories and replace their assigned section property with 'C24x24'.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 15:45:07
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all story names defined in the ETABS model.
number_of_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each retrieved story name, get its height. Identify and store the names of all stories where the height is greater than 15 feet.
tall_stories = []
for story_name in story_names:
    height, ret = SapModel.Story.GetHeight(story_name)
    if height > 15:
        tall_stories.append(story_name)

# Step 3: For each story identified in the previous step (stories with height greater than 15 feet), retrieve the names of all frame objects present on that specific story.
tall_story_frame_objects = {}
for story_name in tall_stories:
    frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    tall_story_frame_objects[story_name] = list(frame_ID_tuple)

# Step 4: Iterate through the frame objects obtained from the qualifying stories. For each frame object, determine if it is a column (a vertical frame element). If it is identified as a column, assign the section property 'C24x24' to it.
for story_name, frame_ids in tall_story_frame_objects.items():
    for frame_ID in frame_ids:
        point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
        X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
        X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

        if X1 - X2 == 0 and Y1 - Y2 == 0:
            print(SapModel.FrameObj.SetSection(frame_ID, "C24x24"))