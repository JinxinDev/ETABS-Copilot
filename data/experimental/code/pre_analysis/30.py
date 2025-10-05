"""
Generated ETABS Script
Description: Increase the thickness of all existing slab sections in the model by 1 inch.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 18:39:42
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined area properties in the model to identify all slab sections.
number_of_area_props, all_area_prop_names, ret = SapModel.PropArea.GetNameList()
slab_section_names = []
for prop_name in all_area_prop_names:
    r_slab_type, r_shell_type, r_mat_prop, r_thickness, r_color, r_notes, r_guid, return_code_get_slab = SapModel.PropArea.GetSlab(prop_name)
    if return_code_get_slab == 0:
        slab_section_names.append(prop_name)

# Step 2: For each retrieved area property, check if it is a slab section. If it is a slab, retrieve its current thickness. Calculate the new thickness by adding 1 inch to the current thickness.
slab_thickness_data = []
for prop_name in slab_section_names:
    r_slab_type, r_shell_type, r_mat_prop, current_thickness, r_color, r_notes, r_guid, return_code_get_slab = SapModel.PropArea.GetSlab(prop_name)
    if return_code_get_slab == 0:
        # Add 1 inch to the current thickness. Convert 1 inch to feet (1/12 ft).
        new_thickness = current_thickness + (1.0 / 12.0)
        slab_thickness_data.append({
            "name": prop_name,
            "current_thickness_ft": current_thickness,
            "new_thickness_ft": new_thickness
        })

# Step 3: Update each identified slab section with its new, increased thickness. The new thickness will be the original thickness plus 1 inch.
for slab_data in slab_thickness_data:
    prop_name = slab_data["name"]
    new_thickness = slab_data["new_thickness_ft"]

    # Retrieve existing properties to pass to SetSlab, as only thickness is changing
    r_slab_type, r_shell_type, r_mat_prop, current_thickness, r_color, r_notes, r_guid, return_code_get_slab = SapModel.PropArea.GetSlab(prop_name)

    if return_code_get_slab == 0:
        # Update the slab property with the new thickness
        return_code_set_slab = SapModel.PropArea.SetSlab(prop_name, r_slab_type, r_shell_type, r_mat_prop, new_thickness)
        if return_code_set_slab != 0:
            print(f"Error updating slab {prop_name} thickness. Return code: {return_code_set_slab}")