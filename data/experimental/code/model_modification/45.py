"""
Generated ETABS Script
Description: Create two live load patterns, 'LIVE' and 'ROOF_LIVE', and apply uniform loads to the respective floor and roof slabs.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-12 10:52:43
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new load pattern named 'LIVE' to the model.
SapModel.LoadPatterns.Add("LIVE", 3, 0.0, True)

# Step 2: Set the load type for the 'LIVE' load pattern to 'Live'.
SapModel.LoadPatterns.SetLoadType("LIVE", 3)

# Step 3: Retrieve the names of all stories in the model to identify floor and roof levels.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 4: For each story that is not the roof level, retrieve all area objects (slabs) on that story and apply a uniform load of 0.08 ksf (80 psf) using the 'LIVE' load pattern.
# Identify the roof story (assuming the last story in the list is the roof)
roof_story = story_names[-1]

# Define load parameters
load_pattern = "LIVE"
load_value = 0.08  # 0.08 ksf (80 psf)
load_direction = 10  # Gravity direction
replace_existing_load = True
coordinate_system = "Global"
item_type_object = 0 # 0 for a single Object

# Iterate through each story
for story_name in story_names:
    # Skip the roof story
    if story_name == roof_story:
        continue

    # Get all area objects (slabs) on the current story
    num_area_objects, area_object_names, ret = SapModel.AreaObj.GetNameListOnStory(story_name)

    # Apply uniform load to each area object on this story
    for area_obj_name in area_object_names:
        ret = SapModel.AreaObj.SetLoadUniform(
            area_obj_name,
            load_pattern,
            load_value,
            load_direction,
            replace_existing_load,
            coordinate_system,
            item_type_object
        )

# Step 5: Add a new load pattern named 'ROOF_LIVE' to the model.
# Step 5: Add a new load pattern named 'ROOF_LIVE' to the model.
SapModel.LoadPatterns.Add("ROOF_LIVE", 3, 0.0, True)

# Step 6: Set the load type for the 'ROOF_LIVE' load pattern to 'Roof Live'.
SapModel.LoadPatterns.SetLoadType("ROOF_LIVE", 4)

# Step 7: Retrieve all area objects (slabs) on the roof level story and apply a uniform load of 0.03 ksf (30 psf) using the 'ROOF_LIVE' load pattern.
# Define load parameters for roof live load
roof_load_pattern = "ROOF_LIVE"
roof_load_value = 0.03  # 0.03 ksf (30 psf)
roof_load_direction = 10  # Gravity direction
roof_replace_existing_load = True
roof_coordinate_system = "Global"
roof_item_type_object = 0 # 0 for a single Object

# Get all area objects (slabs) on the roof story
num_roof_area_objects, roof_area_object_names, ret = SapModel.AreaObj.GetNameListOnStory(roof_story)

# Apply uniform load to each area object on the roof story
for area_obj_name in roof_area_object_names:
    ret = SapModel.AreaObj.SetLoadUniform(
        area_obj_name,
        roof_load_pattern,
        roof_load_value,
        roof_load_direction,
        roof_replace_existing_load,
        roof_coordinate_system,
        roof_item_type_object
    )