"""
Generated ETABS Script
Description: Define a new user-defined concrete material named 'C6000' with a specified compressive strength.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 19:31:26
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Initialize a new user-defined material property named 'C6000' with the material type set to 'Concrete'.
material_name_to_add = "C6000"
material_type_concrete = 2  # 2 corresponds to Concrete
region_placeholder = "Other" # Placeholder for user-defined material
standard_placeholder = "User Defined" # Placeholder for user-defined material
grade_placeholder = "User Defined" # Placeholder for user-defined material

# Add the new user-defined concrete material property
# The AddMaterial method returns the actual material name created and a return code.
created_material_name, ret_code = SapModel.PropMaterial.AddMaterial(material_name_to_add, material_type_concrete, region_placeholder, standard_placeholder, grade_placeholder)

# Step 2: Set the user-defined concrete material properties for 'C6000', specifically setting the compressive strength (f'c) to 6000 psi, which is equivalent to 864 ksf.
ret_code = SapModel.PropMaterial.SetOConcrete_1(created_material_name, 864, False, 0, 1, 2, 0.0022, 0.0052, -0.1, 0, 0)
print(ret_code)