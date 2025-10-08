#etabs: Identify all beams that satisfy ALL of the following conditions: beam length greater than 10 feet AND maximum moment (absolute value, any combination) exceeds 50 kip-ft AND located on stories 3 or 4. For beams meeting these criteria, report: beam label, story, length, maximum moment value, and which load combination governs.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names of all defined stories in the model to identify 'Story3' and 'Story4'.
NumberNames, StoryNameTuple, ret = SapModel.Story.GetNameList()

# Step 2: Get the names of all frame objects located on 'Story3' and 'Story4'.
story3_frame_names = []
story4_frame_names = []

for story_name in StoryNameTuple:
    if story_name == "Story3":
        frame_obj_num_story3, frame_ID_tuple_story3, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
        story3_frame_names.extend(frame_ID_tuple_story3)
    elif story_name == "Story4":
        frame_obj_num_story4, frame_ID_tuple_story4, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
        story4_frame_names.extend(frame_ID_tuple_story4)

# Step 3: For each frame object identified, determine if it is a beam (horizontal element) and calculate its length. This involves getting the names of the end points of each frame object, then retrieving their Cartesian coordinates. A frame object is considered a beam if the absolute difference in Z-coordinates of its end points is less than a small tolerance (e.g., 0.1 feet). The length is calculated from the 3D coordinates of its end points. Store the beam label, its story, and calculated length.
beam_data = []
z_tolerance = 0.1 # feet, for identifying horizontal elements

for frame_name in story3_frame_names:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_name)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    if abs(Z2 - Z1) < z_tolerance:
        # It's a beam (horizontal element)
        length = ((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)**0.5/12
        beam_data.append({"label": frame_name, "story": "Story3", "length": length})

for frame_name in story4_frame_names:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_name)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    if abs(Z2 - Z1) < z_tolerance:
        # It's a beam (horizontal element)
        length = ((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)**0.5/12
        beam_data.append({"label": frame_name, "story": "Story4", "length": length})

# Step 4: Select ALL load combinations for output (do this ONCE)
num_load_combinations, load_combination_names, ret = SapModel.RespCombo.GetNameList()

for combo_name in load_combination_names:
    ret = SapModel.Results.Setup.SetComboSelectedForOutput(combo_name, True)

# Step 5: For each beam, retrieve results (will include ALL selected combinations)
for beam_info in beam_data:
    beam_info["max_abs_moment"] = 0.0
    beam_info["governing_combo"] = ""
    frame_name = beam_info["label"]

    # Retrieve frame forces - returns results for ALL selected combinations
    NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret = SapModel.Results.FrameForce(frame_name, 0)

    if ret == 0 and NumberResults > 0:
        for i in range(NumberResults):
            combo_name = LoadCase[i]  # The combination name for this result
            current_m2 = M2[i]/12000
            current_m3 = M3[i]/12000

            abs_m2 = abs(current_m2)
            abs_m3 = abs(current_m3)

            if abs_m2 > beam_info["max_abs_moment"]:
                beam_info["max_abs_moment"] = abs_m2
                beam_info["governing_combo"] = combo_name

            if abs_m3 > beam_info["max_abs_moment"]:
                beam_info["max_abs_moment"] = abs_m3
                beam_info["governing_combo"] = combo_name

# Step 6: Filter the identified beams based on the following criteria: beam length greater than 10 feet AND maximum absolute moment (from any combination) exceeds 50 kip-ft. For all beams that satisfy both conditions, report their beam label, story, calculated length, the maximum absolute moment value, and the name of the load combination that governs this maximum moment.
print("\nFiltered Beams (Length > 10 ft AND Max Abs Moment > 50 kip-ft):")
print(beam_data)
for beam_info in beam_data:
    if beam_info["length"] > 10.0 and beam_info["max_abs_moment"] > 50.0:
        print(f"  Beam Label: {beam_info["label"]}")
        print(f"  Story: {beam_info["story"]}")
        print(f"  Length: {beam_info["length"]:.2f} ft")
        print(f"  Max Abs Moment: {beam_info["max_abs_moment"]:.2f} kip-ft")
        print(f"  Governing Combo: {beam_info["governing_combo"]}")
        print("----------------------------------------")

