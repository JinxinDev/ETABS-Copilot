"""
Generated ETABS Script
Description: Retrieve and list all distributed and point loads applied to frame objects in the ETABS model, including their magnitudes and associated load patterns.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 17:42:47
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all defined load pattern names in the model.
num_of_load_patterns, load_pattern_names, ret = SapModel.LoadPatterns.GetNameList()

# Step 2: Retrieve a list of all defined frame object names in the model.
num_of_frame_objects, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 3: For each frame object, iterate through all retrieved load patterns and get any distributed load assignments, including the load pattern name, coordinate system, direction, and magnitudes.
all_distributed_loads = []

for frame_obj_name in frame_object_names:
    # Call GetLoadDistributed for the current frame object.
    # The method returns a tuple where the output parameters are followed by the return code.
    number_items, frame_names_out, load_pats_out, my_types_out, csys_out, dirs_out, rd1_out, rd2_out, dist1_out, dist2_out, val1_out, val2_out, ret = \
        SapModel.FrameObj.GetLoadDistributed(frame_obj_name)

    if ret == 0: # Check if the API call was successful
        for i in range(number_items):
            distributed_load_data = {
                "FrameName": frame_names_out[i],
                "LoadPattern": load_pats_out[i],
                "LoadType": my_types_out[i], # 1 for force, 2 for moment
                "CoordinateSystem": csys_out[i],
                "Direction": dirs_out[i], # e.g., 1=X, 2=Y, 3=Z, 4=Local1, 5=Local2, 6=Local3, 7=ProjX, 8=ProjY, 9=ProjZ, 10=Gravity
                "RelativeDistance1": rd1_out[i],
                "RelativeDistance2": rd2_out[i],
                "AbsoluteDistance1": dist1_out[i],
                "AbsoluteDistance2": dist2_out[i],
                "Value1": val1_out[i], # Load magnitude at Dist1/RD1
                "Value2": val2_out[i]  # Load magnitude at Dist2/RD2
            }
            all_distributed_loads.append(distributed_load_data)


# Step 4: For each frame object, iterate through all retrieved load patterns and get any point load assignments, including the load pattern name, coordinate system, direction, and magnitudes.
all_point_loads = []

for frame_obj_name in frame_object_names:
    # Call GetLoadPoint for the current frame object.
    # The method returns a tuple where the output parameters are followed by the return code.
    number_items, frame_names_out, load_pats_out, my_types_out, csys_out, dirs_out, rel_dist_out, abs_dist_out, val_out, ret = \
        SapModel.FrameObj.GetLoadPoint(frame_obj_name)

    if ret == 0: # Check if the API call was successful
        for i in range(number_items):
            point_load_data = {
                "FrameName": frame_names_out[i],
                "LoadPattern": load_pats_out[i],
                "LoadType": my_types_out[i], # 1 for force, 2 for moment
                "CoordinateSystem": csys_out[i],
                "Direction": dirs_out[i], # e.g., 1=X, 2=Y, 3=Z, 4=Local1, 5=Local2, 6=Local3, 7=ProjX, 8=ProjY, 9=ProjZ, 10=Gravity
                "RelativeDistance": rel_dist_out[i],
                "AbsoluteDistance": abs_dist_out[i],
                "Value": val_out[i] # Load magnitude
            }
            all_point_loads.append(point_load_data)

# Step 5: Process and present the collected distributed and point load data, displaying the frame object name, load pattern, load type (distributed/point), direction, and magnitude for each applied load.
# Helper dictionaries for better readability
load_type_map = {1: "Force", 2: "Moment"}
direction_map = {
    1: "X", 2: "Y", 3: "Z",
    4: "Local1", 5: "Local2", 6: "Local3",
    7: "ProjX", 8: "ProjY", 9: "ProjZ",
    10: "Gravity"
}

print("\n--- Applied Loads Summary ---")

# Process and present distributed loads
if all_distributed_loads:
    print("\nDistributed Loads:")
    for load in all_distributed_loads:
        load_type_str = load_type_map.get(load["LoadType"], f"Unknown ({load['LoadType']})")
        direction_str = direction_map.get(load["Direction"], f"Unknown ({load['Direction']})")
        print(f"  Frame: {load['FrameName']}, Pattern: {load['LoadPattern']}, Type: {load_type_str} (Distributed)")
        print(f"    Direction: {direction_str}, CSys: {load['CoordinateSystem']}")
        print(f"    Magnitude: {load['Value1']:.3f} to {load['Value2']:.3f} (at RelDist {load['RelativeDistance1']:.2f} to {load['RelativeDistance2']:.2f})")
else:
    print("\nNo distributed loads found.")

# Process and present point loads
if all_point_loads:
    print("\nPoint Loads:")
    for load in all_point_loads:
        load_type_str = load_type_map.get(load["LoadType"], f"Unknown ({load['LoadType']})")
        direction_str = direction_map.get(load["Direction"], f"Unknown ({load['Direction']})")
        print(f"  Frame: {load['FrameName']}, Pattern: {load['LoadPattern']}, Type: {load_type_str} (Point)")
        print(f"    Direction: {direction_str}, CSys: {load['CoordinateSystem']}")
        print(f"    Magnitude: {load['Value']:.3f} (at RelDist {load['RelativeDistance']:.2f})")
else:
    print("\nNo point loads found.")