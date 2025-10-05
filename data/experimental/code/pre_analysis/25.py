"""
Generated ETABS Script
Description: Generate a summary of all concrete materials, showing each material's name and its specified compressive strength.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 17:29:47
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all defined material property names in the model.
num_of_material, material_tuple, ret = SapModel.PropMaterial.GetNameList()

# Step 2: Iterate through the list of material names, and for each material, attempt to retrieve its concrete material properties to identify concrete materials and their specified compressive strength (Fc).
concrete_materials_fc = {}
for material_name in material_tuple:
    # Attempt to retrieve concrete properties for the current material.
    # The GetOConcrete_1 method returns a tuple containing various properties
    # and an API return code as its last element.
    result_tuple = SapModel.PropMaterial.GetOConcrete_1(material_name)
    
    # The last element of the returned tuple indicates the success of the API call.
    # A value of 0 means the call was successful and the material is concrete.
    api_ret_code = result_tuple[-1]
    
    if api_ret_code == 0:
        # If the API call was successful, the material is concrete.
        # The first element of the tuple is the compressive strength (Fc).
        fc = result_tuple[0]
        concrete_materials_fc[material_name] = fc
        print(f"Material '{material_name}' is Concrete with Fc = {fc}")