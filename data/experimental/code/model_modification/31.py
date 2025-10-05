"""
Generated ETABS Script
Description: Create 'Dead' and 'Live' load patterns, apply uniform loads to all slab objects and distributed loads to all beam objects, then verify the load assignments.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 10:53:08
Steps: 13
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new load pattern named 'Dead' with a load type of 'Dead' and a self-weight multiplier of 1.0.
SapModel.LoadPatterns.Add("Dead", 1, 1.0, True)

# Step 2: Add a new load pattern named 'Live' with a load type of 'Live' and a self-weight multiplier of 0.0.
SapModel.LoadPatterns.Add("Live", 3, 0.0, True)

# Step 3: Retrieve a list of all story names defined in the model.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 4: For each story, retrieve the names of all defined area objects (slabs).
story_slabs = {}
for story_name in story_names:
    num_slabs, slab_names_tuple, ret = SapModel.AreaObj.GetNameListOnStory(story_name)
    story_slabs[story_name] = list(slab_names_tuple)

# Step 5: Iterate through all retrieved slab names and assign a uniform load of 1.0 (e.g., kN/m^2 or kip/ft^2) under the 'Dead' load pattern.
# Iterate through all retrieved slab names and assign a uniform load.
load_pattern_name = "Dead"
load_value = 1.0 # kip/ft^2
load_direction = 10 # Gravity direction
coordinate_system = "Global"
replace_existing_load = True
item_type = 0 # 0 for a single object

for story_name, slab_names in story_slabs.items():
    for slab_name in slab_names:
        ret = SapModel.AreaObj.SetLoadUniform(
            slab_name,
            load_pattern_name,
            load_value,
            load_direction,
            replace_existing_load,
            coordinate_system,
            item_type
        )

# Step 6: Iterate through all retrieved slab names and assign a uniform load of 2.0 (e.g., kN/m^2 or kip/ft^2) under the 'Live' load pattern.
# Iterate through all retrieved slab names and assign a uniform load.
load_pattern_name = "Live"
load_value = 2.0 # kip/ft^2
load_direction = 10 # Gravity direction
coordinate_system = "Global"
replace_existing_load = True
item_type = 0 # 0 for a single object

for story_name, slab_names in story_slabs.items():
    for slab_name in slab_names:
        ret = SapModel.AreaObj.SetLoadUniform(
            slab_name,
            load_pattern_name,
            load_value,
            load_direction,
            replace_existing_load,
            coordinate_system,
            item_type
        )

# Step 7: For each story, retrieve the names of all defined frame objects (beams).
# Step 7: For each story, retrieve the names of all defined frame objects (beams).
story_frames = {}
for story_name in story_names:
    num_frames, frame_names_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    story_frames[story_name] = list(frame_names_tuple)

# Step 8: Iterate through all retrieved beam names and assign a distributed load of 0.5 (e.g., kN/m or kip/ft) under the 'Dead' load pattern.
# Step 8: Iterate through all retrieved beam names and assign a distributed load of 0.5 (kip/ft) under the 'Dead' load pattern.
load_pattern_name = "Dead"
load_value = 0.5 # kip/ft
load_type = 1 # 1 for Force per unit length
load_direction = 10 # Gravity direction
start_dist = 0.0 # Start load at 0% of the frame length
end_dist = 1.0 # End load at 100% of the frame length
start_value = load_value # Uniform load
end_value = load_value # Uniform load
coordinate_system = "Global"
relative_distance = True # Distances are relative (0 to 1)
replace_existing_load = True
item_type = 0 # 0 for a single object

for story_name, frame_names in story_frames.items():
    for frame_name in frame_names:
        ret = SapModel.FrameObj.SetLoadDistributed(
            frame_name,
            load_pattern_name,
            load_type,
            load_direction,
            start_dist,
            end_dist,
            start_value,
            end_value,
            coordinate_system,
            relative_distance,
            replace_existing_load,
            item_type
        )

# Step 9: Iterate through all retrieved beam names and assign a distributed load of 1.0 (e.g., kN/m or kip/ft) under the 'Live' load pattern.
# Step 9: Iterate through all retrieved beam names and assign a distributed load of 1.0 (kip/ft) under the 'Live' load pattern.
load_pattern_name = "Live"
load_value = 1.0 # kip/ft
load_type = 1 # 1 for Force per unit length
load_direction = 10 # Gravity direction
start_dist = 0.0 # Start load at 0% of the frame length
end_dist = 1.0 # End load at 100% of the frame length
start_value = load_value # Uniform load
end_value = load_value # Uniform load
coordinate_system = "Global"
relative_distance = True # Distances are relative (0 to 1)
replace_existing_load = True
item_type = 0 # 0 for a single object

for story_name, frame_names in story_frames.items():
    for frame_name in frame_names:
        ret = SapModel.FrameObj.SetLoadDistributed(
            frame_name,
            load_pattern_name,
            load_type,
            load_direction,
            start_dist,
            end_dist,
            start_value,
            end_value,
            coordinate_system,
            relative_distance,
            replace_existing_load,
            item_type
        )