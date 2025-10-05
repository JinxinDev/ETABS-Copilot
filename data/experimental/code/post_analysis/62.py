"""
Generated ETABS Script
Description: Extract maximum positive and negative moments for all beams on Story 2, identify their governing load combinations, and list beams that exceed 80% of their moment capacity.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-16 22:25:46
Steps: 5
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all frame objects on 'Story 2' and filter them to identify only beam elements.
story_name = "Story2"
frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story_name)

beam_elements = []

for frame_ID in frame_ID_tuple:
    point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
    X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
    X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)
    #print(X1,X2,Y1,Y2)
    # Classify as beam if it's not a column (i.e., X or Y coordinates differ)
    if not (X1 == X2 and Y1 == Y2):
        beam_elements.append(frame_ID)

# Step 2: For each identified beam on 'Story 2', iterate through all defined load combinations (assuming these are known or provided) and extract the frame forces, specifically the M2 and M3 moments, at various locations along the beam.
beam_forces_data = {}
ObjectElm = 0 # Specifies that results are for the object, not elements or groups

for beam_ID in beam_elements:
    (
        NumberResults,
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
        ret
    ) = SapModel.Results.FrameForce(beam_ID, ObjectElm)
    if ret == 0:
        beam_forces_data[beam_ID] = {}
        for i in range(NumberResults):
            current_load_case = LoadCase[i]
            current_obj_sta = ObjSta[i]
            current_m2 = M2[i]
            current_m3 = M3[i]

            if current_load_case not in beam_forces_data[beam_ID]:
                beam_forces_data[beam_ID][current_load_case] = []

            beam_forces_data[beam_ID][current_load_case].append({
                'ObjSta': current_obj_sta,
                'M2': current_m2,
                'M3': current_m3
            })
    else:
        print(f"Error retrieving frame forces for beam: {beam_ID}, Return code: {ret}")

# Step 3: Process the extracted M2 and M3 moment results for each beam across all load combinations to determine the maximum positive and negative moments, and identify the specific load combination that governs each of these extreme values.
processed_beam_moments = {}

for beam_ID, load_case_data in beam_forces_data.items():
    max_M2_pos = {'value': -float('inf'), 'load_case': None}
    max_M2_neg = {'value': float('inf'), 'load_case': None}
    max_M3_pos = {'value': -float('inf'), 'load_case': None}
    max_M3_neg = {'value': float('inf'), 'load_case': None}

    for load_case, results_list in load_case_data.items():
        for result in results_list:
            m2 = result['M2']
            m3 = result['M3']

            # Process M2 moments
            if m2 > max_M2_pos['value']:
                max_M2_pos['value'] = m2
                max_M2_pos['load_case'] = load_case
            if m2 < max_M2_neg['value']:
                max_M2_neg['value'] = m2
                max_M2_neg['load_case'] = load_case

            # Process M3 moments
            if m3 > max_M3_pos['value']:
                max_M3_pos['value'] = m3
                max_M3_pos['load_case'] = load_case
            if m3 < max_M3_neg['value']:
                max_M3_neg['value'] = m3
                max_M3_neg['load_case'] = load_case

    processed_beam_moments[beam_ID] = {
        'M2_max_pos': max_M2_pos,
        'M2_max_neg': max_M2_neg,
        'M3_max_pos': max_M3_pos,
        'M3_max_neg': max_M3_neg
    }

# Step 4: For each beam, retrieve its assigned frame section property name, then get the detailed section properties (e.g., dimensions, material name, assuming a rectangular section for demonstration) and the associated rebar data. Also, retrieve the material properties for the concrete used in the beam section.
beam_properties_data = {}

for beam_ID in beam_elements:
    # 1. Retrieve the assigned frame section property name
    section_property_name, _, ret = SapModel.FrameObj.GetSection(beam_ID)
    if ret != 0:
        print(f"Error retrieving section property for beam {beam_ID}: {ret}")
        continue

    # 2. Get detailed section properties (assuming rectangular section)
    # FileName, MatProp, T3, T2, Color, Notes, GUID, ret
    _, concrete_mat_prop_name, T3, T2, _, _, _, ret = SapModel.PropFrame.GetRectangle(section_property_name)
    if ret != 0:
        print(f"Error retrieving rectangular section properties for {section_property_name}: {ret}")
        continue

    # 3. Get beam reinforcement data
    # MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret
    (long_rebar_mat_prop_name, confine_rebar_mat_prop_name, 
     cover_top, cover_bot, top_left_area, top_right_area, 
     bot_left_area, bot_right_area, ret) = SapModel.PropFrame.GetRebarBeam(section_property_name)
    if ret != 0:
        print(f"Error retrieving rebar beam data for {section_property_name}: {ret}")
        # Continue even if rebar data is not found, as other properties might still be valid

    # 4. Retrieve material properties for concrete
    # fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ret
    concrete_props = SapModel.PropMaterial.GetOConcrete_1(concrete_mat_prop_name)
    if concrete_props[-1] != 0:
        print(f"Error retrieving concrete properties for material {concrete_mat_prop_name}: {concrete_props[-1]}")
        concrete_props = None # Indicate error

    # 5. Retrieve material properties for longitudinal rebar
    # Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainUltimate, FinalSlope, UseCaltransSSDefaults, ret
    long_rebar_props = SapModel.PropMaterial.GetORebar_1(long_rebar_mat_prop_name)
    if long_rebar_props[-1] != 0:
        print(f"Error retrieving longitudinal rebar properties for material {long_rebar_mat_prop_name}: {long_rebar_props[-1]}")
        long_rebar_props = None # Indicate error

    # 6. Retrieve material properties for confinement rebar
    confine_rebar_props = SapModel.PropMaterial.GetORebar_1(confine_rebar_mat_prop_name)
    if confine_rebar_props[-1] != 0:
        print(f"Error retrieving confinement rebar properties for material {confine_rebar_mat_prop_name}: {confine_rebar_props[-1]}")
        confine_rebar_props = None # Indicate error

    beam_properties_data[beam_ID] = {
        'SectionName': section_property_name,
        'Dimensions': {
            'Depth_T3': T3,
            'Width_T2': T2
        },
        'ConcreteMaterial': {
            'Name': concrete_mat_prop_name,
            'Properties': concrete_props[:-1] if concrete_props else None # Exclude return code
        },
        'RebarData': {
            'LongitudinalMaterialName': long_rebar_mat_prop_name,
            'ConfinementMaterialName': confine_rebar_mat_prop_name,
            'CoverTop': cover_top,
            'CoverBottom': cover_bot,
            'TopLeftArea': top_left_area,
            'TopRightArea': top_right_area,
            'BottomLeftArea': bot_left_area,
            'BottomRightArea': bot_right_area
        },
        'LongitudinalRebarMaterial': {
            'Name': long_rebar_mat_prop_name,
            'Properties': long_rebar_props[:-1] if long_rebar_props else None # Exclude return code
        },
        'ConfinementRebarMaterial': {
            'Name': confine_rebar_mat_prop_name,
            'Properties': confine_rebar_props[:-1] if confine_rebar_props else None # Exclude return code
        }
    }
print(processed_beam_moments)
# Step 5: Calculate the moment capacity (Mn) for each beam using the retrieved section dimensions, material properties, and rebar data. Then, compare the previously determined maximum positive and negative moments against 80% of this calculated moment capacity. Finally, list the names of all beams on 'Story 2' where either the maximum positive or negative moment exceeds 80% of their respective moment capacity.
calculated_beam_capacities = {}
non_compliant_beams = []
capacity_check_ratio = 0.80

for beam_ID in beam_elements:
    beam_props = beam_properties_data.get(beam_ID)
    if not beam_props:
        continue

    h = beam_props['Dimensions']['Depth_T3']
    b = beam_props['Dimensions']['Width_T2']

    concrete_props_tuple = beam_props['ConcreteMaterial']['Properties']
    long_rebar_props_tuple = beam_props['LongitudinalRebarMaterial']['Properties']

    if not concrete_props_tuple or not long_rebar_props_tuple:
        continue

    fc = concrete_props_tuple[0]
    Fy = long_rebar_props_tuple[0]

    if fc <= 0 or Fy <= 0 or h <= 0 or b <= 0:
        continue

    cover_top = beam_props['RebarData']['CoverTop']
    cover_bot = beam_props['RebarData']['CoverBottom']
    As_top_total = beam_props['RebarData']['TopLeftArea'] + beam_props['RebarData']['TopRightArea']
    As_bot_total = beam_props['RebarData']['BottomLeftArea'] + beam_props['RebarData']['BottomRightArea']

    d_for_pos_moment = h - cover_bot
    d_for_neg_moment = h - cover_top

    if d_for_pos_moment <= 0 or d_for_pos_moment > h or d_for_neg_moment <= 0 or d_for_neg_moment > h:
        continue

    Mn_pos = 0.0
    if As_bot_total > 0:
        a_pos = (As_bot_total * Fy) / (0.85 * fc * b)
        Mn_pos = As_bot_total * Fy * (d_for_pos_moment - a_pos / 2)
        Mn_pos = max(0.0, Mn_pos)

    Mn_neg = 0.0
    if As_top_total > 0:
        a_neg = (As_top_total * Fy) / (0.85 * fc * b)
        Mn_neg = As_top_total * Fy * (d_for_neg_moment - a_neg / 2)
        Mn_neg = max(0.0, Mn_neg)

    calculated_beam_capacities[beam_ID] = {
        'Mn_pos': Mn_pos,
        'Mn_neg': Mn_neg
    }

    demand_moments = processed_beam_moments.get(beam_ID)
    if not demand_moments:
        continue

    max_M2_pos_demand = abs(demand_moments['M2_max_pos']['value'])
    max_M2_neg_demand = abs(demand_moments['M2_max_neg']['value'])
    max_M3_pos_demand = abs(demand_moments['M3_max_pos']['value'])
    max_M3_neg_demand = abs(demand_moments['M3_max_neg']['value'])

    is_beam_non_compliant = False

    if Mn_pos > 0:
        if max_M2_pos_demand > capacity_check_ratio * Mn_pos or \
           max_M3_pos_demand > capacity_check_ratio * Mn_pos:
            is_beam_non_compliant = True
    elif max_M2_pos_demand > 0 or max_M3_pos_demand > 0:
        is_beam_non_compliant = True

    if Mn_neg > 0:
        if max_M2_neg_demand > capacity_check_ratio * Mn_neg or \
           max_M3_neg_demand > capacity_check_ratio * Mn_neg:
            is_beam_non_compliant = True
    elif max_M2_neg_demand > 0 or max_M3_neg_demand > 0:
        is_beam_non_compliant = True

    if is_beam_non_compliant:
        non_compliant_beams.append(beam_ID)
        print(non_compliant_beams)