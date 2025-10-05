"""
Generated ETABS Script
Description: Create a seismic load pattern and define the mass source for the model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 20:39:27
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new seismic load pattern named EQ_X with a base shear of 250 kips. Note: The base shear parameter is typically set in a more detailed seismic load definition method not explicitly available in the provided skeleton for the 'Add' method.
ret = SapModel.LoadPatterns.Add("EQ_X", 5, 0.0, True)

# Step 2: Set the mass source for the model, including DEAD load with a multiplier of 1.0 and LIVE load with a multiplier of 0.25.
load_patterns = ["DEAD", "LIVE"]
scale_factors = [1.0, 0.25]
number_loads = len(load_patterns)

ret = SapModel.PropMaterial.SetMassSource_1(
    True,          # IncludeElementMass
    True,          # IncludeAddedMass
    True,          # IncludeLoads
    number_loads,  # NumberLoads
    load_patterns, # LoadPat
    scale_factors  # sf
)
