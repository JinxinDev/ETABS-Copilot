#etabs: Set all joints in base level as fixed. Assign rigid diaphragm at each story.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Retrieve a list of all story names in the model to identify the base story and prepare for iterating through other stories for diaphragm assignment.
NumberNames, StoryNameTuple, ret = SapModel.Story.GetNameList()

# Step 2: Identify the base story (the story with the lowest elevation). Then, get all point object names in the model and filter them to find those located at the base story's elevation (Z=0).
base_elevation = 0.0
NumberPoints, PointNameTuple, ret = SapModel.PointObj.GetNameList()
base_story_points = []
for point_name in PointNameTuple:
    X, Y, Z, ret = SapModel.PointObj.GetCoordCartesian(point_name)
    if Z == base_elevation:
        base_story_points.append(point_name)

# Step 3: For each identified point object on the base level, assign fixed restraints, meaning all six degrees of freedom (U1, U2, U3, R1, R2, R3) are restrained.
fixed_restraint = [True, True, True, True, True, True]
for point_name in base_story_points:
    ret = SapModel.PointObj.SetRestraint(point_name, fixed_restraint)
    print(ret)

# Step 4: Retrieve the list of all story names again. Iterate through each story, excluding the base story, to prepare for diaphragm assignment.
NumberNames, StoryNameTuple, ret = SapModel.Story.GetNameList()

# Assuming the first story in the list is the base story, as direct story elevation retrieval
# is not available in the provided JIT knowledge for this step to programmatically identify
# the base story name based on its elevation (Z=0).
base_story_name = StoryNameTuple[0]

# Iterate through each story, excluding the base story, to prepare for diaphragm assignment
for story_name in StoryNameTuple:
    if story_name != base_story_name:
        # This block will be used in subsequent steps for diaphragm assignment
        pass

# Step 5: For each story (excluding the base story), define a new rigid diaphragm using a unique name (e.g., 'D_StoryName'). Then, retrieve all area objects on that specific story and assign the newly created rigid diaphragm to them.
for story_name in StoryNameTuple:
    if story_name != base_story_name:
        # Define a new rigid diaphragm for the current story
        diaphragm_name = "D_" + story_name
        ret = SapModel.Diaphragm.SetDiaphragm(diaphragm_name, False) # False for rigid diaphragm
        print(ret)
        # Retrieve all area objects on the current story
        slab_obj_num, slab_ID_tuple, ret = SapModel.AreaObj.GetNameListOnStory(story_name)

        # Assign the newly created rigid diaphragm to each area object on this story
        for slab_name in slab_ID_tuple:
            ret = SapModel.AreaObj.SetDiaphragm(slab_name, diaphragm_name)
            print(ret)

