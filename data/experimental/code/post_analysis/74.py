"""
Generated ETABS Script
Description: Identify the column with the highest axial load in the model, then report its corresponding maximum lateral displacement at the top story.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-17 19:33:38
Steps: 7
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all stories in the model to identify the top story.
number_of_stories, story_names, ret = SapModel.Story.GetNameList()

# Step 2: Retrieve the names of all frame objects in the model.
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameList()

# Step 3: For each frame object, determine if it is a column by checking its connectivity points' Z-coordinates. Then, retrieve the axial forces for all identified columns for all load cases/combinations.
column_names = []
for frame_ID in frame_ID_tuple:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)
    
    # A small tolerance to account for potential floating point inaccuracies or very slight slopes
    if abs(Z1 - Z2) > 0.01: # Assuming a difference greater than 0.01 ft indicates a vertical/sloped element (column)
        column_names.append(frame_ID)

column_axial_forces = {}
ObjectElm = 0 # Get results for the object itself

for column_name in column_names:
    (NumberResults, 
     Obj, 
     ObjSta, 
     Elm, 
     ElmSta, 
     LoadCase, 
     StepType, 
     StepNum, 
     P, 
     V2, 
     V3, 
     T, 
     M2, 
     M3, 
     ret) = SapModel.Results.FrameForce(column_name, ObjectElm)
    
    # Store axial forces for the current column
    column_axial_forces[column_name] = P

# Step 4: Identify the specific column that has the highest absolute axial load among all columns.
max_abs_axial_load = 0.0
column_with_max_load = None

for column_name, axial_forces_list in column_axial_forces.items():
    for axial_force in axial_forces_list:
        abs_axial_force = abs(axial_force)
        if abs_axial_force > max_abs_axial_load:
            max_abs_axial_load = abs_axial_force
            column_with_max_load = column_name

# Step 5: For the identified column with the highest axial load, retrieve the name of the point object at its top end (on the top story).
point_1, point_2, ret = SapModel.FrameObj.GetPoints(column_with_max_load)
X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)

if Z1 > Z2:
    top_end_point_name = point_1
else:
    top_end_point_name = point_2

# Step 6: Retrieve the joint displacements (Ux, Uy, Uz) for the top point of the identified column for all load cases/combinations.
ObjectElm = 0
(NumberResults,
 Obj,
 Elm,
 LoadCase,
 StepType,
 StepNum,
 U1,
 U2,
 U3,
 R1,
 R2,
 R3,
 ret) = SapModel.Results.JointDispl(top_end_point_name, ObjectElm)

top_point_displacements = {
    "U1": U1,
    "U2": U2,
    "U3": U3,
    "LoadCase": LoadCase,
    "StepType": StepType,
    "StepNum": StepNum
}
print(top_end_point_name)
# Step 7: From the retrieved joint displacements, calculate and report the maximum absolute lateral displacement (maximum of absolute Ux and Uy) at the top point of the column with the highest axial load.
max_abs_lateral_displacement = 0.0
#print(top_point_displacements)
# U1 corresponds to Ux, U2 corresponds to Uy
for i in range(len(top_point_displacements["U1"])):
    current_ux = top_point_displacements["U1"][i]
    current_uy = top_point_displacements["U2"][i]
    print(current_ux,current_uy)
    
    abs_ux = abs(current_ux)
    abs_uy = abs(current_uy)
    
    current_max_lateral = max(abs_ux, abs_uy)
    
    if current_max_lateral > max_abs_lateral_displacement:
        max_abs_lateral_displacement = current_max_lateral
