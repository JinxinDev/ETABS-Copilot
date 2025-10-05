"""
Generated ETABS Script
Description: Identify all columns in the ETABS model, determine their assigned section sizes, and report their grid locations (represented by Cartesian coordinates) to highlight columns with different section sizes.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-19 16:45:50
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Get a list of all frame object names defined in the model.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 2: For each frame object, retrieve the names of its end points. Then, get the Cartesian coordinates for each end point. Based on the Z-coordinates, identify if the frame object is a column (vertical element). If it is a column, retrieve its assigned frame section property name and store the column name, its section property name, and the Cartesian coordinates of its base point.
column_data = []
for frame_ID in frame_ID_tuple:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Check if the frame object is a column (vertical element)
    # Using a small tolerance for floating point comparison
    tolerance = 1e-6
    if abs(X1 - X2) < tolerance and abs(Y1 - Y2) < tolerance and abs(Z1 - Z2) > tolerance:
        section_property, _, ret = SapModel.FrameObj.GetSection(frame_ID)
        
        # Determine the base point (the one with the smaller Z-coordinate)
        if Z1 < Z2:
            base_X, base_Y, base_Z = X1, Y1, Z1
        else:
            base_X, base_Y, base_Z = X2, Y2, Z2
        
        column_data.append({
            "column_name": frame_ID,
            "section_property_name": section_property,
            "base_coordinates": {"X": base_X, "Y": base_Y, "Z": base_Z}
        })

# Step 3: Process the collected column data. Group columns by their assigned section property name. For each group, list the column names and their corresponding Cartesian coordinates (representing grid locations). Finally, identify and report any grid locations where columns have different section sizes.
columns_by_section = {}
sections_by_grid_location = {}

# Process column_data to group by section and identify grid location discrepancies
for column in column_data:
    section_name = column["section_property_name"]
    column_name = column["column_name"]
    base_coords = column["base_coordinates"]
    
    # Group by section property name
    if section_name not in columns_by_section:
        columns_by_section[section_name] = []
    columns_by_section[section_name].append({
        "column_name": column_name,
        "base_coordinates": base_coords
    })

    # Group sections by grid location (X, Y)
    # Round coordinates to handle potential floating point inaccuracies for grid keys
    grid_key = (round(base_coords["X"], 6), round(base_coords["Y"], 6))
    if grid_key not in sections_by_grid_location:
        sections_by_grid_location[grid_key] = set()
    sections_by_grid_location[grid_key].add(section_name)

# Report columns grouped by section property name
print("\n--- Columns Grouped by Section Property Name ---")
if not columns_by_section:
    print("No columns found.")
else:
    for section, cols in columns_by_section.items():
        print(f"  Section: {section}")
        for col_info in cols:
            print(f"    - Column: {col_info['column_name']}, Base Coords: (X={col_info['base_coordinates']['X']:.2f}, Y={col_info['base_coordinates']['Y']:.2f}, Z={col_info['base_coordinates']['Z']:.2f})")

# Identify and report grid locations with columns of different section sizes
print("\n--- Grid Locations with Different Column Section Sizes ---")
found_discrepancy = False
for grid_loc, sections_at_loc in sections_by_grid_location.items():
    if len(sections_at_loc) > 1:
        found_discrepancy = True
        print(f"  Grid Location (X, Y): (X={grid_loc[0]:.2f}, Y={grid_loc[1]:.2f}) has columns with different sections:")
        for section in sections_at_loc:
            print(f"    - Section: {section}")

if not found_discrepancy:
    print("  No grid locations found with columns of different section sizes.")