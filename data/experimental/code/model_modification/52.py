"""
Generated ETABS Script
Description: The script will identify all stories above 'Story1', then iterate through these stories to find all column objects and change their assigned frame section property to 'W18x130'.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 09:51:10
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
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: Iterate through the retrieved story names to identify all stories that are above 'Story1'.
base_elevation, num_stories_full, all_story_names, story_elevations, story_heights, is_master_story, similar_to_story, splice_above, splice_height, story_colors, ret = SapModel.Story.GetStories_2()

story1_elevation = 0.0
for i in range(num_stories_full):
    if all_story_names[i] == "Story1":
        story1_elevation = story_elevations[i]
        break

stories_above_story1 = []
for i in range(num_stories_full):
    if story_elevations[i] > story1_elevation:
        stories_above_story1.append(all_story_names[i])

# Step 3: For each story identified as being above 'Story1', retrieve the names of all frame objects (columns and beams) located on that specific story.
story_frame_objects = {}
for story_name in stories_above_story1:
    frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    story_frame_objects[story_name] = list(frame_ID_tuple)

# Step 4: From the list of frame objects on each relevant story, filter to identify only the column objects. Then, assign the frame section property 'W18x130' to each of these identified column objects.
story_column_objects = {}
for story_name, frame_ID_list in story_frame_objects.items():
    column_list = []
    for frame_ID in frame_ID_list:
        point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
        X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
        X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

        if X1 - X2 == 0 and Y1 - Y2 == 0:
            column_list.append(frame_ID)
            
            ret = SapModel.FrameObj.SetSection(frame_ID, "W18x130")
    story_column_objects[story_name] = column_list
#print(story_column_objects)