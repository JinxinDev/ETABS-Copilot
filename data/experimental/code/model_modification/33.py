"""
Generated ETABS Script
Description: Create a comprehensive material set including 4000 psi concrete, Grade 60 rebar, and A992 steel, then verify their addition to the model library.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-13 17:06:08
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add 4000 psi concrete material to the model library from the ETABS standard material library. The material will be from the 'United States' region, 'Customary' standard, and 'f'c 4000 psi' grade.
material_name_concrete_4000 = "CONC_4000_PSI"
mat_type_concrete = 2 # 2 = Concrete
region = "United States"
standard = "Customary"
grade = "f'c 4000 psi"

# Add 4000 psi concrete material to the model library
material_name_added, ret_code = SapModel.PropMaterial.AddMaterial(
    material_name_concrete_4000,
    mat_type_concrete,
    region,
    standard,
    grade
)

if ret_code == 0:
    print(f"Successfully added concrete material: {material_name_added}")
else:
    print(f"Error adding concrete material '{material_name_concrete_4000}'. Return code: {ret_code}")

# Step 2: Add Grade 60 rebar material to the model library from the ETABS standard material library. The material will be from the 'United States' region, 'ASTM A615' standard, and 'Grade 60' grade.
# Step 2: Add Grade 60 rebar material to the model library
material_name_rebar_60 = "REBAR_GRADE_60"
mat_type_rebar = 6 # 6 = Rebar
region_rebar = "United States"
standard_rebar = "ASTM A615"
grade_rebar = "Grade 60"

# Add Grade 60 rebar material to the model library
material_name_added_rebar, ret_code_rebar = SapModel.PropMaterial.AddMaterial(
    material_name_rebar_60,
    mat_type_rebar,
    region_rebar,
    standard_rebar,
    grade_rebar
)

if ret_code_rebar == 0:
    print(f"Successfully added rebar material: {material_name_added_rebar}")
else:
    print(f"Error adding rebar material '{material_name_rebar_60}'. Return code: {ret_code_rebar}")

# Step 3: Add A992 steel material to the model library from the ETABS standard material library. The material will be from the 'United States' region, 'ASTM A992' standard, and 'Grade 50' grade.
# Step 3: Add A992 steel material to the model library from the ETABS standard material library.
material_name_steel_A992 = "STEEL_A992_GR50"
mat_type_steel = 1 # 1 = Steel
region_steel = "United States"
standard_steel = "ASTM A992"
grade_steel = "Grade 50"

# Add A992 steel material to the model library
material_name_added_steel, ret_code_steel = SapModel.PropMaterial.AddMaterial(
    material_name_steel_A992,
    mat_type_steel,
    region_steel,
    standard_steel,
    grade_steel
)

if ret_code_steel == 0:
    print(f"Successfully added steel material: {material_name_added_steel}")
else:
    print(f"Error adding steel material '{material_name_steel_A992}'. Return code: {ret_code_steel}")

# Step 4: Retrieve the names of all defined material properties currently in the model library.
# Step 4: Retrieve the names of all defined material properties currently in the model library.
num_materials, material_names_tuple, ret_code_get_names = SapModel.PropMaterial.GetNameList()

if ret_code_get_names == 0:
    print(f"Successfully retrieved {num_materials} material names.")
    print("Defined Materials:")
    for name in material_names_tuple:
        print(f"- {name}")
else:
    print(f"Error retrieving material names. Return code: {ret_code_get_names}")

# Step 5: Verify that 'f'c 4000 psi' concrete, 'Grade 60' rebar, and 'A992 Grade 50' steel materials are present in the retrieved list of material names.
# Step 5: Verify that 'f'c 4000 psi' concrete, 'Grade 60' rebar, and 'A992 Grade 50' steel materials are present.

# Convert the tuple to a list for easier checking if needed, though 'in' works directly on tuples.
material_names_list = list(material_names_tuple)

# Check for concrete material
if material_name_added in material_names_list:
    print(f"Verification successful: Concrete material '{material_name_concrete_4000}' is present.")
else:
    print(f"Verification failed: Concrete material '{material_name_concrete_4000}' is NOT present.")

# Check for rebar material
if material_name_added_rebar in material_names_list:
    print(f"Verification successful: Rebar material '{material_name_rebar_60}' is present.")
else:
    print(f"Verification failed: Rebar material '{material_name_rebar_60}' is NOT present.")

# Check for steel material
if material_name_added_steel in material_names_list:
    print(f"Verification successful: Steel material '{material_name_steel_A992}' is present.")
else:
    print(f"Verification failed: Steel material '{material_name_steel_A992}' is NOT present.")