"""
Generated ETABS Script
Description: Verify that every story level in the ETABS model is either defined as a 'Master Story' or is 'Similar To' another story, and report any stories that do not meet these conditions.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 17:43:27
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
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each retrieved story, check if it is defined as a 'Master Story'.
for story_name in story_names:
    is_master_story, ret = SapModel.Story.GetMasterStory(story_name)
    print(f"Story: {story_name}, Is Master Story: {is_master_story}")

# Step 3: For any story that is not a 'Master Story', check if it is 'Similar To' another story.
    if not is_master_story:
        _, similar_to_story, ret = SapModel.Story.GetSimilarTo(story_name)
        print(f"    Story: {story_name} is similar to: {similar_to_story}")

# Step 4: Identify and report the names of any stories that are neither a 'Master Story' nor 'Similar To' another story.
        if not similar_to_story:
            print(f"    Story: {story_name} is neither a Master Story nor similar to any other story.")