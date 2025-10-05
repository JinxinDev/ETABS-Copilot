"""
Generated ETABS Script
Description: Create a rigid diaphragm for each story in the ETABS model and assign it to all area objects on that respective story.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 20:08:06
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined stories in the ETABS model.
number_of_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each retrieved story name, define a new rigid diaphragm. The diaphragm name will be derived from the story name (e.g., 'D_Story1' for 'Story1').
for story_name in story_names:
    diaphragm_name = "D_" + story_name
    # SetDiaphragm(Name, SemiRigid)
    # For a rigid diaphragm, SemiRigid should be False.
    ret = SapModel.Diaphragm.SetDiaphragm(diaphragm_name, True)

# Step 3: For each story, retrieve the names of all area objects defined on that specific story.
story_area_objects = {}
for story_name in story_names:
    # GetNameListOnStory(StoryName)
    # Returns: NumberNames, MyName, ret
    number_of_area_objects, area_object_names, ret = SapModel.AreaObj.GetNameListOnStory(story_name)
    story_area_objects[story_name] = area_object_names

# Step 4: For each story, assign the diaphragm created for that story to all area objects found on that story.
for story_name in story_names:
    diaphragm_name = "D_" + story_name
    area_object_names = story_area_objects[story_name]
    for area_object_name in area_object_names:
        # SetDiaphragm(Name, DiaphragmName)
        ret = SapModel.AreaObj.SetDiaphragm(area_object_name, diaphragm_name)