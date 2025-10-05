"""
Generated ETABS Script
Description: Find the maximum bending moment for each frame section property defined in the model by iterating through all frame objects and their assigned sections, considering all load cases and combinations.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 09:38:02
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined frame section properties in the model.
frame_section_names_count, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 2: Retrieve the names of all defined load patterns in the model.
load_pattern_names_count, load_pattern_names, ret = SapModel.LoadPatterns.GetNameList()

# Step 3: Retrieve the names of all defined load combinations in the model.
load_combination_names_count, load_combination_names, ret = SapModel.RespCombo.GetNameList()

# Step 4: Combine the lists of load patterns and load combinations to create a comprehensive list of analysis cases to consider for results.
analysis_cases = load_pattern_names + load_combination_names

# Step 5: Initialize a data structure (e.g., a dictionary) to store the maximum absolute bending moment found for each frame section property. Initialize all values to zero or a very small negative number to ensure any valid moment is captured as the maximum.
max_abs_bending_moment_per_section = {section_name: 0.0 for section_name in frame_section_names}

# Step 6: Retrieve the names of all frame objects present in the model.
frame_object_count, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 7: Iterate through each frame object. For each frame object, determine its assigned section property using 'GetSection'. Then, iterate through all defined analysis cases (load patterns and combinations). For each analysis case, retrieve the frame forces (including bending moments M2 and M3) along the length of the frame object using 'FrameForce'. From these forces, find the maximum absolute bending moment (max(abs(M2), abs(M3))) at any station along the object. Compare this value with the currently stored maximum for the frame object's assigned section property and update if a larger absolute moment is found.
ObjectElm = 0

for frame_object_name in frame_object_names:
    section_property, _, ret = SapModel.FrameObj.GetSection(frame_object_name)

    for case_name in analysis_cases:
        (
            NumberResults,
            Obj,
            ObjSta,
            Elm,
            ElmSta,
            LoadCase,
            StepType,
            StepNum,
            P,
            V2,
            V3,
            T,
            M2,
            M3,
            ret
        ) = SapModel.Results.FrameForce(frame_object_name, ObjectElm)

        current_max_abs_moment = 0.0
        for i in range(NumberResults):
            abs_m2 = abs(M2[i])
            abs_m3 = abs(M3[i])
            current_max_abs_moment = max(current_max_abs_moment, abs_m2, abs_m3)

        if current_max_abs_moment > max_abs_bending_moment_per_section[section_property]:
            max_abs_bending_moment_per_section[section_property] = current_max_abs_moment

# Step 8: Report the maximum absolute bending moment found for each frame section property.
print("\nMaximum Absolute Bending Moment per Frame Section Property:")
for section_name, max_moment in max_abs_bending_moment_per_section.items():
    print(f"  Section: {section_name}, Max Abs Bending Moment: {max_moment:.2f} kip-ft")