#etabs: Define concrete material CONC with 4,000 psi strength. Define rebar material REBAR as Grade 60 with 60 ksi yield strength. Create column sections: C20X20 (20"×20"), C18X18 (18"×18"), C24X24 (24"×24"), and C20X20 (20"×20"). Create beam section B12X24 (12"×24"). Create slab section SLAB5 as 5-inch shell-thin element.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Define a concrete material named 'CONC' with a strength of 4,000 psi by importing it from the US standard material library (ASTM A615, 4000Psi grade).
mat_name_conc, ret_code_conc = SapModel.PropMaterial.AddMaterial("CONC", 2, "United States", "Customary", "f'c 4000 psi")
print(ret_code_conc)
# Step 2: Define a rebar material named 'REBAR' as Grade 60 with 60 ksi yield strength by importing it from the US standard material library (ASTM A615, Grade60 grade).
mat_name_rebar, ret_code_rebar = SapModel.PropMaterial.AddMaterial("REBAR", 6, "United States", "ASTM A615", "Grade 60")
print(ret_code_conc)
# Step 3: Create a rectangular column section named 'C20X20' with dimensions 20 inches by 20 inches, using the 'CONC' material.
section_name_col = "C20X20"
depth_col_ft = 20 / 12.0
width_col_ft = 20 / 12.0
ret_code_col_section = SapModel.PropFrame.SetRectangle(section_name_col, mat_name_conc, depth_col_ft, width_col_ft)
print(ret_code_col_section)
# Step 4: Create a rectangular column section named 'C18X18' with dimensions 18 inches by 18 inches, using the 'CONC' material.
section_name_col_18x18 = "C18X18"
depth_col_18x18_ft = 18 / 12.0
width_col_18x18_ft = 18 / 12.0
ret_code_col_section_18x18 = SapModel.PropFrame.SetRectangle(section_name_col_18x18, mat_name_conc, depth_col_18x18_ft, width_col_18x18_ft)
print(ret_code_col_section_18x18)
# Step 5: Create a rectangular column section named 'C24X24' with dimensions 24 inches by 24 inches, using the 'CONC' material.
section_name_col_24x24 = "C24X24"
depth_col_24x24_ft = 24 / 12.0
width_col_24x24_ft = 24 / 12.0
ret_code_col_section_24x24 = SapModel.PropFrame.SetRectangle(section_name_col_24x24, mat_name_conc, depth_col_24x24_ft, width_col_24x24_ft)
print(ret_code_col_section_24x24)
# Step 6: Create a rectangular column section named 'C20X20' with dimensions 20 inches by 20 inches, using the 'CONC' material.
section_name_col_20x20int = "C20X20"
depth_col_20x20int_ft = 20 / 12.0
width_col_20x20int_ft = 20 / 12.0
ret_code_col_section_20x20int = SapModel.PropFrame.SetRectangle(section_name_col_20x20int, mat_name_conc, depth_col_20x20int_ft, width_col_20x20int_ft)
print(ret_code_col_section_20x20int)
# Step 7: Create a rectangular beam section named 'B12X24' with dimensions 12 inches by 24 inches, using the 'CONC' material.
section_name_beam = "B12X24"
depth_beam_ft = 24 / 12.0
width_beam_ft = 12 / 12.0
ret_code_beam_section = SapModel.PropFrame.SetRectangle(section_name_beam, mat_name_conc, depth_beam_ft, width_beam_ft)
print(ret_code_beam_section)
# Step 8: Create a slab section named 'SLAB5' as a 5-inch thick shell-thin element, using the 'CONC' material.
section_name_slab = "SLAB5"
ESLABTYPE_SLAB = 0
ESHELLTYPE_SHELLTHIN = 1
thickness_slab_ft = 5 / 12.0
ret_code_slab_section = SapModel.PropArea.SetSlab(section_name_slab, ESLABTYPE_SLAB, ESHELLTYPE_SHELLTHIN, mat_name_conc, thickness_slab_ft)
print(ret_code_slab_section)
