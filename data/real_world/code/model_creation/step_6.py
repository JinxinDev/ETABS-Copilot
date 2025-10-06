#etabs: Generate ASCE 7 combinations: 1.4SD; 1.2SD+1.6LL; 1.2SD+1.0LL; 0.9SD.


import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Step 1: Check if a load pattern named "SD" exists in the model. If it does not exist, add a new load pattern named "SD" with a type of "Dead".
num_of_load_patterns, load_pattern_tuple, ret = SapModel.LoadPatterns.GetNameList()
if "SD" not in load_pattern_tuple:
    SapModel.LoadPatterns.Add("SD", 1, 0.0, True)
    print("Load pattern 'SD' (Superimposed Dead) added successfully.")
else:
    print("Load pattern 'SD' already exists.")

# Step 2: Check if a load pattern named "LL" exists in the model. If it does not exist, add a new load pattern named "LL" with a type of "Live".
num_of_load_patterns, load_pattern_tuple, ret = SapModel.LoadPatterns.GetNameList()
if "LL" not in load_pattern_tuple:
    SapModel.LoadPatterns.Add("LL", 3, 0.0, True)
    print("Load pattern 'LL' (Live Load) added successfully.")
else:
    print("Load pattern 'LL' already exists.")

# Step 3: Add a new load combination named "ASCE7-1.4SD" of type "Linear Add". Include the load case "SD" with a scale factor of 1.4.
combo_name_1 = "ASCE7-1.4SD"
SapModel.RespCombo.Add(combo_name_1, 0)
SapModel.RespCombo.SetCaseList_1(combo_name_1, 0, "SD", 0, 1.4)
print(f"Load combination '{combo_name_1}' added successfully.")

# Step 4: Add a new load combination named "ASCE7-1.2SD+1.6LL" of type "Linear Add". Include the load case "SD" with a scale factor of 1.2 and the load case "LL" with a scale factor of 1.6.
combo_name_2 = "ASCE7-1.2SD+1.6LL"
SapModel.RespCombo.Add(combo_name_2, 0)
SapModel.RespCombo.SetCaseList_1(combo_name_2, 0, "SD", 0, 1.2)
SapModel.RespCombo.SetCaseList_1(combo_name_2, 0, "LL", 0, 1.6)
print(f"Load combination '{combo_name_2}' added successfully.")

# Step 5: Add a new load combination named "ASCE7-1.2SD+1.0LL" of type "Linear Add". Include the load case "SD" with a scale factor of 1.2 and the load case "LL" with a scale factor of 1.0.
combo_name_3 = "ASCE7-1.2SD+1.0LL"
SapModel.RespCombo.Add(combo_name_3, 0)
SapModel.RespCombo.SetCaseList_1(combo_name_3, 0, "SD", 0, 1.2)
SapModel.RespCombo.SetCaseList_1(combo_name_3, 0, "LL", 0, 1.0)
print(f"Load combination '{combo_name_3}' added successfully.")

# Step 6: Add a new load combination named "ASCE7-0.9SD" of type "Linear Add". Include the load case "SD" with a scale factor of 0.9.
combo_name_4 = "ASCE7-0.9SD"
SapModel.RespCombo.Add(combo_name_4, 0)
SapModel.RespCombo.SetCaseList_1(combo_name_4, 0, "SD", 0, 0.9)
print(f"Load combination '{combo_name_4}' added successfully.")


