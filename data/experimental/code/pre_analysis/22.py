"""
Generated ETABS Script
Description: Identify all frame objects classified as beams that have more than one distributed load assigned to them under the same load pattern. Beams are defined as horizontal frame elements.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 17:08:33
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects currently defined in the ETABS model.
frame_obj_count, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 2: For each frame object, retrieve the names of its start and end point objects. Then, for each point object, get its Cartesian coordinates (X, Y, Z) to determine if the frame object is a horizontal beam (i.e., its start and end Z-coordinates are approximately equal). Filter the list to include only beam objects.
beam_objects = []
tolerance = 0.01 # Define a small tolerance for Z-coordinate comparison (in feet)

for frame_name in frame_object_names:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1_name, point_2_name, ret = SapModel.FrameObj.GetPoints(frame_name)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1_name)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2_name)

    # Check if the Z-coordinates are approximately equal to identify horizontal beams.
    if abs(Z1 - Z2) < tolerance:
        beam_objects.append(frame_name)


# Step 3: For each identified beam object, retrieve all distributed load assignments. This will include the load pattern, load type, direction, and magnitude for each distributed load.
beam_distributed_loads = {}

for beam_name in beam_objects:
    # Retrieve all distributed load assignments for the current beam object.
    # The method returns multiple arrays, one for each load property.
    number_items, frame_names, load_pats, my_types, csys_list, dirs, rd1_list, rd2_list, dist1_list, dist2_list, val1_list, val2_list, ret = SapModel.FrameObj.GetLoadDistributed(beam_name)

    # Initialize a list to store loads for the current beam.
    beam_distributed_loads[beam_name] = []

    # Iterate through the retrieved load items and store their details.
    for i in range(number_items):
        load_data = {
            "LoadPattern": load_pats[i],
            "LoadType": my_types[i], # 1 = Force/Length, 2 = Moment/Length
            "CoordinateSystem": csys_list[i],
            "Direction": dirs[i],
            "RelativeDistance1": rd1_list[i],
            "RelativeDistance2": rd2_list[i],
            "ActualDistance1": dist1_list[i],
            "ActualDistance2": dist2_list[i],
            "Value1": val1_list[i],
            "Value2": val2_list[i]
        }
        beam_distributed_loads[beam_name].append(load_data)
# Step 4: Process the retrieved distributed loads for each beam. Group the loads by their respective load patterns. For each load pattern, count how many distributed loads are assigned to the current beam.
beam_loads_by_pattern = {}

for beam_name, loads in beam_distributed_loads.items():
    # Initialize a dictionary to store load pattern counts for the current beam.
    load_pattern_counts = {}
    for load_data in loads:
        load_pattern = load_data["LoadPattern"]
        # Increment the count for the current load pattern.
        load_pattern_counts[load_pattern] = load_pattern_counts.get(load_pattern, 0) + 1
    # Store the grouped and counted loads for the current beam.
    beam_loads_by_pattern[beam_name] = load_pattern_counts

# Step 5: Identify and store the names of all beams where at least one load pattern has more than one distributed load assigned to it. These are the 'problematic' beams.
problematic_beams = []

for beam_name, load_pattern_counts in beam_loads_by_pattern.items():
    for count in load_pattern_counts.values():
        if count > 1:
            problematic_beams.append(beam_name)
            break # No need to check other load patterns for this beam, it's already problematic

# Step 6: Output the names of the beams that have more than one distributed load assigned under the same load pattern.
print("Beams with more than one distributed load under the same load pattern:")
for beam_name in problematic_beams:
    print(beam_name)