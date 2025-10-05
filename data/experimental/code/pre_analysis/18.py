"""
Generated ETABS Script
Description: Count the total number of defined I-sections and rectangular frame sections in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 09:35:10
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined I-section frame properties.
prop_type_map = {
    1: "I",
    2: "Channel",
    3: "T",
    4: "Angle",
    5: "DblAngle",
    6: "Box",
    7: "Pipe",
    8: "Rectangular",
    9: "Circle",
    10: "General"
}

# Call the function to get all frame property definitions
num_names, all_frame_names, prop_type, t3, t2, tf, tw, t2b, tfb, ret = SapModel.PropFrame.GetAllFrameProperties()

i_section_names = []
if ret == 0: # Check if the API call was successful
    for i in range(num_names):
        if prop_type[i] == 1: # 1 corresponds to "I" section type based on the provided map
            i_section_names.append(all_frame_names[i])

# The variable 'i_section_names' now contains a list of all defined I-section frame property names.

# Step 2: Retrieve the names of all defined rectangular frame properties.
rectangular_section_names = []
if ret == 0: # Check if the API call was successful from the previous step
    for i in range(num_names):
        if prop_type[i] == 8: # 8 corresponds to "Rectangular" section type based on the provided map
            rectangular_section_names.append(all_frame_names[i])

# The variable 'rectangular_section_names' now contains a list of all defined rectangular frame property names.

# Step 3: Count the number of I-section frame properties found.
num_i_sections = len(i_section_names)
# The variable 'num_i_sections' now contains the count of I-section frame properties.

# Step 4: Count the number of rectangular frame properties found.
num_rectangular_sections = len(rectangular_section_names)
# The variable 'num_rectangular_sections' now contains the count of rectangular frame properties.

# Step 5: Report the total count of I-sections and rectangular sections.
print(f"Total I-section frame properties found: {num_i_sections}")
print(f"Total rectangular frame properties found: {num_rectangular_sections}")