"""
Generated ETABS Script
Description: Retrieve the maximum shear force, corresponding axial load, and the location for all beam elements located on 'Story4' in the ETABS model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 17:14:34
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Get the names of all frame objects that are located on 'Story4'.
story_name = "Story4"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

# Step 2: Iterate through the retrieved frame objects on 'Story4'. For each frame object, determine if it is a beam by checking its assigned section property. A section is considered a beam section if beam rebar data can be retrieved for it.
beam_frame_IDs = []

for frame_ID in frame_ID_tuple:
    section_property, _, ret_section = SapModel.FrameObj.GetSection(frame_ID)
    
    # Attempt to retrieve beam rebar data for the section property
    # We only care about the return value to determine if it's a beam section
    _, _, _, _, _, _, _, _, ret_rebar_beam = SapModel.PropFrame.GetRebarBeam(section_property)
    
    if ret_rebar_beam == 0:
        # If GetRebarBeam returns 0, it means beam rebar data exists for this section
        beam_frame_IDs.append(frame_ID)

# Step 3: For each identified beam on 'Story4', retrieve its frame forces, including axial load (P) and shear forces (V2, V3), along its length for all load cases or combinations.
beam_forces_data = {}
ObjectElm = 0

for frame_ID in beam_frame_IDs:
    (NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret) = SapModel.Results.FrameForce(frame_ID, ObjectElm)

    if ret == 0:
        beam_forces_data[frame_ID] = {
            "P": P,
            "V2": V2,
            "V3": V3,
            "ObjSta": ObjSta,
            "LoadCase": LoadCase
        }
    else:
        print(f"Error retrieving frame forces for beam: {frame_ID}")

# Step 4: Process the retrieved frame forces for each beam. For each beam, find the maximum absolute shear force (considering both V2 and V3) and identify the corresponding axial load (P) and the location (station) along the beam where this maximum shear occurs. Report these values for each beam.
processed_beam_forces = {}

for frame_ID, data in beam_forces_data.items():
    max_abs_shear = -1.0
    max_shear_P = None
    max_shear_station = None
    max_shear_load_case = None

    # Assuming all lists (P, V2, V3, ObjSta, LoadCase) have the same length
    num_results = len(data["P"])

    for i in range(num_results):
        current_P = data["P"][i]
        current_V2 = data["V2"][i]
        current_V3 = data["V3"][i]
        current_ObjSta = data["ObjSta"][i]
        current_LoadCase = data["LoadCase"][i]

        current_abs_shear = max(abs(current_V2), abs(current_V3))

        if current_abs_shear > max_abs_shear:
            max_abs_shear = current_abs_shear
            max_shear_P = current_P
            max_shear_station = current_ObjSta
            max_shear_load_case = current_LoadCase
    
    processed_beam_forces[frame_ID] = {
        "max_abs_shear": max_abs_shear,
        "corresponding_P": max_shear_P,
        "location_station": max_shear_station,
        "load_case": max_shear_load_case
    }
    print(processed_beam_forces)