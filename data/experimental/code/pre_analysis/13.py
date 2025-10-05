"""
Generated ETABS Script
Description: Retrieve all grid line coordinates and spacings in the X and Y directions for all defined grid systems in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-11 16:22:05
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined grid systems in the model.
num_of_grid_systems, grid_system_names, ret = SapModel.GridSys.GetNameList()

# Step 2: For each retrieved grid system name, get its Cartesian grid data, which includes grid line coordinates and spacings in the X and Y directions.
grid_systems_data = []
for grid_name in grid_system_names:
    # Retrieve Cartesian grid data for the current grid system
    Xo, Yo, RZ, StoryRangeIsDefault, TopStory, BottomStory, BubbleSize, GridColor, \
    NumXLines, GridLineIDX, OrdinateX, VisibleX, BubbleLocX, \
    NumYLines, GridLineIDY, OrdinateY, VisibleY, BubbleLocY, \
    NumGenLines, GridLineIDGen, GenOrdX1, GenOrdY1, GenOrdX2, GenOrdY2, VisibleGen, BubbleLocGen, ret \
    = SapModel.GridSys.GetGridSysCartesian(grid_name)

    # Store the retrieved data for subsequent steps
    grid_systems_data.append({
        "Name": grid_name,
        "Xo": Xo,
        "Yo": Yo,
        "RZ": RZ,
        "StoryRangeIsDefault": StoryRangeIsDefault,
        "TopStory": TopStory,
        "BottomStory": BottomStory,
        "BubbleSize": BubbleSize,
        "GridColor": GridColor,
        "NumXLines": NumXLines,
        "GridLineIDX": GridLineIDX,
        "OrdinateX": OrdinateX,
        "VisibleX": VisibleX,
        "BubbleLocX": BubbleLocX,
        "NumYLines": NumYLines,
        "GridLineIDY": GridLineIDY,
        "OrdinateY": OrdinateY,
        "VisibleY": VisibleY,
        "BubbleLocY": BubbleLocY,
        "NumGenLines": NumGenLines,
        "GridLineIDGen": GridLineIDGen,
        "GenOrdX1": GenOrdX1,
        "GenOrdY1": GenOrdY1,
        "GenOrdX2": GenOrdX2,
        "GenOrdY2": GenOrdY2,
        "VisibleGen": VisibleGen,
        "BubbleLocGen": BubbleLocGen
    })
print(grid_systems_data)