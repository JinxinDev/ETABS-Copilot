"""
Generated ETABS Script
Description: Create multiple rectangular beam section sizes, assign them to existing beams based on their length, and then generate a section usage summary for beams on each floor of the model.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-20 17:51:54
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
print("ETABS connection established")

# Step 1: Add a concrete material property named 'CONC4000' with a grade of 'f'c 4000 psi' from the 'United States' region and 'Customary' standard.
material_name, ret_code = SapModel.PropMaterial.AddMaterial("CONC4000", 2, "United States", "Customary", "f'c 4000 psi")

# Step 2: Define three rectangular frame section properties for beams: 'B12x18' with a depth of 18 inches and width of 12 inches, 'B18x24' with a depth of 24 inches and width of 18 inches, and 'B24x30' with a depth of 30 inches and width of 24 inches. All sections should use the 'CONC4000' material.
ret_code = SapModel.PropFrame.SetRectangle("B12x18", "CONC4000", 18/12, 12/12)
ret_code = SapModel.PropFrame.SetRectangle("B18x24", "CONC4000", 24/12, 18/12)
ret_code = SapModel.PropFrame.SetRectangle("B24x30", "CONC4000", 30/12, 24/12)

# Step 3: Retrieve the names of all frame objects in the model.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 4: For each frame object, retrieve its end point names and then their Cartesian coordinates to calculate the length and determine if it is a horizontal beam (i.e., start and end Z-coordinates are approximately equal). Store the beam names, their lengths, and their current section properties.
import math

beam_data = []
tolerance = 1e-3 # Tolerance for Z-coordinate comparison (in feet)

for frame_ID in frame_ID_tuple:
    # Get the names of the two point objects (joints) at the ends of the frame.
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

    # Get the global Cartesian coordinates (X, Y, Z) for the first point.
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

    # Get the global Cartesian coordinates (X, Y, Z) for the second point.
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

    # Calculate the length of the frame object
    length = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2 + (Z2 - Z1)**2)

    # Determine if it is a horizontal beam (Z-coordinates are approximately equal)
    if abs(Z1 - Z2) < tolerance:
        # Retrieve the section property name for the frame object
        section_property, _, ret = SapModel.FrameObj.GetSection(frame_ID)

        # Store the beam name, its length, and its section property
        beam_data.append({
            "name": frame_ID,
            "length": length,
            "section_property": section_property
        })

# Step 5: Iterate through the identified beams and assign the new section properties based on their calculated lengths: assign 'B12x18' to beams with length less than or equal to 15 feet, 'B18x24' to beams with length greater than 15 feet and less than or equal to 25 feet, and 'B24x30' to beams with length greater than 25 feet.
for beam in beam_data:
    beam_name = beam["name"]
    beam_length = beam["length"]

    new_section_property = ""
    if beam_length <= 15:
        new_section_property = "B12x18"
    elif beam_length > 15 and beam_length <= 25:
        new_section_property = "B18x24"
    else:
        new_section_property = "B24x30"

    # Assign the new section property to the beam
    ret_code = SapModel.FrameObj.SetSection(beam_name, new_section_property)

# Step 6: Retrieve the names of all stories (floors) in the model.
num_of_stories, story_names_tuple, ret_code = SapModel.Story.GetNameList()

# Step 7: For each story, retrieve the names of all frame objects on that story. Then, for each frame object, determine if it is a beam by checking its end point coordinates. For each identified beam on the story, retrieve its assigned frame section property. Compile a count of each unique beam section property used on that specific story.
story_beam_section_counts = {}

for story_name in story_names_tuple:
    beam_section_counts = {}
    # Get all frame objects on the current story
    frame_obj_num_on_story, frame_ID_tuple_on_story, ret_code = SapModel.FrameObj.GetNameListOnStory(story_name)

    for frame_ID in frame_ID_tuple_on_story:
        # Get the names of the two point objects (joints) at the ends of the frame.
        point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)

        # Get the global Cartesian coordinates (X, Y, Z) for the first point.
        X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)

        # Get the global Cartesian coordinates (X, Y, Z) for the second point.
        X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

        # Determine if it is a horizontal beam (Z-coordinates are approximately equal)
        if abs(Z1 - Z2) < tolerance:
            # Retrieve the section property name for the frame object
            section_property, _, ret = SapModel.FrameObj.GetSection(frame_ID)

            # Increment the count for this section property
            beam_section_counts[section_property] = beam_section_counts.get(section_property, 0) + 1
    
    story_beam_section_counts[story_name] = beam_section_counts

# Step 8: Generate and display a summary report showing the usage of each beam section property for every floor, including the count of each section type per floor.
print("\n--- Beam Section Usage Report Per Floor ---")
for story_name, beam_section_counts in story_beam_section_counts.items():
    print(f"\nStory: {story_name}")
    if beam_section_counts:
        for section_property, count in beam_section_counts.items():
            print(f"  Section: {section_property}, Count: {count}")
    else:
        print("  No beams found on this story.")