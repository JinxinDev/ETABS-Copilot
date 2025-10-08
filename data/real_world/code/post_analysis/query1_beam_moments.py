#etabs: For all beams on stories 2 through 5, extract and create a table showing: beam label, story level, start point coordinates, end point coordinates, maximum positive moment with its value and governing load combination, maximum negative moment with its value and governing load combination, and beam length. Sort the results by story level then by maximum absolute moment in descending order.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names of all stories in the model to identify stories 2 through 5.
NumberNames, StoryNameTuple, ret = SapModel.Story.GetNameList()

# Step 2: Iterate through stories 'Story2', 'Story3', 'Story4', and 'Story5'. For each story, get the names of all frame objects present on that story.
target_stories = ['Story2', 'Story3', 'Story4', 'Story5']
story_frame_objects = {}

for story_name in target_stories:
    frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)
    if ret == 0:
        story_frame_objects[story_name] = list(frame_ID_tuple)
    else:
        print(f"Error retrieving frame objects for story {story_name}: {ret}")

# Step 3: For each identified frame object, determine if it is a beam. This involves retrieving the names of the point objects connected to the frame object (assuming a method like GetConnectedPoints exists in cFrameObj), then getting the Cartesian coordinates of these points using their names. A frame object is considered a beam if the Z-coordinates of its start and end points are approximately equal. Calculate the beam length from these coordinates.
beams_data = {}
tolerance = 1e-3 # feet, for Z-coordinate comparison

for story_name, frame_ID_list in story_frame_objects.items():
    beams_on_story = []
    for frame_ID in frame_ID_list:
        # Get the names of the two point objects (joints) at the ends of the frame.
        point_1, point_2, ret_points = SapModel.FrameObj.GetPoints(frame_ID)

        if ret_points == 0:
            # Get the global Cartesian coordinates (X, Y, Z) for the first point.
            X1, Y1, Z1, ret_coord1 = SapModel.PointObj.GetCoordCartesian(point_1)

            # Get the global Cartesian coordinates (X, Y, Z) for the second point.
            X2, Y2, Z2, ret_coord2 = SapModel.PointObj.GetCoordCartesian(point_2)

            if ret_coord1 == 0 and ret_coord2 == 0:
                # Check if the Z-coordinates are approximately equal to identify a beam
                if abs(Z1 - Z2) < tolerance:
                    # Calculate beam length
                    length = ((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)**0.5/12
                    beams_on_story.append({"frame_ID": frame_ID, "length": length})
            else:
                print(f"Error retrieving coordinates for frame {frame_ID} points: {ret_coord1}, {ret_coord2}")
        else:
            print(f"Error retrieving points for frame {frame_ID}: {ret_points}")
    if beams_on_story:
        beams_data[story_name] = beams_on_story

# Step 4: Set all load combinations for output, then retrieve frame forces
# First, get all load combination names
NumCombos, ComboNames, ret = SapModel.RespCombo.GetNameList()
SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
if ret == 0:
    # Select all combinations for outputs
    for combo_name in ComboNames[:]:
        ret_select = SapModel.Results.Setup.SetComboSelectedForOutput(combo_name, True)
        if ret_select != 0:
            print(f"Warning: Could not select combo {combo_name} for output")
else:
    print(f"Error retrieving combination names: {ret}")

beam_moments_data = {}

for story_name, beams_on_story in beams_data.items():
    story_beam_moments = []
    for beam_info in beams_on_story:
        frame_ID = beam_info["frame_ID"]
        beam_length = beam_info["length"]

        # Retrieve frame force results for all selected combinations
        # ObjectElm = 0 indicates results for the object itself
        NumberResults, Obj, ObjSta, Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3, ret = SapModel.Results.FrameForce(frame_ID, 0)

        if ret == 0 and NumberResults > 0:
            max_pos_M3 = -float('inf')
            governing_pos_combo = None
            max_neg_M3 = float('inf')
            governing_neg_combo = None

            for i in range(NumberResults):
                current_M3 = M3[i]/12000
                current_LoadCase = LoadCase[i]

                if current_M3 > max_pos_M3:
                    max_pos_M3 = current_M3
                    governing_pos_combo = current_LoadCase

                if current_M3 < max_neg_M3:
                    max_neg_M3 = current_M3
                    governing_neg_combo = current_LoadCase
            
            story_beam_moments.append({
                "frame_ID": frame_ID,
                "length": beam_length,
                "max_pos_M3": max_pos_M3,
                "governing_pos_combo": governing_pos_combo,
                "max_neg_M3": max_neg_M3,
                "governing_neg_combo": governing_neg_combo
            })
        else:
            print(f"Error or no results for beam {frame_ID}: ret={ret}, NumberResults={NumberResults}")
    
    if story_beam_moments:
        beam_moments_data[story_name] = story_beam_moments

# Step 5: Collect all extracted data for each beam (beam label, story level, start point coordinates, end point coordinates, maximum positive moment, governing load combination for positive moment, maximum negative moment, governing load combination for negative moment, and beam length) into a structured format.
all_beams_collected_data = []

for story_name, beams_on_story_moments in beam_moments_data.items():
    for beam_moment_info in beams_on_story_moments:
        frame_ID = beam_moment_info["frame_ID"]
        beam_length = beam_moment_info["length"]
        max_pos_M3 = beam_moment_info["max_pos_M3"]
        governing_pos_combo = beam_moment_info["governing_pos_combo"]
        max_neg_M3 = beam_moment_info["max_neg_M3"]
        governing_neg_combo = beam_moment_info["governing_neg_combo"]

        # Re-retrieve point objects (joints) at the ends of the frame
        point_1, point_2, ret_points = SapModel.FrameObj.GetPoints(frame_ID)

        if ret_points == 0:
            # Re-retrieve global Cartesian coordinates for the start and end points
            X1, Y1, Z1, ret_coord1 = SapModel.PointObj.GetCoordCartesian(point_1)
            X2, Y2, Z2, ret_coord2 = SapModel.PointObj.GetCoordCartesian(point_2)

            if ret_coord1 == 0 and ret_coord2 == 0:
                beam_data = {
                    "frame_ID": frame_ID,
                    "story_level": story_name,
                    "start_point_coords": {"X": X1, "Y": Y1, "Z": Z1},
                    "end_point_coords": {"X": X2, "Y": Y2, "Z": Z2},
                    "max_pos_M3": max_pos_M3,
                    "governing_pos_combo": governing_pos_combo,
                    "max_neg_M3": max_neg_M3,
                    "governing_neg_combo": governing_neg_combo,
                    "beam_length": beam_length
                }
                all_beams_collected_data.append(beam_data)
            else:
                print(f"Error retrieving coordinates for points of frame {frame_ID}: {ret_coord1}, {ret_coord2}")
        else:
            print(f"Error retrieving points for frame {frame_ID}: {ret_points}")

# Step 6: Sort the collected beam data. First, sort by story level (e.g., by converting story names to numerical values or using story elevations obtained via cStory.GetElevation for numerical comparison). Second, sort by the maximum absolute moment (comparing the absolute values of maximum positive and maximum negative moments) in descending order.
story_elevations = {}
for story_name in target_stories:
    height, ret = SapModel.Story.GetElevation(story_name)
    if ret == 0:
        story_elevations[story_name] = height
    else:
        print(f"Error retrieving elevation for story {story_name}: {ret}")

# Sort the collected beam data
all_beams_collected_data.sort(key=lambda beam: (
    story_elevations.get(beam["story_level"], 0), # Primary sort by story elevation (ascending)
    -max(abs(beam["max_pos_M3"]), abs(beam["max_neg_M3"])) # Secondary sort by max absolute moment (descending)
))

# Step 7: Present the sorted beam data in a clear, readable table format.
print("\n--- Sorted Beam Data ---")
print(f"{"Frame ID":<15} {"Story":<10} {"Start (X,Y,Z)":<30} {"End (X,Y,Z)":<30} {"Length (ft)":<15} {"Max +M3 (kip-ft)":<20} {"Combo (+)":<15} {"Max -M3 (kip-ft)":<20} {"Combo (-)":<15}")
print("-" * 200)

for beam in all_beams_collected_data:
    frame_ID = beam["frame_ID"]
    story_level = beam["story_level"]
    start_coords = beam["start_point_coords"]
    end_coords = beam["end_point_coords"]
    beam_length = beam["beam_length"]
    max_pos_M3 = beam["max_pos_M3"]
    governing_pos_combo = beam["governing_pos_combo"]
    max_neg_M3 = beam["max_neg_M3"]
    governing_neg_combo = beam["governing_neg_combo"]

    start_str = f"({start_coords['X']:.2f}, {start_coords['Y']:.2f}, {start_coords['Z']:.2f})"
    end_str = f"({end_coords['X']:.2f}, {end_coords['Y']:.2f}, {end_coords['Z']:.2f})"

    print(f"{frame_ID:<15} {story_level:<10} {start_str:<30} {end_str:<30} {beam_length:<15.2f} {max_pos_M3:<20.2f} {governing_pos_combo:<15} {max_neg_M3:<20.2f} {governing_neg_combo:<15}")
