"""
Generated ETABS Script
Description: Retrieve the Cartesian coordinates for all points that define all slab area objects in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 09:54:51
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined area objects in the model. These objects represent the slabs.
area_obj_count, area_obj_names, ret = SapModel.AreaObj.GetNameList()

# Step 2: For each retrieved slab (area object) name, get the names of the point objects that define its geometry.
# Initialize a dictionary to store point names for each area object
area_points_map = {}

# Iterate through each area object name (slab)
for area_name in area_obj_names:
    # Get the names of the point objects that define the current area object
    number_of_points, point_tuple, ret = SapModel.AreaObj.GetPoints(area_name)
    # Store the point names in the dictionary, keyed by the area object name
    area_points_map[area_name] = point_tuple

# Step 3: For each point object name obtained from the slabs, retrieve its Cartesian X, Y, and Z coordinates.
point_coordinates = {}
for area_name, point_tuple in area_points_map.items():
    for point_name in point_tuple:
        # Check if coordinates for this point have already been retrieved
        if point_name not in point_coordinates:
            # Retrieve the Cartesian coordinates (X, Y, Z) for the point object
            X, Y, Z, ret = SapModel.PointObj.GetCoordCartesian(point_name)
            # Store the coordinates in the dictionary, keyed by the point name
            point_coordinates[point_name] = (X, Y, Z)
print(point_coordinates)