"""
Generated ETABS Script
Description: Generate an inventory of all concrete frame sections, including their width, height, and reinforcement details.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-10 21:31:25
Steps: 2
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve a list of all defined frame section property names in the ETABS model.
num_frame_sections, frame_section_names, ret = SapModel.PropFrame.GetNameList()

# Step 2: For each retrieved frame section name, attempt to get its properties as a rectangular section. If successful, retrieve the material name associated with it. Then, check if the material is concrete. If it is a concrete rectangular section, extract its width, height (depth), and attempt to retrieve both beam and column reinforcement details.
concrete_rectangular_sections_data = []

for section_name in frame_section_names:
    is_concrete_section = False
    beam_rebar_details = None
    column_rebar_details = None
    
    MatPropLong_beam, MatPropConfine_beam, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret_beam = SapModel.PropFrame.GetRebarBeam(section_name)
    if ret_beam == 0:
        is_concrete_section = True
        beam_rebar_details = {
            "MatPropLong": MatPropLong_beam,
            "MatPropConfine": MatPropConfine_beam,
            "CoverTop": CoverTop,
            "CoverBot": CoverBot,
            "TopLeftArea": TopLeftArea,
            "TopRightArea": TopRightArea,
            "BotLeftArea": BotLeftArea,
            "BotRightArea": BotRightArea
        }

    MatPropLong_col, MatPropConfine_col, Pattern, ConfineType, Cover, NumberCBars, NumberR3Bars, NumberR2Bars, RebarSize, TieSize, TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, ToBeDesigned, ret_col = SapModel.PropFrame.GetRebarColumn(section_name)
    if ret_col == 0:
        is_concrete_section = True
        column_rebar_details = {
            "MatPropLong": MatPropLong_col,
            "MatPropConfine": MatPropConfine_col,
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

    if is_concrete_section:
        section_material_name = None
        section_width = None
        section_height = None

        concrete_rectangular_sections_data.append({
            "SectionName": section_name,
            "MaterialName": section_material_name,
            "Width": section_width,
            "Height": section_height,
            "BeamRebar": beam_rebar_details,
            "ColumnRebar": column_rebar_details
        })