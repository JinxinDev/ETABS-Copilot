"""
Generated ETABS Script
Description: A sequential plan to retrieve the total slab area for each story in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 10:39:05
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined stories in the model.
num_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: Iterate through each story name. For each story, retrieve the names of all area objects (slabs) defined on that specific story.
story_slabs_map = {}
for story_name in story_names:
    slab_obj_num, slab_ID_tuple, ret = SapModel.AreaObj.GetNameListOnStory(story_name)
    if ret == 0:
        story_slabs_map[story_name] = list(slab_ID_tuple)
    else:
        # In a production script, more robust error handling would be implemented.
        # For now, we'll just print a message.
        print(f"Error retrieving area objects for story '{story_name}'. Return code: {ret}")

# Step 3: For each area object (slab) found on a story, retrieve the names of the point objects that define its perimeter.
slab_points_map = {}
for story_name, slab_names_list in story_slabs_map.items():
    for slab_name in slab_names_list:
        num_points, point_tuple, ret = SapModel.AreaObj.GetPoints(slab_name)
        if ret == 0:
            slab_points_map[slab_name] = list(point_tuple)
        else:
            print(f"Error retrieving points for slab '{slab_name}'. Return code: {ret}")

# Step 4: For each point object name retrieved, get its Cartesian coordinates (X, Y, Z) in the present units.
point_coords_map = {}
processed_points = set()

for slab_name, point_names_list in slab_points_map.items():
    for point_name in point_names_list:
        if point_name not in processed_points:
            X, Y, Z, ret = SapModel.PointObj.GetCoordCartesian(point_name)
            if ret == 0:
                point_coords_map[point_name] = (X, Y, Z)
                processed_points.add(point_name)
            else:
                print(f"Error retrieving coordinates for point '{point_name}'. Return code: {ret}")

# Step 5: Calculate the area of each slab using the retrieved coordinates of its defining points. Sum the areas of all slabs on each story to get the total slab area per story.
def calculate_polygon_area(points):
    """
    Calculates the area of a polygon given a list of (x, y) coordinates using the shoelace formula.
    Points are assumed to be ordered sequentially around the perimeter.
    """
    if len(points) < 3:
        return 0.0 # Not a polygon

    sum1 = 0.0
    sum2 = 0.0
    num_points = len(points)

    for i in range(num_points):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % num_points] # Wrap around for the last point

        sum1 += x1 * y2
        sum2 += y1 * x2

    area = 0.5 * abs(sum1 - sum2)
    return area

slab_areas_map = {}
for slab_name, point_names_list in slab_points_map.items():
    slab_points_coords_xy = []
    for point_name in point_names_list:
        if point_name in point_coords_map:
            X, Y, Z = point_coords_map[point_name]
            slab_points_coords_xy.append((X, Y))
        else:
            print(f"Warning: Coordinates for point '{point_name}' not found for slab '{slab_name}'. Skipping area calculation for this slab.")
            slab_points_coords_xy = [] # Clear points to ensure 0 area if any point is missing
            break
    
    if slab_points_coords_xy:
        slab_area = calculate_polygon_area(slab_points_coords_xy)
        slab_areas_map[slab_name] = slab_area
    else:
        slab_areas_map[slab_name] = 0.0

story_total_slab_area = {}
for story_name, slab_names_list in story_slabs_map.items():
    total_area_for_story = 0.0
    for slab_name in slab_names_list:
        if slab_name in slab_areas_map:
            total_area_for_story += slab_areas_map[slab_name]
        else:
            print(f"Warning: Area for slab '{slab_name}' not found when summing for story '{story_name}'. Assuming 0 area.")
    story_total_slab_area[story_name] = total_area_for_story

# Optional: Print results for verification
# print("\nSlab Areas:")
# for slab, area in slab_areas_map.items():
#     print(f"  Slab '{slab}': {area:.2f} sq ft")

# print("\nTotal Slab Area per Story:")
# for story, total_area in story_total_slab_area.items():
#     print(f"  Story '{story}': {total_area:.2f} sq ft")

# Step 6: Output or store the calculated total slab area for each story.
# Step 6: Output the calculated total slab area for each story.
print("\n--- Total Slab Area per Story ---")
for story_name, total_area in story_total_slab_area.items():
    print(f"Story '{story_name}': {total_area:.2f} sq ft")

# In a more complex script, this data might be written to a CSV, Excel file, or a database.