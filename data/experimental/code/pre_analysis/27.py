"""
Generated ETABS Script
Description: This plan outlines the steps to identify all beams in the ETABS model that have a span-to-depth ratio greater than 20, indicating potential susceptibility to deflection issues. It involves retrieving frame object names, their assigned section properties, and then calculating the ratio based on section depth and assumed span length.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-14 17:50:53
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all frame object names defined in the ETABS model. This list will be iterated to find potential beams.
frame_obj_num, frame_names, ret = SapModel.FrameObj.GetNameList()

# Step 2: Retrieve comprehensive details for all defined frame section properties. This information is crucial for determining the depth of each section, which is a component of the span-to-depth ratio. The `GetAllFrameProperties` method is assumed to provide sufficient detail to extract the depth for any given section name.
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
num_names, my_name, prop_type, t3, t2, tf, tw, t2b, tfb, ret = SapModel.PropFrame.GetAllFrameProperties()
section_props_dict = {}
for i in range(num_names):
    section_name = my_name[i]
    section_type_code = prop_type[i]
    section_type_name = prop_type_map.get(section_type_code)
    details = {
        "Type": section_type_name,
        "Depth (t3)": t3[i],
        "Width (t2)": t2[i]
    }
    if section_type_code in [1, 2, 3, 5]:
        details["FlangeThk (tf)"] = tf[i]
        details["WebThk (tw)"] = tw[i]
    section_props_dict[section_name] = details

# Step 3: For each frame object name obtained, first retrieve its assigned frame section property name using `cFrameObj.GetSection`. Then, using the details of all frame section properties (from the previous step), determine the depth of this specific section. Concurrently, obtain the length (span) of the current frame object. It is assumed that the code generator can determine if a frame object is a beam (e.g., by checking its orientation or internal ETABS object type) and can retrieve its length. Calculate the span-to-depth ratio for each identified beam. If this ratio is greater than 20, identify and report the beam as potentially susceptible to deflection issues.
import math

potential_deflection_beams = []

for frame_name in frame_names:
    # 1. Retrieve assigned frame section property name
    section_property,_, ret = SapModel.FrameObj.GetSection(frame_name)

    # 2. Determine the depth of this specific section
    section_details = section_props_dict.get(section_property)
    if section_details and "Depth (t3)" in section_details:
        depth = section_details["Depth (t3)"]
    else:
        print(f"Warning: Could not find depth for section {section_property} of frame {frame_name}. Skipping.")
        continue

    # 3. Obtain the length (span) of the current frame object
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_name)

    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Calculate length (span) using Euclidean distance
    span = math.sqrt(math.pow(X2 - X1, 2) + math.pow(Y2 - Y1, 2) + math.pow(Z2 - Z1, 2))

    # 4. Determine if it's a beam (not a column)
    # A frame is considered a column if its X and Y coordinates are essentially the same.
    # Using a small tolerance for float comparison.
    is_column = (abs(X1 - X2) < 1e-6 and abs(Y1 - Y2) < 1e-6)

    if not is_column: # It's a beam or inclined member
        # 5. Calculate the span-to-depth ratio
        if depth > 0: # Avoid division by zero
            span_to_depth_ratio = span / depth
            # 6. Identify and report if ratio > 20
            if span_to_depth_ratio > 20:
                potential_deflection_beams.append({
                    "Frame Name": frame_name,
                    "Section Name": section_property,
                    "Span": span,
                    "Depth": depth,
                    "Span-to-Depth Ratio": span_to_depth_ratio
                })
                print(f"Potential deflection issue: Beam '{frame_name}' (Section: '{section_property}') has a span-to-depth ratio of {span_to_depth_ratio:.2f} (Span: {span:.2f} ft, Depth: {depth:.2f} ft).")
        else:
            print(f"Warning: Depth for beam '{frame_name}' is zero or negative. Cannot calculate span-to-depth ratio.")

if potential_deflection_beams:
    print("\n--- Summary of Beams with Potential Deflection Issues ---")
    for beam_data in potential_deflection_beams:
        print(f"Frame: {beam_data['Frame Name']}, Section: {beam_data['Section Name']}, Ratio: {beam_data['Span-to-Depth Ratio']:.2f}")
else:
    print("\nNo beams identified with span-to-depth ratio greater than 20.")