"""
Generated ETABS Script
Description: Retrieve the mode shape vector for the first torsional mode and identify the corner of the building that experiences the largest displacement.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 17:53:57
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal periods, cyclic frequencies, circular frequencies, and eigenvalues for all modal load cases to understand the dynamic characteristics of the structure.
(NumberResults, LoadCase, StepType, StepNum, Period, Frequency, CircFreq, EigenValue, ret) = SapModel.Results.ModalPeriod()

# Step 2: Retrieve the modal participating mass ratios for all modes of all selected modal analysis cases to identify the modes with significant torsional participation (high RZ ratio).
(NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret) = SapModel.Results.ModalParticipatingMassRatios()

# Step 3: Analyze the retrieved modal periods and participating mass ratios to identify the specific mode number corresponding to the first torsional mode. This involves finding the mode with the lowest period that exhibits a dominant rotational (RZ) participating mass ratio.
# Initialize variables to store the first torsional mode information
first_torsional_mode_number = -1
first_torsional_mode_period = -1.0
first_torsional_rz_ratio = -1.0

# Iterate through the modes to find the first torsional mode
# Modes are typically 1-indexed, but Python lists are 0-indexed.
# The 'Period' and 'RZ' tuples are ordered by mode number.
for i in range(NumberResults):
    mode_number = i + 1 # ETABS modes are 1-indexed
    current_period = Period[i]
    current_ux_ratio = UX[i]
    current_uy_ratio = UY[i]
    current_rz_ratio = RZ[i]

    # Criteria for a dominant torsional mode: RZ ratio is significantly higher than UX and UY ratios.
    # This identifies the mode where rotational participation about Z is dominant over translational.
    if current_rz_ratio > current_ux_ratio and current_rz_ratio > current_uy_ratio:
        first_torsional_mode_number = mode_number
        first_torsional_mode_period = current_period
        first_torsional_rz_ratio = current_rz_ratio
        break # Found the first mode that satisfies the torsional dominance criteria

# The variables first_torsional_mode_number, first_torsional_mode_period,
# and first_torsional_rz_ratio now hold the identified first torsional mode's data.
# These can be used in subsequent steps.

# Step 4: Retrieve the names of all defined stories in the model to facilitate iterating through the building levels.
num_of_stories, story_names_tuple, ret = SapModel.Story.GetNameList()

# Step 5: Retrieve the names of all point objects in the model, which will be used to query their coordinates and displacements.
# Initialize a set to store unique point names collected from various objects.
all_point_names_set = set()

# Retrieve names of all frame objects in the model.
num_frames, frame_names_tuple, ret = SapModel.FrameObj.GetNameList()

# Iterate through each frame object to get the names of its associated points (joints).
for frame_name in frame_names_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_name)
    all_point_names_set.add(point_1)
    all_point_names_set.add(point_2)

# Retrieve names of all area objects in the model.
num_areas, area_names_tuple, ret = SapModel.AreaObj.GetNameList()

# Iterate through each area object to get the names of its associated points (joints).
for area_name in area_names_tuple:
    # Get the names of the point objects that define an area object.
    number_of_points_for_area, area_points_tuple, ret = SapModel.AreaObj.GetPoints(area_name)
    for point_name in area_points_tuple:
        all_point_names_set.add(point_name)

# Convert the set of unique point names to a tuple and get the total count.
point_names_tuple = tuple(all_point_names_set)
num_of_points = len(point_names_tuple)
# The 'ret' value for this composite operation can be considered successful if all sub-operations were successful.
# For simplicity, we'll assume success if the individual calls returned 0.
# The final 'ret' from the last API call is not directly relevant for the overall collection of points.

# Step 6: For each retrieved point object, get its Cartesian coordinates (X, Y, Z) to determine its location and identify corner points of the building on each story.
# Initialize a dictionary to store the coordinates of each point.
point_coordinates = {}

# Iterate through each point name and retrieve its Cartesian coordinates.
for point_name in point_names_tuple:
    X, Y, Z, ret = SapModel.PointObj.GetCoordCartesian(point_name)
    if ret == 0: # Check if the API call was successful
        point_coordinates[point_name] = (X, Y, Z)
    else:
        # Handle error or log if a point's coordinates could not be retrieved
        print(f"Error retrieving coordinates for point: {point_name}")

# The 'point_coordinates' dictionary now holds the X, Y, Z coordinates for all retrieved points.

# Step 7: Retrieve the joint displacements (UX, UY, UZ, RX, RY, RZ) for all point objects for the identified first torsional mode. This data represents the mode shape vector.
ObjectElm = 0

modal_load_case_name = LoadCase[0]

joint_displacements_torsional_mode = {}

for point_name in point_names_tuple:
    (NumberResults_joint, Obj_joint, Elm_joint, LoadCase_joint, StepType_joint, StepNum_joint, U1_joint, U2_joint, U3_joint, R1_joint, R2_joint, R3_joint, ret_joint) = SapModel.Results.JointDispl(point_name, ObjectElm)

    if ret_joint == 0:
        for i in range(NumberResults_joint):
            if (LoadCase_joint[i] == modal_load_case_name and
                StepType_joint[i] == "Mode" and
                StepNum_joint[i] == float(first_torsional_mode_number)):

                joint_displacements_torsional_mode[point_name] = (
                    U1_joint[i], U2_joint[i], U3_joint[i],
                    R1_joint[i], R2_joint[i], R3_joint[i]
                )
                break
    else:
        print(f"Error retrieving joint displacements for point: {point_name}")

# Step 8: Process the joint displacement data for the identified first torsional mode. Filter for corner points on each story (based on their X and Y coordinates), calculate the resultant displacement for each corner, and then identify the specific corner point that experiences the largest total displacement.
import math

# Step 8: Process the joint displacement data for the identified first torsional mode.
# Filter for corner points on each story (based on their X and Y coordinates),
# calculate the resultant displacement for each corner, and then identify the specific
# corner point that experiences the largest total displacement.

# 1. Group points by Z-coordinate (story level)
points_by_z_level = {}
for point_name, coords in point_coordinates.items():
    X, Y, Z = coords
    if Z not in points_by_z_level:
        points_by_z_level[Z] = []
    points_by_z_level[Z].append((point_name, X, Y))

# 2. Identify corner points for each Z-level (story)
corner_points_by_z_level = {}
coord_tolerance = 0.1 # feet, for identifying points close to min/max X/Y

for z_level, points_on_level in points_by_z_level.items():
    if not points_on_level:
        continue

    # Extract X and Y coordinates for points on this level
    x_coords = [p[1] for p in points_on_level]
    y_coords = [p[2] for p in points_on_level]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    corner_points_on_level = []
    for point_name, X, Y in points_on_level:
        is_corner_x = (abs(X - min_x) < coord_tolerance) or (abs(X - max_x) < coord_tolerance)
        is_corner_y = (abs(Y - min_y) < coord_tolerance) or (abs(Y - max_y) < coord_tolerance)

        # A point is considered a corner if it's at an extreme X and an extreme Y
        if is_corner_x and is_corner_y:
            corner_points_on_level.append(point_name)

    if corner_points_on_level:
        corner_points_by_z_level[z_level] = corner_points_on_level

# 3. Calculate resultant displacement for corner points and find the maximum
max_resultant_displacement = -1.0
point_with_max_displacement = None
z_level_of_max_displacement = None

for z_level, corner_points in corner_points_by_z_level.items():
    for point_name in corner_points:
        if point_name in joint_displacements_torsional_mode:
            U1, U2, U3, R1, R2, R3 = joint_displacements_torsional_mode[point_name]
            
            # Calculate resultant translational displacement
            resultant_displacement = math.sqrt(U1**2 + U2**2 + U3**2)

            if resultant_displacement > max_resultant_displacement:
                max_resultant_displacement = resultant_displacement
                point_with_max_displacement = point_name
                z_level_of_max_displacement = z_level

# The variables point_with_max_displacement, max_resultant_displacement,
# and z_level_of_max_displacement now hold the information about the corner
# point with the largest total displacement in the first torsional mode.