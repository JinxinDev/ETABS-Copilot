"""
Generated ETABS Script
Description: Retrieve all unique beam section properties used in the model and list their dimensions. This involves identifying frame objects that act as beams, extracting their assigned section properties, and then querying the dimensions for each unique section.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-19 16:43:11
Steps: 6
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Get a list of all frame object names currently defined in the model.
frame_obj_num, frame_names, ret = SapModel.FrameObj.GetNameList()

# Step 2: Initialize an empty set to store unique beam section property names.
beam_section_names = set()

# Step 3: Iterate through each frame object. For each frame object, retrieve the names of its end point objects. Then, get the Cartesian coordinates (X, Y, Z) for each of these end points. Based on the Z-coordinates of the end points, determine if the frame object is a beam (i.e., if the Z-coordinates are approximately the same, indicating a horizontal element). If it is a beam, retrieve the name of the frame section property assigned to it and add this section property name to the set of unique beam section names.
for frame_ID in frame_names:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Determine if the frame object is a beam (horizontal element).
    # A small tolerance is used for comparing Z-coordinates due to potential floating-point inaccuracies.
    if abs(Z1 - Z2) < 0.001: # Assuming a tolerance of 0.001 feet for Z-coordinate difference
        # If it's a beam, retrieve its section property name.
        section_property, _, ret = SapModel.FrameObj.GetSection(frame_ID)
        # Add the section property name to the set of unique beam section names.
        beam_section_names.add(section_property)

# Step 4: Initialize an empty dictionary to store the dimensions for each unique beam section.
beam_section_dimensions = {}

# Step 5: Iterate through each unique beam section name collected. For each section, attempt to retrieve its dimensions. First, try to get rectangular section dimensions using 'cPropFrame.GetRectangle'. If that fails (meaning it's not a rectangular section), then try to get I-section dimensions using 'cPropFrame.GetISection_1'. Store the retrieved dimensions (width, depth, flange thickness, web thickness, etc.) in the dictionary, associated with the section name. If neither method successfully retrieves dimensions, note that the section type is not supported by the available dimension retrieval methods.
for section_name in beam_section_names:
    # Attempt to retrieve rectangular section dimensions
    FileName, MatProp, T3, T2, Color, Notes, GUID, ret = SapModel.PropFrame.GetRectangle(section_name)

    if ret == 0: # Successfully retrieved rectangular dimensions
        beam_section_dimensions[section_name] = {
            "type": "Rectangle",
            "width": T2, # T2 is width
            "depth": T3  # T3 is depth
        }
    else:
        # If not rectangular, attempt to retrieve I-section dimensions
        FileName, MatProp, T3, T2, Tf, Tw, T2b, Tfb, FilletRadius, Color, Notes, GUID, ret = SapModel.PropFrame.GetISection_1(section_name)

        if ret == 0: # Successfully retrieved I-section dimensions
            beam_section_dimensions[section_name] = {
                "type": "ISection",
                "depth": T3,
                "top_flange_width": T2,
                "top_flange_thickness": Tf,
                "web_thickness": Tw,
                "bottom_flange_width": T2b,
                "bottom_flange_thickness": Tfb
            }
        else:
            # If neither rectangular nor I-section, note as unsupported
            beam_section_dimensions[section_name] = {
                "type": "Unsupported",
                "note": "Section type not supported by available dimension retrieval methods."
            }

# Step 6: Output or display the collected unique beam section names along with their respective dimensions.
print("\n--- Unique Beam Section Dimensions ---")
for section_name, dimensions in beam_section_dimensions.items():
    print(f"Section Name: {section_name}")
    print(f"  Type: {dimensions['type']}")
    if dimensions['type'] == "Rectangle":
        print(f"  Width: {dimensions['width']:.3f} ft")
        print(f"  Depth: {dimensions['depth']:.3f} ft")
    elif dimensions['type'] == "ISection":
        print(f"  Depth: {dimensions['depth']:.3f} ft")
        print(f"  Top Flange Width: {dimensions['top_flange_width']:.3f} ft")
        print(f"  Top Flange Thickness: {dimensions['top_flange_thickness']:.3f} ft")
        print(f"  Web Thickness: {dimensions['web_thickness']:.3f} ft")
        print(f"  Bottom Flange Width: {dimensions['bottom_flange_width']:.3f} ft")
        print(f"  Bottom Flange Thickness: {dimensions['bottom_flange_thickness']:.3f} ft")
    else:
        print(f"  Note: {dimensions['note']}")
    print("------------------------------------")
