"""
Generated ETABS Script
Description: Modify the existing rectangular frame section 'B14x28' by changing its depth to 30 inches and then renaming it to 'B14x30'.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 20:02:33
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the current properties of the rectangular frame section named 'B14x28' to obtain its material, width, and other relevant parameters.
section_name = 'B14x28'
FileName, MatProp, T3, T2, Color, Notes, GUID, ret = SapModel.PropFrame.GetRectangle(section_name)

if ret == 0:
    print(f"Successfully retrieved properties for section '{section_name}':")
    print(f"  Material: {MatProp}")
    print(f"  Depth (T3): {T3} ft")
    print(f"  Width (T2): {T2} ft")
else:
    print(f"Error retrieving properties for section '{section_name}'. Return code: {ret}")

# Step 2: Modify the rectangular frame section 'B14x28' by setting its depth to 30 inches, while keeping its material and width the same as the original 'B14x28' section.
new_depth_inches = 30
new_depth_feet = new_depth_inches / 12.0

ret = SapModel.PropFrame.SetRectangle(section_name, MatProp, new_depth_feet, T2)

if ret == 0:
    print(f"Successfully modified section '{section_name}'. New depth: {new_depth_inches} inches ({new_depth_feet} ft)")
else:
    print(f"Error modifying section '{section_name}'. Return code: {ret}")

# Step 3: Rename the modified frame section from 'B14x28' to 'B14x30'.
new_section_name = 'B14x30'
ret = SapModel.PropFrame.ChangeName(section_name, new_section_name)

if ret == 0:
    print(f"Successfully renamed section from '{section_name}' to '{new_section_name}'.")
    section_name = new_section_name # Update section_name for subsequent steps
else:
    print(f"Error renaming section '{section_name}'. Return code: {ret}")