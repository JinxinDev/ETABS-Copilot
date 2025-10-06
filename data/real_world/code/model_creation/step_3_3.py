#etabs: Draw rectangular slab. The bays per floor have corner coordinates: A1-B2 (0,0 to 20,20), A2-B3 (0,20 to 20,40), A3-B4 (0,40 to 20,60), A4-B5 (0,60 to 20,80), B1-C2 (20,0 to 40,20), B2-C3 (20,20 to 40,40), B3-C4 (20,40 to 40,60), B4-C5 (20,60 to 40,80), C1-D2 (40,0 to 60,20), C2-D3 (40,20 to 60,40), C3-D4 (40,40 to 60,60), and C4-D5 (40,60 to 60,80). Create these slabs on stories 2-5 and the roof level. Assign existing SLAB5 to all slabs.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve the names of all stories in the model to identify the target stories.
NumberNames, StoryNameTuple, ret = SapModel.Story.GetNameList()

# Step 2: Identify the target stories: 'Story2', 'Story3', 'Story4', 'Story5'. For each identified story, retrieve its elevation.
target_stories = ['Story2', 'Story3', 'Story4', 'Story5']
story_elevations = {}

for story_name in StoryNameTuple:
    if story_name in target_stories:
        elevation, ret = SapModel.Story.GetElevation(story_name)
        story_elevations[story_name] = elevation

# Step 3: Define the corner coordinates for each of the 12 rectangular slab bays. The bays are: A1-B2 (0,0 to 20,20), A2-B3 (0,20 to 20,40), A3-B4 (0,40 to 20,60), A4-B5 (0,60 to 20,80), B1-C2 (20,0 to 40,20), B2-C3 (20,20 to 40,40), B3-C4 (20,40 to 40,60), B4-C5 (20,60 to 40,80), C1-D2 (40,0 to 60,20), C2-D3 (40,20 to 60,40), C3-D4 (40,40 to 60,60), and C4-D5 (40,60 to 60,80).
slab_bay_coordinates = [
    {"name": "A1-B2", "coords": [(0, 0), (20, 0), (20, 20), (0, 20)]},
    {"name": "A2-B3", "coords": [(0, 20), (20, 20), (20, 40), (0, 40)]},
    {"name": "A3-B4", "coords": [(0, 40), (20, 40), (20, 60), (0, 60)]},
    {"name": "A4-B5", "coords": [(0, 60), (20, 60), (20, 80), (0, 80)]},
    {"name": "B1-C2", "coords": [(20, 0), (40, 0), (40, 20), (20, 20)]},
    {"name": "B2-C3", "coords": [(20, 20), (40, 20), (40, 40), (20, 40)]},
    {"name": "B3-C4", "coords": [(20, 40), (40, 40), (40, 60), (20, 60)]},
    {"name": "B4-C5", "coords": [(20, 60), (40, 60), (40, 80), (20, 80)]},
    {"name": "C1-D2", "coords": [(40, 0), (60, 0), (60, 20), (40, 20)]},
    {"name": "C2-D3", "coords": [(40, 20), (60, 20), (60, 40), (40, 40)]},
    {"name": "C3-D4", "coords": [(40, 40), (60, 40), (60, 60), (40, 60)]},
    {"name": "C4-D5", "coords": [(40, 60), (60, 60), (60, 80), (40, 80)]}
]

# Step 4: Iterate through each of the target stories ('Story2', 'Story3', 'Story4', 'Story5', 'Roof') and their respective elevations. For each story, iterate through the defined 12 rectangular bay coordinates. For each bay, draw a new rectangular area object (slab) using the bay's X, Y coordinates and the current story's elevation for the Z coordinate. Assign the existing slab property 'SLAB5' to each newly created slab.
for story_name in target_stories:
    elevation = story_elevations[story_name]
    for bay in slab_bay_coordinates:
        bay_name = bay["name"]
        coords = bay["coords"]

        x_coords = [c[0] for c in coords]
        y_coords = [c[1] for c in coords]
        num_points = len(x_coords)
        z_coords = [elevation] * num_points

        # Add the rectangular area object (slab)
        # The first three return values are tuples of the input coordinates, which we don't need to capture explicitly.
        _, _, _, area_name, ret = SapModel.AreaObj.AddByCoord(num_points, x_coords, y_coords, z_coords)

        # Assign the 'SLAB5' property to the newly created slab
        if ret == 0:
            ret = SapModel.AreaObj.SetProperty(area_name, "SLAB5")

