"""
Generated ETABS Script
Description: Determine if the second mode of vibration is predominantly translational or torsional by comparing the sum of UX and UY participation to the RZ participation.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 17:49:54
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal participating mass ratios for all modes from the ETABS model. This will provide the UX, UY, and RZ participation ratios for each mode.
(NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret) = SapModel.Results.ModalParticipatingMassRatios()

# Step 2: Extract the UX, UY, and RZ participation ratios specifically for the second mode of vibration from the retrieved data.
ux_mode2 = UX[1]
uy_mode2 = UY[1]
rz_mode2 = RZ[1]

# Step 3: Calculate the sum of the UX and UY participation ratios for the second mode.
sum_ux_uy_mode2 = ux_mode2 + uy_mode2

# Step 4: Compare the sum of UX and UY participation ratios with the RZ participation ratio for the second mode to determine if it is predominantly translational or torsional. If (UX + UY) > RZ, it is translational; otherwise, it is torsional.
if sum_ux_uy_mode2 > rz_mode2:
    mode2_type = "translational"
else:
    mode2_type = "torsional"
print(f"The second mode of vibration is predominantly {mode2_type}.")