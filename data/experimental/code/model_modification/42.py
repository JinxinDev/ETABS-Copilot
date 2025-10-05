"""
Generated ETABS Script
Description: Create specified load patterns (DEAD, LIVE, WIND_X, WIND_Y) and apply uniform dead and live loads to all floor slabs in the model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-12 09:14:17
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new load pattern named 'DEAD' with load type 'Dead' and a self-weight multiplier of 1.0.
SapModel.LoadPatterns.Add("DEAD", 1, 1.0, True)

# Step 2: Add a new load pattern named 'LIVE' with load type 'Live'.
SapModel.LoadPatterns.Add("LIVE", 3, 0.0, True)

# Step 3: Add a new load pattern named 'WIND_X' with load type 'Wind'.
SapModel.LoadPatterns.Add("WIND_X", 6, 0.0, True)

# Step 4: Add a new load pattern named 'WIND_Y' with load type 'Wind'.
SapModel.LoadPatterns.Add("WIND_Y", 6, 0.0, True)

# Step 5: Retrieve the names of all defined area objects in the model, which represent the floor slabs.
slab_obj_num, all_area_object_names, ret = SapModel.AreaObj.GetNameList()

# Step 6: Apply a uniform load of 0.085 ksf under the 'DEAD' load pattern to all identified floor slabs.
# Step 6: Apply a uniform load of 0.085 ksf under the 'DEAD' load pattern to all identified floor slabs.
load_value_dead = 0.085 # ksf
load_pattern_dead = "DEAD"

for area_obj_name in all_area_object_names:
    ret = SapModel.AreaObj.SetLoadUniform(
        area_obj_name,       # Name: The name of a single area object.
        load_pattern_dead,   # LoadPat: The name of the load pattern to apply the load.
        load_value_dead,     # Value: The magnitude of the uniform load.
        10,                  # Dir: Gravity direction (10 for Gravity when CSys is Global).
        True,                # Replace: If True, this load replaces all other loads of the same pattern.
        "Global",            # CSys: The coordinate system for the load direction.
        0                    # ItemType: 0 for a single Object.
    )

# Step 7: Apply a uniform load of 0.080 ksf under the 'LIVE' load pattern to all identified floor slabs.
# Step 7: Apply a uniform load of 0.080 ksf under the 'LIVE' load pattern to all identified floor slabs.
load_value_live = 0.080 # ksf
load_pattern_live = "LIVE"

for area_obj_name in all_area_object_names:
    ret = SapModel.AreaObj.SetLoadUniform(
        area_obj_name,       # Name: The name of a single area object.
        load_pattern_live,   # LoadPat: The name of the load pattern to apply the load.
        load_value_live,     # Value: The magnitude of the uniform load.
        10,                  # Dir: Gravity direction (10 for Gravity when CSys is Global).
        True,                # Replace: If True, this load replaces all other loads of the same pattern.
        "Global",            # CSys: The coordinate system for the load direction.
        0                    # ItemType: 0 for a single Object.
    )