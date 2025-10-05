"""
Generated ETABS Script
Description: Generate a report detailing each concrete material's strength and, for each material, list the top 5 columns with the highest axial loads that utilize it.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-18 00:13:52
Steps: 9
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined material properties in the ETABS model.
num_of_material, material_names, ret = SapModel.PropMaterial.GetNameList()

# Step 2: Iterate through all material names to identify concrete materials. For each concrete material, retrieve its basic properties to confirm its type, and then get its specific concrete properties, including its strength (f'c). Store this information.
concrete_materials_data = {}
for material_name in material_names:
    mat_type, color, notes, guid, ret = SapModel.PropMaterial.GetMaterial(material_name)

    if mat_type == 2: # Assuming 2 corresponds to eMatType.Concrete
        concrete_props_tuple = SapModel.PropMaterial.GetOConcrete_1(material_name)
        fc, is_lightweight, fcs_factor, ss_type, ss_hys_type, strain_at_fc, strain_ultimate, final_slope, friction_angle, dilatational_angle, ret_concrete = concrete_props_tuple

        concrete_materials_data[material_name] = {
            "MatType": mat_type,
            "Color": color,
            "Notes": notes,
            "GUID": guid,
            "fc": fc,
            "IsLightweight": is_lightweight,
            "fcs_factor": fcs_factor,
            "SSType": ss_type,
            "SSHysType": ss_hys_type,
            "StrainAtfc": strain_at_fc,
            "StrainUltimate": strain_ultimate,
            "FinalSlope": final_slope,
            "FrictionAngle": friction_angle,
            "DilatationalAngle": dilatational_angle
        }

# Step 3: Retrieve the names of all frame objects defined in the ETABS model.
num_frame_objects, frame_object_names, ret = SapModel.FrameObj.GetNameList()

# Step 4: Retrieve all frame section properties and their associated material names. Additionally, for each frame section property, attempt to retrieve its column rebar data to identify which sections are designated for columns. Store this mapping of section name to material name and column designation.
# Step 4: Retrieve all frame section properties, their associated material names, and identify column sections.
num_section_names, section_names, prop_types, t3_dims, t2_dims, tf_dims, tw_dims, t2b_dims, tfb_dims, ret_all_props = SapModel.PropFrame.GetAllFrameProperties()

frame_section_properties = {}

# Map for property types (from example)
prop_type_map = {
    1: "I",
    2: "Channel",
    3: "T",
    4: "Angle",
    5: "DblAngle",
    6: "Box",
    7: "Pipe",
    8: "Rectangular",
    9: "Circle",
    10: "General"
}

for i in range(num_section_names):
    section_name = section_names[i]
    section_type_code = prop_types[i]
    section_type_name = prop_type_map.get(section_type_code, "Unknown") # Default to "Unknown" if not in map
    
    section_data = {
        "SectionType": section_type_name,
        "GeometricProperties": {
            "Depth_t3": t3_dims[i],
            "Width_t2": t2_dims[i],
            "FlangeThk_tf": tf_dims[i],
            "WebThk_tw": tw_dims[i],
            "T2b": t2b_dims[i],
            "Tfb": tfb_dims[i]
        },
        "IsColumn": False,
        "AssociatedMaterialName": None, # This will be the rebar material for columns, or None if base material not retrievable
        "ColumnRebarData": None
    }

    # Attempt to retrieve column rebar data
    MatPropLong, MatPropConfine, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned, ret_rebar = SapModel.PropFrame.GetRebarColumn(section_name)
    
    if ret_rebar == 0:
        section_data["IsColumn"] = True
        section_data["AssociatedMaterialName"] = MatPropLong # Use longitudinal rebar material as the associated material
        section_data["ColumnRebarData"] = {
            "MatPropLong": MatPropLong,
            "MatPropConfine": MatPropConfine,
            "Pattern": Pattern,
            "ConfineType": ConfineType,
            "Cover": Cover,
            "NumberCBars": NumberCBars,
            "NumberR3Bars": NumberR3Bars,
            "NumberR2Bars": NumberR2Bars,
            "RebarSize": RebarSize,
            "TieSize": TieSize,
            "TieSpacingLongit": TieSpacingLongit,
            "Number2DirTieBars": Number2DirTieBars,
            "Number3DirTieBars": Number3DirTieBars,
            "ToBeDesigned": ToBeDesigned
        }
    
    frame_section_properties[section_name] = section_data

# Step 5: For each frame object, retrieve the name of the frame section property assigned to it. This will link frame objects to their section properties.
frame_object_to_section_map = {}
for frame_obj_name in frame_object_names:
    section_property_name, auto_recalc, ret = SapModel.FrameObj.GetSection(frame_obj_name)
    frame_object_to_section_map[frame_obj_name] = section_property_name

# Step 6: Retrieve the frame forces for all frame objects. This will include axial loads (P) for each frame element. The analysis is assumed to have been run already.
frame_forces_data = {}
ObjectElm = 0 # Specifies that results are for the object itself

for frame_obj_name in frame_object_names:
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
    ) = SapModel.Results.FrameForce(frame_obj_name, ObjectElm)

    if ret == 0 and NumberResults > 0:
        forces_list = []
        for i in range(NumberResults):
            forces_list.append({
                "Object": Obj[i],
                "ObjectStation": ObjSta[i],
                "Element": Elm[i],
                "ElementStation": ElmSta[i],
                "LoadCase": LoadCase[i],
                "StepType": StepType[i],
                "StepNum": StepNum[i],
                "AxialForce_P": P[i],
                "Shear2_V2": V2[i],
                "Shear3_V3": V3[i],
                "Torsion_T": T[i],
                "Moment2_M2": M2[i],
                "Moment3_M3": M3[i]
            })
        frame_forces_data[frame_obj_name] = forces_list
    elif ret != 0:
        print(f"Error retrieving frame forces for object: {frame_obj_name}, Return code: {ret}")


# Step 7: Consolidate the gathered data: Map each frame object to its assigned section property, then to its material, and finally to its maximum axial load. Filter this data to include only columns (based on the column section identification) that use concrete materials. Group these columns by their concrete material.
concrete_columns_by_material = {}

for frame_obj_name in frame_object_names:
    section_property_name = frame_object_to_section_map.get(frame_obj_name)

    if section_property_name and section_property_name in frame_section_properties:
        section_data = frame_section_properties[section_property_name]

        if section_data["IsColumn"]:
            # Retrieve the base material for the section
            base_material_name = None
            section_type_name = section_data["SectionType"]

            # Use specific Get methods to retrieve the base material property for the section
            if section_type_name == "Rectangular":
                _, MatProp, T3, T2, Color, Notes, GUID, ret = SapModel.PropFrame.GetRectangle(section_property_name)
                if ret == 0: base_material_name = MatProp
            elif section_type_name == "Circle":
                MatProp, Diameter, Color, Notes, GUID, ret = SapModel.PropFrame.GetCircle(section_property_name)
                if ret == 0: base_material_name = MatProp
            elif section_type_name == "Pipe":
                MatProp, Diameter, WallThick, Color, Notes, GUID, ret = SapModel.PropFrame.GetPipe(section_property_name)
                if ret == 0: base_material_name = MatProp
            elif section_type_name == "Box":
                MatProp, T3, T2, Tf, Tw, Color, Notes, GUID, ret = SapModel.PropFrame.GetBox(section_property_name)
                if ret == 0: base_material_name = MatProp
            # Note: Other section types (I, Channel, T, Angle, DblAngle, General) are typically steel or more complex
            # and are less commonly used for concrete columns in this context. Only common concrete section types are handled here.

            if base_material_name and base_material_name in concrete_materials_data:
                # This is a concrete column, now find its maximum axial load
                max_axial_load = 0.0
                if frame_obj_name in frame_forces_data:
                    for force_result in frame_forces_data[frame_obj_name]:
                        max_axial_load = max(max_axial_load, abs(force_result["AxialForce_P"]))

                if base_material_name not in concrete_columns_by_material:
                    concrete_columns_by_material[base_material_name] = []

                concrete_columns_by_material[base_material_name].append({
                    "ObjectName": frame_obj_name,
                    "SectionName": section_property_name,
                    "MaxAxialLoad": max_axial_load
                })


# Step 8: For each concrete material group, sort the associated columns by the absolute value of their axial loads in descending order. Select the top 5 columns from each sorted list.
top_5_concrete_columns_by_material = {}

for material_name, columns_list in concrete_columns_by_material.items():
    # Sort columns by MaxAxialLoad in descending order
    sorted_columns = sorted(columns_list, key=lambda x: x["MaxAxialLoad"], reverse=True)
    
    # Select the top 5 columns
    top_5_concrete_columns_by_material[material_name] = sorted_columns[:5]

# Step 9: Generate a formatted report that displays each concrete material's strength and, for each material, lists the names of the top 5 columns with the highest axial loads that use it, along with their respective axial loads.
print("\n--- Top 5 Concrete Columns by Material and Axial Load ---")
for material_name, columns_list in top_5_concrete_columns_by_material.items():
    fc_strength = concrete_materials_data[material_name]["fc"]
    print(f"\nMaterial: {material_name} (f'c = {fc_strength:.2f} ksf)")
    if columns_list:
        for i, column_data in enumerate(columns_list):
            print(f"  {i+1}. Column: {column_data["ObjectName"]}, Max Axial Load: {column_data["MaxAxialLoad"]:.2f} kips")
    else:
        print("  No concrete columns found for this material.")