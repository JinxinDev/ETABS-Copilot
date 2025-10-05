"""
Generated ETABS Script
Description: Create rectangular floor slabs at Story 2 with specified dimensions and coordinates, assign an 8-inch thick slab property, and apply a 50 psf live load.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 20:02:44
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the Z-coordinate (elevation) of 'Story 2' to correctly place the area objects.
story_name_to_retrieve = 'Story2'
story2_elevation, ret = SapModel.Story.GetElevation(story_name_to_retrieve)

# Step 2: Add a concrete material property named 'CONC4000' with a grade of 'f'c 4000 psi' from the 'United States' 'Customary' standard.
# Define parameters for the concrete material
material_name = "CONC4000"
mat_type_concrete = 2  # Concrete material type
region_name = "United States"
standard_name = "Customary"
grade_name = "f'c 4000 psi"

# Add the concrete material property with the specified name and properties.
# The AddMaterial function returns the name of the material it created
# (which should be 'CONC4000' if successfully added) and a return code.
material_name_created, ret = SapModel.PropMaterial.AddMaterial(
    MatType=mat_type_concrete,
    Region=region_name,
    Standard=standard_name,
    Grade=grade_name
)

# Step 3: Define a new slab area property named 'SLAB8INCH' with a thickness of 8 inches (0.6667 ft) and assign the 'CONC4000' concrete material.
# Define parameters for the slab area property
slab_prop_name = "SLAB8INCH"
slab_type_slab = 0  # ESLABTYPE_SLAB
shell_type_thin = 1 # ESHELLTYPE_SHELLTHIN
slab_material = "CONC4000" # Material defined in the previous step
slab_thickness = 8 / 12 # 8 inches converted to feet

# Add the slab area property
ret = SapModel.PropArea.SetSlab(slab_prop_name, slab_type_slab, shell_type_thin, slab_material, slab_thickness)

# Step 4: Add a new load pattern named 'LIVE' with a load type of 'Live' and a self-weight multiplier of 0.
# Add a new load pattern named 'LIVE' with a load type of 'Live' and a self-weight multiplier of 0.
# The 'Add' method also creates a corresponding analysis case if the last argument is True.
load_pattern_name = "LIVE"
load_type_live = 3 # Corresponds to 'Live' load type
self_weight_multiplier = 0.0
add_analysis_case = True

ret = SapModel.LoadPatterns.Add(load_pattern_name, load_type_live, self_weight_multiplier, add_analysis_case)

# Step 5: Create six rectangular area objects (slabs) at the Z-elevation of 'Story 2'. The first three slabs are: (0,0) to (30,40) using coordinates (0,0,Z), (30,0,Z), (30,40,Z), (0,40,Z); (30,0) to (60,40) using coordinates (30,0,Z), (60,0,Z), (60,40,Z), (30,40,Z); and (60,0) to (90,40) using coordinates (60,0,Z), (90,0,Z), (90,40,Z), (60,40,Z).
# Define the number of points for a rectangular area object
num_points = 4

# Z-coordinate for all slabs (from Step 1)
z_coord_list = [story2_elevation] * num_points

# List to store the names of the created area objects
created_area_names = []

# Slab 1: (0,0) to (30,40)
x_coords_slab1 = [0.0, 30.0, 30.0, 0.0]
y_coords_slab1 = [0.0, 0.0, 40.0, 40.0]
_, _, _, area_name_slab1, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab1, y_coords_slab1, z_coord_list)
created_area_names.append(area_name_slab1)

# Slab 2: (30,0) to (60,40)
x_coords_slab2 = [30.0, 60.0, 60.0, 30.0]
y_coords_slab2 = [0.0, 0.0, 40.0, 40.0]
_, _, _, area_name_slab2, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab2, y_coords_slab2, z_coord_list)
created_area_names.append(area_name_slab2)

# Slab 3: (60,0) to (90,40)
x_coords_slab3 = [60.0, 90.0, 90.0, 60.0]
y_coords_slab3 = [0.0, 0.0, 40.0, 40.0]
_, _, _, area_name_slab3, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab3, y_coords_slab3, z_coord_list)
created_area_names.append(area_name_slab3)

# Slab 4: (0,40) to (30,80) - Based on pattern for six slabs
x_coords_slab4 = [0.0, 30.0, 30.0, 0.0]
y_coords_slab4 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab4, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab4, y_coords_slab4, z_coord_list)
created_area_names.append(area_name_slab4)

# Slab 5: (30,40) to (60,80) - Based on pattern for six slabs
x_coords_slab5 = [30.0, 60.0, 60.0, 30.0]
y_coords_slab5 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab5, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab5, y_coords_slab5, z_coord_list)
created_area_names.append(area_name_slab5)

# Slab 6: (60,40) to (90,80) - Based on pattern for six slabs
x_coords_slab6 = [60.0, 90.0, 90.0, 60.0]
y_coords_slab6 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab6, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab6, y_coords_slab6, z_coord_list)
created_area_names.append(area_name_slab6)

# Note: The provided knowledge does not include a method to assign a slab property
# to an area object after creation using AddByCoord. 
# Therefore, these area objects are created geometrically, but the 'SLAB8INCH'
# property is not assigned in this step based on the available API methods.
# The 'created_area_names' list holds the names of the newly created area objects.

# Step 6: Create the remaining three rectangular area objects (slabs) at the Z-elevation of 'Story 2'. These slabs are: (0,40) to (30,80) using coordinates (0,40,Z), (30,40,Z), (30,80,Z), (0,80,Z); (30,40) to (60,80) using coordinates (30,40,Z), (60,40,Z), (60,80,Z), (30,80,Z); and (60,40) to (90,80) using coordinates (60,40,Z), (90,40,Z), (90,80,Z), (60,80,Z).
# Create the first of the remaining three slabs: (0,40) to (30,80)
x_coords_slab_curr1 = [0.0, 30.0, 30.0, 0.0]
y_coords_slab_curr1 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab_curr1, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab_curr1, y_coords_slab_curr1, z_coord_list)
created_area_names.append(area_name_slab_curr1)

# Create the second of the remaining three slabs: (30,40) to (60,80)
x_coords_slab_curr2 = [30.0, 60.0, 60.0, 30.0]
y_coords_slab_curr2 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab_curr2, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab_curr2, y_coords_slab_curr2, z_coord_list)
created_area_names.append(area_name_slab_curr2)

# Create the third of the remaining three slabs: (60,40) to (90,80)
x_coords_slab_curr3 = [60.0, 90.0, 90.0, 60.0]
y_coords_slab_curr3 = [40.0, 40.0, 80.0, 80.0]
_, _, _, area_name_slab_curr3, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords_slab_curr3, y_coords_slab_curr3, z_coord_list)
created_area_names.append(area_name_slab_curr3)

# Step 7: Retrieve the names of all area objects on 'Story 2' and assign the 'SLAB8INCH' property to them.
# Retrieve the names of all area objects on 'Story 2'
# story_name_to_retrieve is 'Story 2' from Step 1
num_area_objects_on_story2, area_names_on_story2, ret = SapModel.AreaObj.GetNameListOnStory(story_name_to_retrieve)

# Assign the 'SLAB8INCH' property to each retrieved area object
# slab_prop_name is 'SLAB8INCH' from Step 3
for area_name in area_names_on_story2:
    ret = SapModel.AreaObj.SetProperty(area_name, slab_prop_name)

# Step 8: Retrieve the names of all area objects on 'Story 2' and apply a uniform live load of 0.05 ksf (50 psf) in the gravity direction using the 'LIVE' load pattern.
# Retrieve the names of all area objects on 'Story 2' (already done in Step 7)
# num_area_objects_on_story2, area_names_on_story2, ret = SapModel.AreaObj.GetNameListOnStory(story_name_to_retrieve)

# Define parameters for the uniform live load
load_value_live = 0.05 # 0.05 ksf (50 psf) in kip_ft_F units
load_direction = 10 # Gravity direction
replace_existing_loads = True # Replace existing loads of the same pattern
coordinate_system = "Global"
item_type_object = 0 # Apply to a single object

# Apply the uniform live load to each area object on 'Story 2'
# load_pattern_name is 'LIVE' from Step 4
for area_name in area_names_on_story2:
    ret = SapModel.AreaObj.SetLoadUniform(
        area_name,
        load_pattern_name,
        load_value_live,
        load_direction,
        replace_existing_loads,
        coordinate_system,
        item_type_object
    )