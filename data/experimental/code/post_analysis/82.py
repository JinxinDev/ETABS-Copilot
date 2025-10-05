"""
Generated ETABS Script
Description: Retrieve the modal period, cyclic frequency, and eigenvalue for the third vibrational mode from the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 16:31:23
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal period, cyclic frequency, circular frequency, and eigenvalue for all modal load cases.
(NumberResults, LoadCase, StepType, StepNum, Period, Frequency, CircFreq, EigenValue, ret) = SapModel.Results.ModalPeriod()

# Step 2: Filter the retrieved modal analysis results to specifically extract the modal period, cyclic frequency, and eigenvalue for the third vibrational mode.
third_mode_period = Period[2]
third_mode_frequency = Frequency[2]
third_mode_eigenvalue = EigenValue[2]
print(third_mode_period,third_mode_frequency,third_mode_eigenvalue)