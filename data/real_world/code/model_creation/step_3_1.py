#etabs: Draw columns at all grid intersections for each story. Grid intersections are located at coordinates: A-1 (0,0), A-2 (0,20), A-3 (0,40), A-4 (0,60), A-5 (0,80), B-1 (20,0), B-2 (20,20), B-3 (20,40), B-4 (20,60), B-5 (20,80), C-1 (40,0), C-2 (40,20), C-3 (40,40), C-4 (40,60), C-5 (40,80), D-1 (60,0), D-2 (60,20), D-3 (60,40), D-4 (60,60), and D-5 (60,80).For stories 1-3, assign section C20X20 to exterior columns at A-1, A-2, A-3, A-4, A-5, D-1, D-2, D-3, D-4, D-5, B-1, B-5, C-1, and C-5. Assign section C24X24 to interior columns at B-2, B-3, B-4, C-2, C-3, and C-4. For stories 4-5, assign section C18X18 to the same exterior column locations and C20X20 to the same interior column locations. The sections are already developed.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names and elevations of all stories in the model to determine the Z-coordinates for drawing columns. This will provide a mapping of story names to their respective elevations.
base_elevation, number_stories, story_names, story_elevations, story_heights, is_master_story, similar_to_story, splice_above, splice_height, color, ret = SapModel.Story.GetStories_2()

# Create a dictionary to map story names to their elevations
story_elevation_map = dict(zip(story_names, story_elevations))

# Step 2: Define the (X,Y) coordinates for all grid intersections where columns are to be drawn. Specifically, identify and store the coordinates for exterior columns: A-1 (0,0), A-2 (0,20), A-3 (0,40), A-4 (0,60), A-5 (0,80), D-1 (60,0), D-2 (60,20), D-3 (60,40), D-4 (60,60), D-5 (60,80), B-1 (20,0), B-5 (20,80), C-1 (40,0), C-5 (40,80). Also, identify and store the coordinates for interior columns: B-2 (20,20), B-3 (20,40), B-4 (20,60), C-2 (40,20), C-3 (40,40), C-4 (40,60).
exterior_column_coords = [
    (0, 0), (0, 20), (0, 40), (0, 60), (0, 80),  # A-1 to A-5
    (60, 0), (60, 20), (60, 40), (60, 60), (60, 80), # D-1 to D-5
    (20, 0), (20, 80), # B-1, B-5
    (40, 0), (40, 80)  # C-1, C-5
]

interior_column_coords = [
    (20, 20), (20, 40), (20, 60), # B-2, B-3, B-4
    (40, 20), (40, 40), (40, 60)  # C-2, C-3, C-4
]

all_column_coords = exterior_column_coords + interior_column_coords
z1 = story_elevation_map['Story1']
# Draw exterior columns
for x, y in exterior_column_coords:
    column_name, ret = SapModel.FrameObj.AddByCoord(x, y, 0, x, y, z1)
    ret = SapModel.FrameObj.SetSection(column_name, 'C20X20')

# Draw interior columns
for x, y in interior_column_coords:
    column_name, ret = SapModel.FrameObj.AddByCoord(x, y, 0, x, y, z1)
    ret = SapModel.FrameObj.SetSection(column_name, 'C24X24')
# Step 3: Iterate through stories 1, 2, and 3. For each of these stories, iterate through the defined exterior column (X,Y) coordinates and draw a column from the current story's elevation to the next story's elevation. Assign the section property 'C20X20' to these exterior columns. Then, iterate through the defined interior column (X,Y) coordinates and draw a column from the current story's elevation to the next story's elevation. Assign the section property 'C24X24' to these interior columns.
for i in range(3):
    current_story_name = story_names[i]
    next_story_name = story_names[i+1]
    z1 = story_elevation_map[current_story_name]
    z2 = story_elevation_map[next_story_name]

    # Draw exterior columns
    for x, y in exterior_column_coords:
        column_name, ret = SapModel.FrameObj.AddByCoord(x, y, z1, x, y, z2)
        ret = SapModel.FrameObj.SetSection(column_name, 'C20X20')

    # Draw interior columns
    for x, y in interior_column_coords:
        column_name, ret = SapModel.FrameObj.AddByCoord(x, y, z1, x, y, z2)
        ret = SapModel.FrameObj.SetSection(column_name, 'C24X24')

# Step 4: Iterate through stories 4 and 5. For each of these stories, iterate through the defined exterior column (X,Y) coordinates and draw a column from the current story's elevation to the next story's elevation. Assign the section property 'C18X18' to these exterior columns. Then, iterate through the defined interior column (X,Y) coordinates and draw a column from the current story's elevation to the next story's elevation. Assign the section property 'C20X20' to these interior columns.
for i in range(3, 4):
    current_story_name = story_names[i]
    next_story_name = story_names[i+1]
    z1 = story_elevation_map[current_story_name]
    z2 = story_elevation_map[next_story_name]

    # Draw exterior columns
    for x, y in exterior_column_coords:
        column_name, ret = SapModel.FrameObj.AddByCoord(x, y, z1, x, y, z2)
        ret = SapModel.FrameObj.SetSection(column_name, 'C18X18')
        print(ret)

    # Draw interior columns
    for x, y in interior_column_coords:
        column_name, ret = SapModel.FrameObj.AddByCoord(x, y, z1, x, y, z2)
        ret = SapModel.FrameObj.SetSection(column_name, 'C20X20')
        print(ret)

