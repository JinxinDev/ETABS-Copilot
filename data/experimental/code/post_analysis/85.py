"""
Generated ETABS Script
Description: Identify the mode number that corresponds to the first primary torsional mode of the structure by analyzing modal participating mass ratios.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 16:46:42
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal participating mass ratios for all modes from the analysis results. This data will include translational (UX, UY) and rotational (RZ) mass participation for each mode.
NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret = SapModel.Results.ModalParticipatingMassRatios()

# Step 2: Analyze the retrieved modal participating mass ratios to identify the first mode where the rotational mass participation (RZ) is significantly dominant compared to the translational mass participation (UX and UY). This mode will be considered the first primary torsional mode.
first_primary_torsional_mode_number = -1
torsional_dominance_factor = 1.5

for i in range(NumberResults):
    current_ux = UX[i]
    current_uy = UY[i]
    current_rz = RZ[i]

    # A mode is considered a primary torsional mode if its rotational mass participation (RZ)
    # is significantly dominant compared to its translational mass participation (UX and UY).
    # We define "significantly dominant" as RZ being at least 'torsional_dominance_factor'
    # times greater than both UX and UY.
    if current_rz > torsional_dominance_factor * current_ux and \
       current_rz > torsional_dominance_factor * current_uy:
        first_primary_torsional_mode_number = i + 1 # Store 1-indexed mode number
        break # Found the first one, so we can stop