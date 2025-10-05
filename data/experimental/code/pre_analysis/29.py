"""
Generated ETABS Script
Description: This script will identify the story in the ETABS model that contains the highest number of column elements. It will iterate through all stories, retrieve frame objects on each story, determine which of these are columns, count them, and then report the story with the maximum column count.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 18:35:42
Steps: 7
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

# Step 2: Initialize a data structure (e.g., a dictionary or hash map) to store the count of column elements for each story.
column_counts_by_story = {story: 0 for story in story_names}

# Step 3: Iterate through each story name obtained in the first step. For each story, retrieve the names of all frame objects located on that specific story.
frame_objects_by_story = {}
for story in story_names:
    num_frames, frame_names, ret = SapModel.FrameObj.GetNameListOnStory(story)
    frame_objects_by_story[story] = frame_names

# Step 4: For each frame object retrieved on the current story, get the name of the frame section property assigned to it.
frame_sections_by_story = {}
for story, frame_names in frame_objects_by_story.items():
    story_frame_sections = {}
    for frame_name in frame_names:
        section_property, _, ret = SapModel.FrameObj.GetSection(frame_name)
        story_frame_sections[frame_name] = section_property
    frame_sections_by_story[story] = story_frame_sections

# Step 5: For each frame section property name, attempt to retrieve its column rebar data. If column rebar data can be successfully retrieved, consider the associated frame object as a column and increment the column count for the current story.
for story, frame_sections in frame_sections_by_story.items():
    for frame_name, section_property in frame_sections.items():
        # Attempt to retrieve column rebar data for the section property
        MatPropLong, MatPropConfine, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned, ret = SapModel.PropFrame.GetRebarColumn(section_property)
        
        # If column rebar data is successfully retrieved (ret == 0), it's a column
        if ret == 0:
            column_counts_by_story[story] += 1

# Step 6: After processing all frame objects on all stories, identify the story that has the highest recorded column count.
max_columns = -1
story_with_most_columns = None

for story, count in column_counts_by_story.items():
    if count > max_columns:
        max_columns = count
        story_with_most_columns = story

# Step 7: Report the name of the story with the highest number of column elements and its corresponding column count.
print(f"The story with the most column elements is '{story_with_most_columns}' with {max_columns} columns.")