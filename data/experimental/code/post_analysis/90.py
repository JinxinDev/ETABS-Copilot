"""
Generated ETABS Script
Description: Identify the first three coupled modes in the ETABS model, where a coupled mode is defined by having mass participation greater than 15% in both a translational (UX or UY) and a rotational (RZ) direction simultaneously.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 18:02:27
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal participating mass ratios for all modes from the default modal analysis case. This will provide the mass participation percentages for translational (UX, UY, UZ) and rotational (RX, RY, RZ) directions for each mode.
(NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret) = SapModel.Results.ModalParticipatingMassRatios()

# Step 2: Iterate through the retrieved modal participating mass ratios. For each mode, check if the mass participation is greater than 15% (0.15) in either the UX or UY direction, AND simultaneously greater than 15% (0.15) in the RZ direction. Store the mode numbers that satisfy these conditions.
qualifying_modes = []
for i in range(NumberResults):
    mode_num = i + 1
    if (UX[i] > 0.15 or UY[i] > 0.15) and RZ[i] > 0.15:
        qualifying_modes.append(mode_num)

# Step 3: From the identified coupled modes, report the first three modes that meet the specified criteria.
print("First three coupled modes (UX/UY > 15% AND RZ > 15%):")
if len(qualifying_modes) > 0:
    for i in range(min(3, len(qualifying_modes))):
        print(f"Mode {qualifying_modes[i]}")
else:
    print("No coupled modes found meeting the criteria.")