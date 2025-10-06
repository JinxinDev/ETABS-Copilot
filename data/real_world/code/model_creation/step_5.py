#etabs: Apply superimposed dead load of 25 psf on floor slabs at stories 2, 3, and 4. Apply superimposed dead load of 20 psf on the story5. Apply live load of 50 psf on floor slabs at stories 2, 3, and 4. Apply live load of 20 psf on the story 5.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Ensure a load pattern named 'SD' (Superimposed Dead) exists. If not, add a new load pattern of type 'Super Dead' with a self-weight multiplier of 1.
load_pattern_name = "SD"
num_of_load_patterns, load_pattern_tuple, ret = SapModel.LoadPatterns.GetNameList()

if load_pattern_name not in load_pattern_tuple:
    SapModel.LoadPatterns.Add(load_pattern_name, 2, 1.0, True)
    print(f"Load pattern '{load_pattern_name}' added successfully.")
else:
    print(f"Load pattern '{load_pattern_name}' already exists.")

# Step 2: Ensure a load pattern named 'LL' (Live Load) exists. If not, add a new load pattern of type 'Live' with a self-weight multiplier of 0.
load_pattern_name_ll = "LL"
num_of_load_patterns, load_pattern_tuple, ret = SapModel.LoadPatterns.GetNameList()

if load_pattern_name_ll not in load_pattern_tuple:
    SapModel.LoadPatterns.Add(load_pattern_name_ll, 3, 0.0, True)
    print(f"Load pattern '{load_pattern_name_ll}' added successfully.")
else:
    print(f"Load pattern '{load_pattern_name_ll}' already exists.")

# Step 3: Retrieve the names of all area objects (floor slabs) on stories 'Story2', 'Story3', and 'Story4'.
target_stories = ['Story2', 'Story3', 'Story4']
area_objects_by_story = {}

for story_name in target_stories:
    slab_obj_num, slab_ID_tuple, ret = SapModel.AreaObj.GetNameListOnStory(story_name)
    if ret == 0:
        area_objects_by_story[story_name] = list(slab_ID_tuple)
        print(f"Retrieved {slab_obj_num} area objects on story '{story_name}'.")
    else:
        print(f"Error retrieving area objects on story '{story_name}'. Return code: {ret}")

# Step 4: Apply a uniform superimposed dead load of 25 psf to all identified area objects on stories 'Story2', 'Story3', and 'Story4' using the 'SD' load pattern.
# Apply uniform superimposed dead load to area objects.
load_pattern_sd = "SD"
load_value_psf = 25
load_value_ksf = load_value_psf / 1000.0 # Convert psf to ksf

for story_name, area_objects in area_objects_by_story.items():
    for area_obj_name in area_objects:
        ret = SapModel.AreaObj.SetLoadUniform(
            area_obj_name,
            load_pattern_sd,
            load_value_ksf,
            10,
            True,
            "Global",
            0
        )
        if ret == 0:
            print(f"Applied {load_value_psf} psf SD load to area object '{area_obj_name}' on story '{story_name}'.")
        else:
            print(f"Error applying load to area object '{area_obj_name}' on story '{story_name}'. Return code: {ret}")

# Step 5: Retrieve the names of all area objects (floor slabs) on story 'Story5'.
target_story_story5 = 'Story5'
slab_obj_num_story5, slab_ID_tuple_story5, ret = SapModel.AreaObj.GetNameListOnStory(target_story_story5)

if ret == 0:
    area_objects_by_story[target_story_story5] = list(slab_ID_tuple_story5)
    print(f"Retrieved {slab_obj_num_story5} area objects on story '{target_story_story5}'.")
else:
    print(f"Error retrieving area objects on story '{target_story_story5}'. Return code: {ret}")

# Step 6: Apply a uniform superimposed dead load of 20 psf to all identified area objects on story 'Story5' using the 'SD' load pattern.
load_pattern_sd_story5 = "SD"
load_value_psf_story5 = 20
load_value_ksf_story5 = load_value_psf_story5 / 1000.0 # Convert psf to ksf

for area_obj_name in area_objects_by_story[target_story_story5]:
    ret = SapModel.AreaObj.SetLoadUniform(
        area_obj_name,
        load_pattern_sd_story5,
        load_value_ksf_story5,
        10,
        True,
        "Global",
        0
    )
    if ret == 0:
        print(f"Applied {load_value_psf_story5} psf SD load to area object '{area_obj_name}' on story '{target_story_story5}'.")
    else:
        print(f"Error applying load to area object '{area_obj_name}' on story '{target_story_story5}'. Return code: {ret}")

# Step 7: Apply a uniform live load of 50 psf to all identified area objects on stories 'Story2', 'Story3', and 'Story4' using the 'LL' load pattern.
# Step 7: Apply a uniform live load of 50 psf to all identified area objects on stories 'Story2', 'Story3', and 'Story4' using the 'LL' load pattern.
load_pattern_ll = "LL"
load_value_psf_ll = 50
load_value_ksf_ll = load_value_psf_ll / 1000.0 # Convert psf to ksf

target_stories_ll = ['Story2', 'Story3', 'Story4']

for story_name in target_stories_ll:
    if story_name in area_objects_by_story:
        for area_obj_name in area_objects_by_story[story_name]:
            ret = SapModel.AreaObj.SetLoadUniform(
                area_obj_name,
                load_pattern_ll,
                load_value_ksf_ll,
                10,
                True,
                "Global",
                0
            )
            if ret == 0:
                print(f"Applied {load_value_psf_ll} psf LL load to area object '{area_obj_name}' on story '{story_name}'.")
            else:
                print(f"Error applying LL load to area object '{area_obj_name}' on story '{story_name}'. Return code: {ret}")
    else:
        print(f"No area objects found for story '{story_name}' to apply LL load.")

# Step 8: Apply a uniform live load of 20 psf to all identified area objects on story 'Story5' using the 'LL' load pattern.
# Step 8: Apply a uniform live load of 20 psf to all identified area objects on story 'Story5' using the 'LL' load pattern.
load_pattern_ll_story5 = "LL"
load_value_psf_ll_story5 = 20
load_value_ksf_ll_story5 = load_value_psf_ll_story5 / 1000.0 # Convert psf to ksf

if target_story_story5 in area_objects_by_story:
    for area_obj_name in area_objects_by_story[target_story_story5]:
        ret = SapModel.AreaObj.SetLoadUniform(
            area_obj_name,
            load_pattern_ll_story5,
            load_value_ksf_ll_story5,
            10,
            True,
            "Global",
            0
        )
        if ret == 0:
            print(f"Applied {load_value_psf_ll_story5} psf LL load to area object '{area_obj_name}' on story '{target_story_story5}'.")
        else:
            print(f"Error applying LL load to area object '{area_obj_name}' on story '{target_story_story5}'. Return code: {ret}")
else:
    print(f"No area objects found for story '{target_story_story5}' to apply LL load.")

