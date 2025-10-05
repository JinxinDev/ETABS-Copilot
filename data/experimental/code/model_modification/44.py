"""
Generated ETABS Script
Description: Create a 'DEAD' load pattern, assign a self-weight multiplier of 1.0, and then apply a uniform dead load of 50 psf (0.05 ksf) to all slab objects and a distributed dead load of 2.0 kip/ft to all beam objects.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-12 10:48:18
Steps: 8
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Add a new load pattern named 'DEAD' with load type 'Dead'.
SapModel.LoadPatterns.Add("DEAD", 1, 1.0, True)

# Step 2: Set the self-weight multiplier for the 'DEAD' load pattern to 1.0.
SapModel.LoadPatterns.SetSelfWTMultiplier("DEAD", 1.0)

# Step 3: Retrieve the names of all area objects in the model.
area_object_count, area_names_tuple, ret = SapModel.AreaObj.GetNameList()

# Step 4: For each retrieved area object, get its assigned property and determine if it is a slab property. Collect the names of all identified slab objects.
slab_object_names = []
for area_name in area_names_tuple:
    # Get the property assigned to the area object
    prop_name, ret = SapModel.AreaObj.GetProperty(area_name)
    # Attempt to retrieve slab properties for the assigned property name
    # If successful (ret == 0), it means the property is a slab property.
    # We don't need the actual slab data, just the success/failure of the call.
    # The GetSlab method requires multiple return variables, so we use placeholders.
    _, _, _, _, _, _, _, ret_slab = SapModel.PropArea.GetSlab(prop_name)
    
    if ret_slab == 0:
        # If GetSlab succeeded, the property is a slab property, so the area object is a slab.
        slab_object_names.append(area_name)

# Step 5: Apply a uniform dead load of 0.05 ksf to all identified slab objects for the 'DEAD' load pattern.
load_pattern_name = "DEAD"
load_value = 0.05  # 0.05 ksf
direction = 10     # Gravity direction
c_sys = "Global"
replace_existing_loads = True
item_type = 0      # 0 for a single Object

for slab_name in slab_object_names:
    ret = SapModel.AreaObj.SetLoadUniform(
        slab_name,
        load_pattern_name,
        load_value,
        direction,
        replace_existing_loads,
        c_sys,
        item_type
    )

# Step 6: Retrieve the names of all frame objects in the model.
# Step 6: Retrieve the names of all frame objects in the model.
frame_object_count, frame_names_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 7: For each retrieved frame object, get its assigned section property and use rebar data information to differentiate and identify if it is a beam. Collect the names of all identified beam objects.
beam_object_names = []

for frame_name in frame_names_tuple:
    # Get the section property assigned to the frame object
    section_property_name, _, ret = SapModel.FrameObj.GetSection(frame_name)
    
    # Attempt to retrieve beam rebar data for the assigned section property name.
    # If successful (ret_beam == 0), it means the property is a concrete beam section
    # with reinforcement defined, thus the frame object is a beam.
    # We don't need the actual rebar data, just the success/failure of the call.
    # The GetRebarBeam method requires multiple return variables, so we use placeholders.
    _, _, _, _, _, _, _, _, ret_beam = SapModel.PropFrame.GetRebarBeam(
        section_property_name
    )

    #print(section_property_name,ret_beam)
    if ret_beam == 0:
        # If GetRebarBeam succeeded, the property is a beam property, so the frame object is a beam.
        beam_object_names.append(frame_name)

# Step 8: Apply a distributed dead load of 2.0 kip/ft to all identified beam objects for the 'DEAD' load pattern.
# Step 8: Apply a distributed dead load of 2.0 kip/ft to all identified beam objects for the 'DEAD' load pattern.
load_pattern_name = "DEAD"
load_value_distributed = 2.0  # 2.0 kip/ft
load_type = 1                 # 1 for Force per unit length
direction = 10                # Gravity direction
start_dist = 0.0              # Relative distance from I-End
end_dist = 1.0                # Relative distance to J-End
c_sys = "Global"
rel_dist = True               # Distances are relative
replace_existing_loads = True # Replace existing loads
item_type = 0                 # 0 for a single Object

for beam_name in beam_object_names:
    ret = SapModel.FrameObj.SetLoadDistributed(
        beam_name,
        load_pattern_name,
        load_type,
        direction,
        start_dist,
        end_dist,
        load_value_distributed, # Val1
        load_value_distributed, # Val2 (for uniform load)
        c_sys,
        rel_dist,
        replace_existing_loads,
        item_type
    )
    print(ret,beam_name)