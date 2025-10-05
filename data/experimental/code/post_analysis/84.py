"""
Generated ETABS Script
Description: Retrieve the modal load participation ratio for the fundamental mode in the X-direction from the analyzed ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 16:41:18
Steps: 1
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal load participation ratios for all modes and analysis cases. The fundamental mode in the X-direction will be identified from these results.
NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret = SapModel.Results.ModalParticipatingMassRatios()

# Identify the fundamental mode in the X-direction
fundamental_mode_x_index = -1
max_ux_participation = -1.0

for i in range(NumberResults):
    if UX[i] > max_ux_participation:
        max_ux_participation = UX[i]
        fundamental_mode_x_index = i

# The mode number is 1-indexed, so add 1 to the found index
fundamental_mode_x = fundamental_mode_x_index + 1
fundamental_mode_x_period = Period[fundamental_mode_x_index]

print(f"Fundamental mode in X-direction: Mode {fundamental_mode_x} (Period: {fundamental_mode_x_period:.3f} s)")