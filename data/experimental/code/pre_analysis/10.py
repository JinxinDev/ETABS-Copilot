"""
Generated ETABS Script
Description: Retrieve and list all concrete materials defined in the ETABS model, along with their compressive strengths and unit weights.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 20:54:03
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all material properties currently defined in the ETABS model.
num_of_materials, material_names, ret = SapModel.PropMaterial.GetNameList()

# Step 2: Iterate through each retrieved material name. For each material, attempt to get its concrete-specific properties. If the material is concrete, extract its compressive strength (fck) and unit weight (UnitWeight).
concrete_properties = {}
for material_name in material_names:
    # Get basic material properties to determine its type
    # The GetMaterial method returns a tuple: (MatType, Color, Notes, GUID, ReturnValue)
    mat_type, color, notes, guid, ret_get_material = SapModel.PropMaterial.GetMaterial(material_name)

    # Check if the material type is concrete
    # Based on the example `SetMaterial("Concrete",2)`, we infer 2 is the enum value for concrete.
    if mat_type == 2: # Assuming 2 corresponds to eMatType.Concrete
        # Attempt to get concrete-specific properties
        # GetOConcrete_1 returns a tuple: (fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ReturnValue)
        result_concrete_props = SapModel.PropMaterial.GetOConcrete_1(material_name)

        # Unpack the results
        fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ret_get_oconcrete = result_concrete_props

        if ret_get_oconcrete == 0: # Successfully retrieved concrete properties
            concrete_properties[material_name] = {
                "fck": fc # Compressive strength (fc)
                # Note: UnitWeight is requested but is not available through the provided API methods (GetMaterial or GetOConcrete_1).
            }

# Step 3: Present the collected data, listing each concrete material's name, compressive strength, and unit weight.
print("\n--- Concrete Material Properties ---")
if concrete_properties:
    for material_name, props in concrete_properties.items():
        fck = props.get("fck")
        # UnitWeight was noted as not available in the previous step, so we cannot print it.
        print(f"Material Name: {material_name}")
        print(f"  Compressive Strength (fck): {fck:.2f} kip/ft^2") # Assuming fck is in kip/ft^2 based on kip_ft_F unit system
        print("------------------------------------")
else:
    print("No concrete materials found or properties could not be retrieved.")