"""
Generated ETABS Script
Description: Retrieve the maximum story drift value for the top story of the model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 18:35:54
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined stories in the model to identify the top story.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: Retrieve the story drift results for all stories and load cases. This will provide the necessary data to find the maximum drift for the top story.
num_results, story_names_drift, load_cases, step_types, step_nums, directions, drifts, labels, x_coords, y_coords, z_coords, ret = SapModel.Results.StoryDrifts()

# Step 3: Process the retrieved story drift results to identify the top story (assuming it's the last story in the list obtained from GetNameList) and then find the maximum drift value among all load cases for that specific top story.
top_story_name = story_names[-1]
max_drift_top_story = 0.0

for i in range(num_results):
    if story_names_drift[i] == top_story_name:
        current_drift = drifts[i]
        if current_drift > max_drift_top_story:
            max_drift_top_story = current_drift