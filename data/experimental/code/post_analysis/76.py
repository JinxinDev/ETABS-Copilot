"""
Generated ETABS Script
Description: Retrieve inter-story drift results for all stories, calculate the allowable drift based on story height, and list stories where the X-direction inter-story drift exceeds this limit.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 22:52:16
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all story names defined in the model.
number_of_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each story, retrieve its height. This will be used to calculate the allowable inter-story drift.
story_heights = {}
for story_name in story_names:
    story_height, ret = SapModel.Story.GetHeight(story_name)
    story_heights[story_name] = story_height

# Step 3: Retrieve the inter-story drift results for all stories and all load cases/combinations. We are specifically interested in the drift in the X-direction.
number_results, story_names_drift, load_cases_drift, step_types, step_nums, directions, drifts, labels, x_coords, y_coords, z_coords, ret = SapModel.Results.StoryDrifts()

x_direction_drifts = []
for i in range(number_results):
    if directions[i] == "X":
        x_direction_drifts.append({
            "Story": story_names_drift[i],
            "LoadCase": load_cases_drift[i],
            "Drift": drifts[i]
        })

# Step 4: Iterate through each story, calculate the allowable inter-story drift (0.002 times the story height), and compare it with the actual inter-story drift in the X-direction. List the names of all stories where the actual X-direction drift is greater than the calculated limit.
stories_exceeding_drift_limit = []
for story_name in story_names:
    allowable_drift = 0.002 * story_heights[story_name]
    
    max_actual_x_drift_for_story = 0.0
    for drift_data in x_direction_drifts:
        if drift_data["Story"] == story_name:
            if abs(drift_data["Drift"]) > max_actual_x_drift_for_story:
                max_actual_x_drift_for_story = abs(drift_data["Drift"])
    
    if max_actual_x_drift_for_story > allowable_drift:
        stories_exceeding_drift_limit.append(story_name)