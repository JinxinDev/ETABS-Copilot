#etabs: Create a rectangular grid with four lines (A-D) in the X-direction at 20-foot spacing and five lines (1-5) in the Y-direction at 20-foot spacing. Story 1 has 15-foot height; stories 2-5 have 12-foot heights.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
SapModel = EtabsObject.SapModel
ret = EtabsObject.ApplicationStart()
ret = SapModel.InitializeNewModel()
ret = SapModel.SetPresentUnits(4)

# Step 1: Create a new grid-only model with 4 grid lines in the X-direction (A-D) at 20-foot spacing and 5 grid lines in the Y-direction (1-5) at 20-foot spacing, and 5 stories.
ret = SapModel.File.NewGridOnly(5, 12.0, 12.0, 4, 5, 20.0, 20.0)

# Step 2: Set the height of Story 1 to 15 feet and stories 2 through 5 to 12 feet.
base_elevation = 0.0
num_stories = 5
in_story_names = ["Story1", "Story2", "Story3", "Story4", "Story5"]
in_story_heights = [15.0, 12.0, 12.0, 12.0, 12.0]
in_is_master_story = [False, False, False, False, True]
in_similar_to_story = ["Story5", "Story5", "Story5", "Story5", "None"]
in_splice_above = [False, False, False, False, False]
in_splice_height = [0.0, 0.0, 0.0, 0.0, 0.0]
in_color = [0, 0, 0, 0, 0]

(
    story_names_out,
    story_heights_out,
    is_master_story_out,
    similar_to_story_out,
    splice_above_out,
    splice_height_out,
    color_out,
    ret,
) = SapModel.Story.SetStories_2(base_elevation, num_stories, in_story_names, in_story_heights,
    in_is_master_story, in_similar_to_story,
    in_splice_above, in_splice_height, in_color)