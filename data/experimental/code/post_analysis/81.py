"""
Generated ETABS Script
Description: Retrieve and list the story drifts for all stories that are designated as 'Master Story' in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 10:11:04
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the names of all defined stories in the model.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: Iterate through each story to identify which ones are designated as 'Master Story' using the 'GetMasterStory' method.
master_stories = []
for story_name in story_names:
    is_master_story, ret = SapModel.Story.GetMasterStory(story_name)
    if is_master_story:
        master_stories.append(story_name)

# Step 3: For each identified 'Master Story', retrieve its story drifts using the 'StoryDrifts' method from the analysis results interface.
# For each identified 'Master Story', retrieve its story drifts.
# First, retrieve all story drift results.
(
    NumberResults,
    Story,
    LoadCase,
    StepType,
    StepNum,
    Direction,
    Drift,
    Label,
    X,
    Y,
    Z,
    ret
) = SapModel.Results.StoryDrifts()

# Initialize a dictionary to store story drifts specifically for master stories.
master_story_drifts = {}

# Iterate through the retrieved results and filter for master stories.
for i in range(NumberResults):
    current_story = Story[i]
    if current_story in master_stories:
        if current_story not in master_story_drifts:
            master_story_drifts[current_story] = []
        
        # Append the drift details for the current master story.
        master_story_drifts[current_story].append({
            "LoadCase": LoadCase[i],
            "StepType": StepType[i],
            "StepNum": StepNum[i],
            "Direction": Direction[i],
            "Drift": Drift[i],
            "Label": Label[i],
            "X": X[i],
            "Y": Y[i],
            "Z": Z[i]
        })


# Step 4: Display the retrieved story drifts for all 'Master Stories'.
print("\nStory Drifts for Master Stories:")
for story, drifts in master_story_drifts.items():
    print(f"\nMaster Story: {story}")
    for drift_data in drifts:
        print(f"  Load Case: {drift_data['LoadCase']}, Direction: {drift_data['Direction']}, Drift: {drift_data['Drift']:.6f}, Label: {drift_data['Label']}, X: {drift_data['X']:.2f}, Y: {drift_data['Y']:.2f}, Z: {drift_data['Z']:.2f}")