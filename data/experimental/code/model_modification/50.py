"""
Generated ETABS Script
Description: Draw columns using the 'C24x24' section at all grid intersections on the first floor.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 20:17:36
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names, elevations, and heights of all stories in the model to identify the 'first floor' and the story directly above it. This information is crucial for determining the start and end Z-coordinates for the columns.
number_names, story_names, ret = SapModel.Story.GetNameList()

story_data = []
for name in story_names:
    elevation, ret_elev = SapModel.Story.GetElevation(name)
    height, ret_height = SapModel.Story.GetHeight(name)
    story_data.append({
        "name": name,
        "elevation": elevation,
        "height": height
    })

# Sort stories by elevation to easily identify the 'first floor' and the one above it
story_data.sort(key=lambda x: x["elevation"])

# The 'first floor' would typically be the lowest story (story_data[0] if elevation is 0 or lowest positive)
# and the story directly above it would be story_data[1] (if it exists).

# Step 2: Retrieve the names of all defined grid systems and then get the X and Y coordinates of the grid lines for the primary grid system. This will allow for the calculation of all grid intersection points.
number_of_grid_systems, grid_system_names, ret = SapModel.GridSys.GetNameList()

if number_of_grid_systems > 0:
    primary_grid_system_name = grid_system_names[0]
    
    # Retrieve grid line coordinates for the primary grid system
    (Xo, Yo, RZ, GridSysType, NumXLines, NumYLines, GridLineIDX, GridLineIDY, OrdinateX, OrdinateY, VisibleX, VisibleY, BubbleLocX, BubbleLocY, ret) = SapModel.GridSys.GetGridSys_2(primary_grid_system_name)

    # OrdinateX and OrdinateY now contain the X and Y coordinates of the grid lines
    # These can be used to calculate intersection points later.

# Step 3: Iterate through all calculated grid intersection points on the first floor. For each intersection, add a new vertical column frame object using the 'C24x24' section property. The column should extend from the elevation of the first floor to the elevation of the story directly above it.
if len(story_data) >= 2 and number_of_grid_systems > 0:
    first_floor_elevation = story_data[0]["elevation"]
    story_above_first_floor_elevation = story_data[1]["elevation"]

    column_section_name = 'C24x24'

    for x_coord in OrdinateX:
        for y_coord in OrdinateY:
            # Define start and end coordinates for the column
            x1 = x_coord
            y1 = y_coord
            z1 = first_floor_elevation

            x2 = x_coord
            y2 = y_coord
            z2 = story_above_first_floor_elevation
            print(x1, y1, z1, x2, y2, z2)
            # Add the column frame object
            column_name, ret = SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2)

            # Assign the 'C24x24' section property to the new column
            if ret == 0:
                ret = SapModel.FrameObj.SetSection(column_name, column_section_name)
            else:
                # Handle error if column creation failed
                print(f"Error adding column at ({x1}, {y1}, {z1}) to ({x2}, {y2}, {z2}): {ret}")
else:
    print("Not enough stories or no grid systems defined to place columns.")