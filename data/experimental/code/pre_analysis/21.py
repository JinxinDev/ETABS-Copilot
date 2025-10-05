"""
Generated ETABS Script
Description: Identify all slab panels in the ETABS model that have an aspect ratio (longer side / shorter side) greater than 2.0.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 16:50:54
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all area objects defined in the ETABS model.
area_obj_count, area_obj_names, ret = SapModel.AreaObj.GetNameList()

# Step 2: For each area object, retrieve the name of the area property assigned to it.
area_properties = {}
for area_name in area_obj_names:
    prop_name, ret = SapModel.AreaObj.GetProperty(area_name)
    area_properties[area_name] = prop_name

# Step 3: For each area property name, verify if it is a slab section property. This step implicitly filters out non-slab area objects.
slab_section_properties = {}
for area_name, prop_name in area_properties.items():
    # Attempt to retrieve slab property data. If successful, it's a slab section.
    SlabType, ShellType, MatProp, Thickness, color, notes, GUID, ret = SapModel.PropArea.GetSlab(prop_name)
    if ret == 0: # A return value of 0 indicates success, meaning it is a slab section.
        slab_section_properties[prop_name] = SlabType

# Step 4: For each identified slab panel, retrieve the names of the point objects that define its geometry.
slab_panel_points = {}
for area_name in area_obj_names:
    prop_name = area_properties[area_name]
    if prop_name in slab_section_properties:
        # This area object is a slab panel, retrieve its defining points.
        number_of_points, point_tuple, ret = SapModel.AreaObj.GetPoints(area_name)
        if ret == 0:
            slab_panel_points[area_name] = point_tuple

# Step 5: For each defining point object name, retrieve its X, Y, and Z Cartesian coordinates.
point_coordinates = {}
for area_name, point_tuple in slab_panel_points.items():
    for point_name in point_tuple:
        if point_name not in point_coordinates:
            X, Y, Z, ret = SapModel.PointObj.GetCoordCartesian(point_name)
            if ret == 0:
                point_coordinates[point_name] = (X, Y, Z)

# Step 6: Calculate the dimensions (lengths of sides) of each slab panel using its defining point coordinates, and then compute its aspect ratio (longer side / shorter side).
import math

slab_dimensions_aspect_ratios = {}

for area_name, point_names_tuple in slab_panel_points.items():
    side_lengths = []
    num_points = len(point_names_tuple)

    if num_points < 2:
        slab_dimensions_aspect_ratios[area_name] = (0.0, 0.0, 0.0)
        continue

    for i in range(num_points):
        p1_name = point_names_tuple[i]
        p2_name = point_names_tuple[(i + 1) % num_points]

        p1_coords = point_coordinates.get(p1_name)
        p2_coords = point_coordinates.get(p2_name)

        if p1_coords and p2_coords:
            x1, y1, z1 = p1_coords
            x2, y2, z2 = p2_coords
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            side_lengths.append(distance)
        else:
            pass
    
    if side_lengths:
        max_length = max(side_lengths)
        min_length = min(side_lengths)
        
        aspect_ratio = 0.0
        if min_length > 0:
            aspect_ratio = max_length / min_length
        
        slab_dimensions_aspect_ratios[area_name] = (max_length, min_length, aspect_ratio)
    else:
        slab_dimensions_aspect_ratios[area_name] = (0.0, 0.0, 0.0)

# Step 7: Filter the slab panels, keeping only those where the calculated aspect ratio is greater than 2.0.
filtered_slab_panels_by_aspect_ratio = {}
for area_name, dimensions_aspect_ratio in slab_dimensions_aspect_ratios.items():
    max_length, min_length, aspect_ratio = dimensions_aspect_ratio
    if aspect_ratio > 2.0:
        filtered_slab_panels_by_aspect_ratio[area_name] = dimensions_aspect_ratio

# Step 8: Report the names of all slab panels that meet the criteria (aspect ratio greater than 2.0).
print("Slab panels with aspect ratio greater than 2.0:")
for area_name in filtered_slab_panels_by_aspect_ratio.keys():
    print(area_name)