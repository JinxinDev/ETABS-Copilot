"""
Generated ETABS Script
Description: Retrieve all slab elements in the ETABS model that have a thickness greater than 5 inches.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 17:27:10
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all area object names defined in the model.
area_obj_count, area_obj_names, ret = SapModel.AreaObj.GetNameList()

# Step 2: For each retrieved area object name, get the name of the area property assigned to it.
area_obj_properties = {}
for area_obj_name in area_obj_names:
    prop_name, ret = SapModel.AreaObj.GetProperty(area_obj_name)
    area_obj_properties[area_obj_name] = prop_name

# Step 3: For each area property name, retrieve its slab property data, specifically its thickness, to determine if it is a slab and its dimensions.
unique_area_prop_names = set(area_obj_properties.values())
slab_properties_data = {}
for prop_name in unique_area_prop_names:
    SlabType, ShellType, MatProp, Thickness, color, notes, GUID, ret = SapModel.PropArea.GetSlab(prop_name)
    slab_properties_data[prop_name] = {
        "SlabType": SlabType,
        "ShellType": ShellType,
        "MatProp": MatProp,
        "Thickness": Thickness
    }

# Step 4: Filter the collected slab elements and identify those whose thickness is greater than 5 inches.
thick_slabs = {}
FIVE_INCHES_IN_FEET = 5 / 12.0
for prop_name, data in slab_properties_data.items():
    print(data)
    if data["Thickness"] > FIVE_INCHES_IN_FEET:
        thick_slabs[prop_name] = data
