"""
Generated ETABS Script
Description: Generate a report summarizing the top 5 modes with the highest mass participation in the Y-direction from the current ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 16:33:42
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Retrieve the modal participating mass ratios for all modes and analysis cases from the ETABS model.
NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, RX, RY, RZ, SumRX, SumRY, SumRZ, ret = SapModel.Results.ModalParticipatingMassRatios()

# Step 2: Process the retrieved modal participating mass ratios to filter for the Y-direction, sort them in descending order, and identify the top 5 modes with the highest mass participation. Then, generate a report summarizing these top 5 modes.
modal_data = []
for i in range(NumberResults):
    mode_number = i + 1
    modal_data.append({"mode": mode_number, "uy_participation": UY[i], "period": Period[i]})

# Sort by UY participation in descending order
sorted_modal_data = sorted(modal_data, key=lambda x: x["uy_participation"], reverse=True)

# Get the top 5 modes
top_5_modes = sorted_modal_data[:5]

# Generate report
print("\n--- Top 5 Modal Participating Mass Ratios (Y-Direction) ---")
print(f"{'Mode':<8}{'UY Participation':<20}{'Period (s)':<15}")
print("-" * 53)
for mode_info in top_5_modes:
    print(f"{mode_info['mode']:<8}{mode_info['uy_participation'] * 100:<19.2f}% {mode_info['period']:<15.4f}")
print("----------------------------------------------------")