"""
Generated ETABS Script
Description: Retrieve joint forces and internal forces for beam '506' and verify equilibrium.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 00:07:02
Steps: 3
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the joint forces (reactions) at the start and end points of beam '506' for a relevant load case or combination.
ObjectElm = 0
load_case_or_combo = "DEAD" # Assuming 'DEAD' is a relevant load case. Adjust as needed.
(
    NumberResults,
    Obj,
    Elm,
    PointElm,
    LoadCase,
    StepType,
    StepNum,
    F1,
    F2,
    F3,
    M1,
    M2,
    M3,
    ret
) = SapModel.Results.FrameJointForce("506", ObjectElm)

if ret == 0:
    print(f"Successfully retrieved joint forces for beam '506' for load case '{load_case_or_combo}'.")
    for i in range(NumberResults):
        print(f"  Result {i+1}: Object={Obj[i]}, Element={Elm[i]}, PointElm={PointElm[i]}, LoadCase={LoadCase[i]}, F1={F1[i]:.2f}, F2={F2[i]:.2f}, F3={F3[i]:.2f}, M1={M1[i]:.2f}, M2={M2[i]:.2f}, M3={M3[i]:.2f}")
else:
    print(f"Error retrieving joint forces for beam '506'. Return code: {ret}")

# Step 2: Retrieve the internal shear and moment forces for beam '506' at its ends for the same load case or combination.
ObjectElm = 0
(NumberResults_frame_force, Obj_frame_force, ObjSta_frame_force, Elm_frame_force, ElmSta_frame_force, LoadCase_frame_force, StepType_frame_force, StepNum_frame_force, P_frame_force, V2_frame_force, V3_frame_force, T_frame_force, M2_frame_force, M3_frame_force, ret_frame_force) = SapModel.Results.FrameForce("506", ObjectElm)

if ret_frame_force == 0:
    print(f"Successfully retrieved internal forces for beam '506'.")
    print(f"Internal Shear and Moment Forces for beam '506' for load case '{load_case_or_combo}':")
    for i in range(NumberResults_frame_force):
        if LoadCase_frame_force[i] == load_case_or_combo and (ObjSta_frame_force[i] < 0.001 or ObjSta_frame_force[i] > 0.999):
            print(f"  Object={Obj_frame_force[i]}, Element={Elm_frame_force[i]}, Relative Distance={ObjSta_frame_force[i]:.2f}, LoadCase={LoadCase_frame_force[i]}, V2={V2_frame_force[i]:.2f}, V3={V3_frame_force[i]:.2f}, M2={M2_frame_force[i]:.2f}, M3={M3_frame_force[i]:.2f}")
else:
    print(f"Error retrieving internal forces for beam '506'. Return code: {ret_frame_force}")

# Step 3: Perform calculations to compare the retrieved joint forces with the internal shear and moment forces at the beam's ends to verify equilibrium.
# Initialize dictionaries to store extracted forces for comparison
joint_force_start = {}
joint_force_end = {}
internal_force_start = {}
internal_force_end = {}

# Extract FrameJointForce results for the specified load case
if ret == 0:
    results_for_load_case_joint_force = [
        (F2[i], F3[i], M2[i], M3[i], PointElm[i])
        for i in range(NumberResults) if LoadCase[i] == load_case_or_combo
    ]

    if len(results_for_load_case_joint_force) >= 2:
        # ASSUMPTION: The first result corresponds to the start joint and the second to the end joint.
        # The ETABS API documentation does not explicitly guarantee this order when querying by frame object name.
        joint_force_start = {
            'F2': results_for_load_case_joint_force[0][0],
            'F3': results_for_load_case_joint_force[0][1],
            'M2': results_for_load_case_joint_force[0][2],
            'M3': results_for_load_case_joint_force[0][3],
            'JointName': results_for_load_case_joint_force[0][4]
        }
        joint_force_end = {
            'F2': results_for_load_case_joint_force[1][0],
            'F3': results_for_load_case_joint_force[1][1],
            'M2': results_for_load_case_joint_force[1][2],
            'M3': results_for_load_case_joint_force[1][3],
            'JointName': results_for_load_case_joint_force[1][4]
        }
        print(f"Extracted FrameJointForce: Start Joint '{joint_force_start['JointName']}', End Joint '{joint_force_end['JointName']}' for beam '506'.")
    else:
        print("Warning: Could not find enough FrameJointForce results for the specified load case to identify both ends.")
else:
    print("Error: FrameJointForce retrieval failed or returned no results.")

# Extract FrameForce results for the specified load case at beam ends
if ret_frame_force == 0:
    for i in range(NumberResults_frame_force):
        if LoadCase_frame_force[i] == load_case_or_combo:
            if ObjSta_frame_force[i] < 0.001: # Start of beam (relative distance approximately 0)
                internal_force_start = {
                    'V2': V2_frame_force[i],
                    'V3': V3_frame_force[i],
                    'M2': M2_frame_force[i],
                    'M3': M3_frame_force[i]
                }
            elif ObjSta_frame_force[i] > 0.999: # End of beam (relative distance approximately 1)
                internal_force_end = {
                    'V2': V2_frame_force[i],
                    'V3': V3_frame_force[i],
                    'M2': M2_frame_force[i],
                    'M3': M3_frame_force[i]
                }
    if internal_force_start and internal_force_end:
        print("Extracted FrameForce: Internal forces at start and end of beam '506'.")
    else:
        print("Warning: Could not find internal forces at both ends of beam '506' for the specified load case.")
else:
    print("Error: FrameForce retrieval failed or returned no results.")

# Perform comparison if all necessary data is available
if joint_force_start and joint_force_end and internal_force_start and internal_force_end:
    tolerance = 0.01 # Define a tolerance for numerical comparison (e.g., 0.01 kips or kip-ft)

    print("\n--- Equilibrium Check for Beam '506' ---")

    # Start Joint Comparison
    print(f"\nAt Start Joint ({joint_force_start['JointName']}):")
    # Joint forces (F2, F3, M2, M3) are reactions exerted by the beam on the joint.
    # Internal forces (V2, V3, M2, M3) are within the beam. At the start, they should be opposite.
    diff_F2_start = abs(joint_force_start['F2'] - (-internal_force_start['V2']))
    status_F2_start = "MATCH" if diff_F2_start < tolerance else "MISMATCH"
    print(f"  Joint F2: {joint_force_start['F2']:.2f} vs Internal V2: {-internal_force_start['V2']:.2f} (Difference: {diff_F2_start:.2f}) - {status_F2_start}")

    diff_F3_start = abs(joint_force_start['F3'] - (-internal_force_start['V3']))
    status_F3_start = "MATCH" if diff_F3_start < tolerance else "MISMATCH"
    print(f"  Joint F3: {joint_force_start['F3']:.2f} vs Internal V3: {-internal_force_start['V3']:.2f} (Difference: {diff_F3_start:.2f}) - {status_F3_start}")

    diff_M2_start = abs(joint_force_start['M2'] - (-internal_force_start['M2']))
    status_M2_start = "MATCH" if diff_M2_start < tolerance else "MISMATCH"
    print(f"  Joint M2: {joint_force_start['M2']:.2f} vs Internal M2: {-internal_force_start['M2']:.2f} (Difference: {diff_M2_start:.2f}) - {status_M2_start}")

    diff_M3_start = abs(joint_force_start['M3'] - (-internal_force_start['M3']))
    status_M3_start = "MATCH" if diff_M3_start < tolerance else "MISMATCH"
    print(f"  Joint M3: {joint_force_start['M3']:.2f} vs Internal M3: {-internal_force_start['M3']:.2f} (Difference: {diff_M3_start:.2f}) - {status_M3_start}")

    # End Joint Comparison
    print(f"\nAt End Joint ({joint_force_end['JointName']}):")
    # At the end, internal forces and joint reactions should be in the same direction for equilibrium.
    diff_F2_end = abs(joint_force_end['F2'] - internal_force_end['V2'])
    status_F2_end = "MATCH" if diff_F2_end < tolerance else "MISMATCH"
    print(f"  Joint F2: {joint_force_end['F2']:.2f} vs Internal V2: {internal_force_end['V2']:.2f} (Difference: {diff_F2_end:.2f}) - {status_F2_end}")

    diff_F3_end = abs(joint_force_end['F3'] - internal_force_end['V3'])
    status_F3_end = "MATCH" if diff_F3_end < tolerance else "MISMATCH"
    print(f"  Joint F3: {joint_force_end['F3']:.2f} vs Internal V3: {internal_force_end['V3']:.2f} (Difference: {diff_F3_end:.2f}) - {status_F3_end}")

    diff_M2_end = abs(joint_force_end['M2'] - internal_force_end['M2'])
    status_M2_end = "MATCH" if diff_M2_end < tolerance else "MISMATCH"
    print(f"  Joint M2: {joint_force_end['M2']:.2f} vs Internal M2: {internal_force_end['M2']:.2f} (Difference: {diff_M2_end:.2f}) - {status_M2_end}")

    diff_M3_end = abs(joint_force_end['M3'] - internal_force_end['M3'])
    status_M3_end = "MATCH" if diff_M3_end < tolerance else "MISMATCH"
    print(f"  Joint M3: {joint_force_end['M3']:.2f} vs Internal M3: {internal_force_end['M3']:.2f} (Difference: {diff_M3_end:.2f}) - {status_M3_end}")

    print("\nEquilibrium check complete.")
else:
    print("\nSkipping equilibrium check: Not all required force data was retrieved successfully.")