"""
Generated ETABS Script
Description: Create a new concrete material with specified properties and then define three rectangular concrete frame sections using this material.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 17:15:21
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Create a new concrete material named 'CONC6000' with a compressive strength of 6000 psi, an elastic modulus of 57000 ksi, and a unit weight of 0.15 kcf.
# Create a new concrete material named 'CONC6000'
# MatType for Concrete is 2 (as per example in knowledge graph)
ret_code = SapModel.PropMaterial.SetMaterial("CONC6000", 2)

# Set concrete properties for 'CONC6000'
# Compressive strength (fc): 6000 psi = 6.0 ksi (consistent with kip_ft_F units where fc is typically in ksi)
# Other parameters are set to default values as observed in the SetOConcrete_1 example
# Parameters: Name, fc, IsLightweight, fcsFactor, SSType, SSHysType, StrainAtfc, StrainUltimate, FinalSlope, FrictionAngle, DilatationalAngle
ret_code = SapModel.PropMaterial.SetOConcrete_1("CONC6000", 6.0, False, 0, 1, 2, 0.0022, 0.0052, -0.1, 0.0, 0.0)

# Step 2: Create a new rectangular concrete frame section named 'COL24x24' with dimensions 24 inches by 24 inches, using the 'CONC6000' material.
# Create a new rectangular concrete frame section named 'COL24x24'
# Dimensions are 24 inches by 24 inches, which need to be converted to feet for the kip_ft_F unit system.
section_name = "COL24x24"
material_name = "CONC6000"
depth_ft = 24.0 / 12.0  # 24 inches = 2 feet
width_ft = 24.0 / 12.0   # 24 inches = 2 feet

# Call SetRectangle using positional arguments
# Parameters: Name, MatProp, T3 (depth), T2 (width)
ret_code = SapModel.PropFrame.SetRectangle(section_name, material_name, depth_ft, width_ft)

# Step 3: Create a new rectangular concrete frame section named 'BEAM16x30' with dimensions 16 inches by 30 inches, using the 'CONC6000' material.
# Step 3: Create a new rectangular concrete frame section named 'BEAM16x30' with dimensions 16 inches by 30 inches, using the 'CONC6000' material.
# Dimensions are 16 inches by 30 inches, which need to be converted to feet for the kip_ft_F unit system.
section_name_beam = "BEAM16x30"
material_name_beam = "CONC6000"
depth_beam_ft = 30.0 / 12.0  # 30 inches = 2.5 feet (T3 parameter)
width_beam_ft = 16.0 / 12.0   # 16 inches = 1.333... feet (T2 parameter)

# Call SetRectangle using positional arguments
# Parameters: Name, MatProp, T3 (depth), T2 (width)
ret_code = SapModel.PropFrame.SetRectangle(section_name_beam, material_name_beam, depth_beam_ft, width_beam_ft)

# Step 4: Create a new rectangular concrete frame section named 'BEAM14x24' with dimensions 14 inches by 24 inches, using the 'CONC6000' material.
# Step 4: Create a new rectangular concrete frame section named 'BEAM14x24' with dimensions 14 inches by 24 inches, using the 'CONC6000' material.
# Dimensions are 14 inches by 24 inches, which need to be converted to feet for the kip_ft_F unit system.
section_name_beam_2 = "BEAM14x24"
material_name_beam_2 = "CONC6000"
depth_beam_2_ft = 24.0 / 12.0  # 24 inches = 2 feet (T3 parameter)
width_beam_2_ft = 14.0 / 12.0   # 14 inches = 1.166... feet (T2 parameter)

# Call SetRectangle using positional arguments
# Parameters: Name, MatProp, T3 (depth), T2 (width)
ret_code = SapModel.PropFrame.SetRectangle(section_name_beam_2, material_name_beam_2, depth_beam_2_ft, width_beam_2_ft)