#etabs: Draw beams at each story. Along grid lines 1 through 5 (Y = 0, 20, 40, 60, 80 feet). Along grid lines A through D (X = 0, 20, 40, 60 feet). Assign existing section B12X24 to all beams.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names and elevations of all stories in the model
base_elevation, number_stories, story_names, story_elevations, story_heights, is_master_story, similar_to_story, splice_above, splice_height, color, ret = SapModel.Story.GetStories_2()

print(f"Number of stories: {number_stories}")
for i in range(number_stories):
    print(f"Story Name: {story_names[i]}, Elevation: {story_elevations[i]:.2f} ft")

# Define grid lines and beam section
y_grid_lines = [0.0, 20.0, 40.0, 60.0, 80.0]
x_grid_lines = [0.0, 20.0, 40.0, 60.0]
beam_section_name = 'B12X24'

# Step 2: Draw beams in X-direction (along Y-grid lines) with segments between adjacent X-grid points
for i in range(number_stories):
    current_story_elevation = story_elevations[i]
    
    # For each Y-grid line, draw beam segments connecting adjacent X-grid points
    for y_coord in y_grid_lines:
        for j in range(len(x_grid_lines) - 1):
            x1 = x_grid_lines[j]
            x2 = x_grid_lines[j + 1]
            
            # Add beam from (x1, y_coord) to (x2, y_coord)
            beam_name, ret = SapModel.FrameObj.AddByCoord(
                x1, y_coord, current_story_elevation,
                x2, y_coord, current_story_elevation
            )
            
            # Assign section property
            ret = SapModel.FrameObj.SetSection(beam_name, beam_section_name)
            if ret == 0:
                print(f"Created beam {beam_name} at story {story_names[i]}: ({x1},{y_coord}) to ({x2},{y_coord})")

# Step 3: Draw beams in Y-direction (along X-grid lines) with segments between adjacent Y-grid points
for i in range(number_stories):
    current_story_elevation = story_elevations[i]
    
    # For each X-grid line, draw beam segments connecting adjacent Y-grid points
    for x_coord in x_grid_lines:
        for j in range(len(y_grid_lines) - 1):
            y1 = y_grid_lines[j]
            y2 = y_grid_lines[j + 1]
            
            # Add beam from (x_coord, y1) to (x_coord, y2)
            beam_name, ret = SapModel.FrameObj.AddByCoord(
                x_coord, y1, current_story_elevation,
                x_coord, y2, current_story_elevation
            )
            
            # Assign section property
            ret = SapModel.FrameObj.SetSection(beam_name, beam_section_name)
            if ret == 0:
                print(f"Created beam {beam_name} at story {story_names[i]}: ({x_coord},{y1}) to ({x_coord},{y2})")

print("\nBeam creation complete!")