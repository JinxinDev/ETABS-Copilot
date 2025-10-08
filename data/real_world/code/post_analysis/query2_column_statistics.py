#etabs: For all columns on story 1, extract axial forces under all four load combinations. For each column, calculate and report: column label, grid location, mean axial force across all combinations, maximum axial force with governing combination, minimum axial force with governing combination, standard deviation of axial forces, and the range between maximum and minimum. Identify the three columns with highest mean axial loads.

import comtypes.client
import statistics

helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names of all frame objects on 'Story1'.
story_name = "Story1"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

if ret != 0:
    print(f"Error retrieving frame objects for story {story_name}: {ret}")
    exit()

# Step 2: Identify columns by checking vertical orientation
columns_data = []
vertical_tolerance = 1e-3

for frame_ID in frame_ID_tuple:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
    if ret != 0:
        continue
    
    X1, Y1, Z1, ret1 = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret2 = SapModel.PointObj.GetCoordCartesian(point_2)
    
    if ret1 == 0 and ret2 == 0:
        # Check if vertical (Z-coordinates differ significantly)
        if abs(Z2 - Z1) > vertical_tolerance:
            columns_data.append({
                "label": frame_ID,
                "point1_coords": (X1, Y1, Z1),
                "point2_coords": (X2, Y2, Z2)
            })

# Step 3: Retrieve grid system data and map columns to grid locations
num_of_grid, grid_name_tuple, ret = SapModel.GridSys.GetNameList()
all_x_grid_lines = []
all_y_grid_lines = []

for grid_name in grid_name_tuple:
    Xo, Yo, RZ, StoryRangeIsDefault, TopStory, BottomStory, BubbleSize, GridColor, \
    NumXLines, GridLineIDX, OrdinateX, VisibleX, BubbleLocX, \
    NumYLines, GridLineIDY, OrdinateY, VisibleY, BubbleLocY, \
    NumGenLines, GridLineIDGen, GenOrdX1, GenOrdY1, GenOrdX2, GenOrdY2, VisibleGen, BubbleLocGen, ret \
    = SapModel.GridSys.GetGridSysCartesian(grid_name)
    
    for i in range(NumXLines):
        all_x_grid_lines.append((GridLineIDX[i], OrdinateX[i]))
    for i in range(NumYLines):
        all_y_grid_lines.append((GridLineIDY[i], OrdinateY[i]))

# Map columns to grid locations
for column in columns_data:
    col_X, col_Y, col_Z = column["point1_coords"]
    
    closest_X_label = "N/A"
    min_dist_X = float('inf')
    for x_label, x_ordinate in all_x_grid_lines:
        dist_X = abs(col_X - x_ordinate)
        if dist_X < min_dist_X:
            min_dist_X = dist_X
            closest_X_label = x_label
    
    closest_Y_label = "N/A"
    min_dist_Y = float('inf')
    for y_label, y_ordinate in all_y_grid_lines:
        dist_Y = abs(col_Y - y_ordinate)
        if dist_Y < min_dist_Y:
            min_dist_Y = dist_Y
            closest_Y_label = y_label
    
    if closest_X_label != "N/A" and closest_Y_label != "N/A":
        column["grid_location"] = f"{closest_Y_label}-{closest_X_label}"
    else:
        column["grid_location"] = "N/A"

# Step 4: Get all load combination names and select all for output
NumCombos, ComboNames, ret = SapModel.RespCombo.GetNameList()

if ret != 0:
    print(f"Error retrieving combination names: {ret}")
    exit()

# Select all combinations for output
for combo_name in ComboNames:
    ret_select = SapModel.Results.Setup.SetComboSelectedForOutput(combo_name, True)
    if ret_select != 0:
        print(f"Warning: Could not select combo {combo_name} for output")

# Extract axial forces for all columns
column_axial_forces = []

for column in columns_data:
    column_label = column["label"]
    
    # Retrieve frame force results for the column (all selected combinations)
    NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret \
        = SapModel.Results.FrameForce(column_label, 0)
    
    if ret == 0 and NumberResults > 0:
        # Group forces by load combination
        combo_forces = {}
        for i in range(NumberResults):
            combo = LoadCase[i]
            axial_force = P[i]/1000
            
            # Store maximum absolute axial force for each combination
            if combo not in combo_forces:
                combo_forces[combo] = []
            combo_forces[combo].append(axial_force)
        
        # For each combination, take the axial force with maximum absolute value
        for combo, forces in combo_forces.items():
            max_abs_force = max(forces, key=abs)
            column_axial_forces.append({
                "column_label": column_label,
                "load_combination": combo,
                "axial_force_P": max_abs_force
            })

# Step 5: Calculate statistics for each column
column_force_statistics = []

for column in columns_data:
    column_label = column["label"]
    grid_location = column.get("grid_location", "N/A")
    
    # Filter axial forces for the current column
    forces_for_column = [
        item for item in column_axial_forces
        if item["column_label"] == column_label and item["axial_force_P"] is not None
    ]
    
    if not forces_for_column:
        column_force_statistics.append({
            "column_label": column_label,
            "grid_location": grid_location,
            "mean_axial_force": None,
            "max_axial_force": None,
            "min_axial_force": None,
            "max_combo": None,
            "min_combo": None,
            "std_dev_axial_force": None,
            "range_axial_force": None
        })
        continue
    
    axial_forces_values = [item["axial_force_P"] for item in forces_for_column]
    
    # Calculate statistics
    mean_force = statistics.mean(axial_forces_values)
    max_force = max(axial_forces_values)
    min_force = min(axial_forces_values)
    
    # Find governing combinations
    max_combo = next(item["load_combination"] for item in forces_for_column if item["axial_force_P"] == max_force)
    min_combo = next(item["load_combination"] for item in forces_for_column if item["axial_force_P"] == min_force)
    
    std_dev_force = statistics.stdev(axial_forces_values) if len(axial_forces_values) > 1 else 0.0
    range_force = max_force - min_force
    
    column_force_statistics.append({
        "column_label": column_label,
        "grid_location": grid_location,
        "mean_axial_force": mean_force,
        "max_axial_force": max_force,
        "min_axial_force": min_force,
        "max_combo": max_combo,
        "min_combo": min_combo,
        "std_dev_axial_force": std_dev_force,
        "range_axial_force": range_force
    })

# Step 6: Report statistics
print("\n--- Column Axial Force Statistics ---")
print(f"{"Column":<15} {"Grid":<10} {"Mean (kips)":<15} {"Max (kips)":<15} {"Max Combo":<20} {"Min (kips)":<15} {"Min Combo":<20} {"Std Dev":<15} {"Range":<15}")
print("-" * 150)

for stats in column_force_statistics:
    if stats["mean_axial_force"] is not None:
        print(f"{stats['column_label']:<15} {stats['grid_location']:<10} {stats['mean_axial_force']:<15.2f} {stats['max_axial_force']:<15.2f} {stats['max_combo']:<20} {stats['min_axial_force']:<15.2f} {stats['min_combo']:<20} {stats['std_dev_axial_force']:<15.2f} {stats['range_axial_force']:<15.2f}")
    else:
        print(f"{stats['column_label']:<15} {stats['grid_location']:<10} No valid data")

# Step 7: Identify top 3 columns by mean axial load
valid_columns = [col for col in column_force_statistics if col["mean_axial_force"] is not None]
sorted_columns = sorted(valid_columns, key=lambda x: abs(x["mean_axial_force"]), reverse=True)
top_3_columns = sorted_columns[:3]

print("\n--- Top 3 Columns by Mean Axial Load ---")
for i, col in enumerate(top_3_columns, 1):
    print(f"Rank {i}: {col['column_label']} (Grid: {col['grid_location']}) - Mean: {col['mean_axial_force']:.2f} kips")
