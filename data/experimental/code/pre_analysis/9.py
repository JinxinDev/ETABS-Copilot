"""
Generated ETABS Script
Description: Retrieve the names of all stories in the model, then for each story, count the number of frame objects and area objects present on that story, and finally, present these counts per story.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 20:33:59
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all defined story names in the ETABS model.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Check if the API call was successful
if ret == 0:
    print(f"Successfully retrieved {num_stories} story names.")
    # story_names is a tuple of strings, e.g., ('Story1', 'Story2', 'Roof')
else:
    print(f"Error retrieving story names. Return code: {ret}")

# Step 2: Iterate through each retrieved story name. For each story, get a list of all frame objects located on that specific story.
frames_on_stories = {}

if ret == 0: # Check if story_names was successfully retrieved in the previous step
    for story_name in story_names:
        # Get a list of all frame objects on the current story
        frame_obj_num, frame_ID_tuple, ret_frame = SapModel.FrameObj.GetNameListOnStory(story_name)
        
        if ret_frame == 0:
            print(f"Successfully retrieved {frame_obj_num} frame objects on story '{story_name}'.")
            # Store the frame IDs for this story
            frames_on_stories[story_name] = list(frame_ID_tuple) # Convert tuple to list for easier manipulation later
        else:
            print(f"Error retrieving frame objects for story '{story_name}'. Return code: {ret_frame}")
else:
    print("Cannot proceed: Story names were not successfully retrieved in the previous step.")

# Step 3: For each story, get a list of all area objects located on that specific story.
area_on_stories = {}

if ret == 0: # Check if story_names was successfully retrieved in the initial step
    for story_name in story_names:
        # Get a list of all area objects on the current story
        area_obj_num, area_ID_tuple, ret_area = SapModel.AreaObj.GetNameListOnStory(story_name)
        
        if ret_area == 0:
            print(f"Successfully retrieved {area_obj_num} area objects on story '{story_name}'.")
            # Store the area IDs for this story
            area_on_stories[story_name] = list(area_ID_tuple) # Convert tuple to list for easier manipulation later
        else:
            print(f"Error retrieving area objects for story '{story_name}'. Return code: {ret_area}")
else:
    print("Cannot proceed: Story names were not successfully retrieved in the initial step.")

# Step 4: For each story, count the number of frame objects and area objects obtained in the previous steps. Store these counts, associating them with their respective story names.
# Step 4: For each story, count the number of frame objects and area objects.
story_object_counts = {}

if ret == 0: # Check if story_names was successfully retrieved in the initial step
    for story_name in story_names:
        frame_count = len(frames_on_stories.get(story_name, []))
        area_count = len(area_on_stories.get(story_name, []))
        
        story_object_counts[story_name] = {
            'frames': frame_count,
            'areas': area_count
        }
        print(f"Story '{story_name}': {frame_count} frame objects, {area_count} area objects.")
else:
    print("Cannot proceed: Story names were not successfully retrieved in the initial step.")


# Step 5: Present the total counts of frame and area objects for each story level.
# Step 5: Present the total counts of frame and area objects for each story level.

print("\n--- Object Counts Per Story ---")
if story_object_counts:
    for story_name, counts in story_object_counts.items():
        print(f"Story '{story_name}':")
        print(f"  Total Frame Objects: {counts['frames']}")
        print(f"  Total Area Objects: {counts['areas']}")
else:
    print("No object counts available. Ensure previous steps ran successfully.")