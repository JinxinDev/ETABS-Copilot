"""
Generated ETABS Script
Description: Increase the section depth of all concrete beams by 4 inches for all stories below the 3rd floor in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-15 11:20:40
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all stories in the model.
number_of_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: For each story, retrieve its elevation to identify stories below the 3rd floor. Assume 'Story 3' is the reference for the 3rd floor.
story_elevations = {}
for story_name in story_names:
    elevation, ret = SapModel.Story.GetElevation(story_name)
    story_elevations[story_name] = elevation

story3_elevation = story_elevations.get('Story3', float('inf'))
stories_below_story3 = []
for story_name, elevation in story_elevations.items():
    if elevation < story3_elevation:
        stories_below_story3.append(story_name)

# Step 3: Retrieve the names of all defined frame section properties in the model.
number_of_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 4: Iterate through each frame section property. For each section, retrieve its rectangular properties to check if it's a rectangular section and get its material name. Then, retrieve the material properties to confirm if it's a concrete material. Store the names and current depths of all identified concrete rectangular beam sections.
concrete_rectangular_beam_sections = []

for section_name in frame_section_names:
    # Attempt to get rectangular properties. T3 is depth, T2 is width.
    FileName, MatProp, T3, T2, Color, Notes, GUID, ret_rect = SapModel.PropFrame.GetRectangle(section_name)

    if ret_rect == 0: # It's a rectangular section
        # Get material properties to check if it's concrete
        MatType, MatColor, MatNotes, MatGUID, ret_mat = SapModel.PropMaterial.GetMaterial(MatProp)

        if ret_mat == 0 and MatType == 2: # It's a concrete material
            # Check if it's a beam by attempting to get beam reinforcement data
            MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret_rebar_beam = SapModel.PropFrame.GetRebarBeam(section_name)

            if ret_rebar_beam == 0: # It's a concrete beam section with reinforcement defined
                concrete_rectangular_beam_sections.append((section_name, T3))

# Step 5: For each identified concrete rectangular beam section, create a new frame section property. The new section will have the same width and material as the original, but its depth will be increased by 4 inches. Assign a new unique name to this modified section (e.g., by appending '_plus_4in' to the original name).
modified_beam_sections = []

for original_section_name, original_depth_ft in concrete_rectangular_beam_sections:
    new_section_name = original_section_name + '_plus_4in'
    
    # Convert 4 inches to feet for consistency with model units (kip_ft_F)
    depth_increase_ft = 4 / 12.0
    new_depth_ft = original_depth_ft + depth_increase_ft

    # Retrieve original section properties to get material and width (T2)
    # T3_orig here will be the same as original_depth_ft
    FileName, MatProp, T3_orig, T2_orig, Color, Notes, GUID, ret_rect = SapModel.PropFrame.GetRectangle(original_section_name)
    if ret_rect == 0: # Successfully retrieved original rectangular properties
        # Create the new rectangular section with increased depth
        ret_set_rect = SapModel.PropFrame.SetRectangle(new_section_name, MatProp, new_depth_ft, T2_orig)

        if ret_set_rect == 0:
            # Retrieve beam rebar data from the original section
            MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret_rebar_beam = SapModel.PropFrame.GetRebarBeam(original_section_name)

            if ret_rebar_beam == 0: # Original section had beam rebar data
                # Apply the same rebar data to the new section
                ret_set_rebar = SapModel.PropFrame.SetRebarBeam(new_section_name, MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea)
                if ret_set_rebar == 0:
                    modified_beam_sections.append(new_section_name)
            else:
                # If original section had no rebar data, the new one won't either (or will have default)
                modified_beam_sections.append(new_section_name)

# Step 6: Iterate through the stories identified as being below the 3rd floor. For each of these stories, retrieve the names of all frame objects (beams) present on that story.
frame_objects_below_story3 = {}
for story_name in stories_below_story3:
    number_of_frames, frame_names, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    if ret == 0:
        frame_objects_below_story3[story_name] = frame_names

# Step 7: For each frame object (beam) on the selected stories, retrieve its currently assigned section property. If this section property matches one of the original concrete beam sections that were modified, assign the corresponding newly created section property (with increased depth) to this frame object.
original_to_modified_section_map = {}
for original_section_name, _ in concrete_rectangular_beam_sections:
    new_section_name = original_section_name + '_plus_4in'
    original_to_modified_section_map[original_section_name] = new_section_name

for story_name, frame_names in frame_objects_below_story3.items():
    for frame_name in frame_names:
        # Retrieve the current section property of the frame object
        current_section_property, _, ret_get_section = SapModel.FrameObj.GetSection(frame_name)

        if ret_get_section == 0:
            # Check if this section property is one of the original concrete beam sections that were modified
            if current_section_property in original_to_modified_section_map:
                # Get the corresponding newly created section property
                new_section_to_assign = original_to_modified_section_map[current_section_property]

                # Assign the new section property to the frame object
                ret_set_section = SapModel.FrameObj.SetSection(frame_name, new_section_to_assign)
                # Optional: Add error handling or logging for SetSection if needed
                # if ret_set_section != 0:
                #     print(f"Error assigning new section {new_section_to_assign} to frame {frame_name}")