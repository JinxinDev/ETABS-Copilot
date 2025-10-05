"""
Generated ETABS Script
Description: A plan to identify and list all beam sections in the ETABS model that have a longitudinal top reinforcement area exceeding 5 square inches.
Session Mode: CONNECT_EXISTING
Generated: 2025-09-13 17:45:27
Steps: 4
"""

import comtypes.client

print("Connecting to ETABS...")
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel
# Note: Current model units are assumed to be kip_ft_F
print("ETABS connection established")

# Step 1: Retrieve the names of all defined frame section properties that are classified as beam sections.
# Define which property types are considered "beam sections" based on common structural shapes
# The numerical codes are derived from the prop_type_map shown in the knowledge graph example for GetAllFrameProperties.
# 1: "I", 2: "Channel", 6: "Box", 7: "Pipe", 8: "Rectangular", 9: "Circle"
beam_type_codes = [
    1, # I-section
    2, # Channel section
    6, # Box section
    7, # Pipe section
    8, # Rectangular section
    9  # Circle section
]

# Call the function to get all frame property definitions
# The return values include the number of names, a tuple of names, a tuple of property types, and other section data.
num_names, all_section_names, prop_types, t3, t2, tf, tw, t2b, tfb, ret = SapModel.PropFrame.GetAllFrameProperties()

# Initialize a list to store the names of beam sections
beam_section_names = []

# Iterate through all frame sections and filter for beam types
for i in range(num_names):
    section_name = all_section_names[i]
    section_type_code = prop_types[i]
    
    if section_type_code in beam_type_codes:
        beam_section_names.append(section_name)
# The 'beam_section_names' list now contains the names of all defined frame sections classified as beams.

# Step 2: For each retrieved beam section property name, get its detailed beam rebar data, which includes the longitudinal top reinforcement area.
# Initialize a list to store rebar data for each beam section
beam_rebar_data = []

# Iterate through each identified beam section name
for beam_section_name in beam_section_names:
    # Retrieve beam reinforcement data for the current section
    # Using positional arguments as per constraint
    MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, TopRightArea, BotLeftArea, BotRightArea, ret = SapModel.PropFrame.GetRebarBeam(beam_section_name)
    
    # Check if the API call was successful (ret == 0)
    if ret == 0:
        # Store the retrieved data in a dictionary
        section_rebar_details = {
            "SectionName": beam_section_name,
            "LongitudinalMaterial": MatPropLong,
            "ConfinementMaterial": MatPropConfine,
            "CoverTop": CoverTop, # [L] - feet
            "CoverBottom": CoverBot, # [L] - feet
            "TopLeftArea": TopLeftArea, # [L^2] - sq ft
            "TopRightArea": TopRightArea, # [L^2] - sq ft
            "BottomLeftArea": BotLeftArea, # [L^2] - sq ft
            "BottomRightArea": BotRightArea # [L^2] - sq ft
        }
        beam_rebar_data.append(section_rebar_details)
    else:
        # Handle cases where rebar data could not be retrieved (e.g., not a concrete beam or no rebar defined)
        print(f"Warning: Could not retrieve rebar data for beam section '{beam_section_name}'. Return code: {ret}")

# The 'beam_rebar_data' list now contains dictionaries, each with detailed rebar information for a beam section.

# Step 3: Evaluate the retrieved longitudinal top reinforcement area for each beam section. If this area is greater than 5 square inches, add the beam section's name to a list of qualifying sections.
# Step 3: Evaluate the retrieved longitudinal top reinforcement area for each beam section.
# Initialize a list to store the names of beam sections that meet the criteria.
qualifying_beam_sections = []

# Define the threshold for top reinforcement area in square inches.
# The ETABS model uses feet for length, so convert 5 sq inches to sq feet.
threshold_area_sq_inches = 5.0
# 1 foot = 12 inches, so 1 sq ft = 144 sq inches
threshold_area_sq_feet = threshold_area_sq_inches / 144.0

# Iterate through the rebar data for each beam section.
for section_data in beam_rebar_data:
    section_name = section_data["SectionName"]
    top_left_area = section_data["TopLeftArea"]
    top_right_area = section_data["TopRightArea"]
    
    # Check if either the top-left or top-right reinforcement area exceeds the threshold.
    if top_left_area > threshold_area_sq_feet or top_right_area > threshold_area_sq_feet:
        qualifying_beam_sections.append(section_name)

# The 'qualifying_beam_sections' list now contains the names of beam sections
# where the longitudinal top reinforcement area is greater than 5 square inches.

# Step 4: Output the final list of beam sections that use more than 5 square inches of longitudinal top reinforcement.
# Output the final list of qualifying beam sections.
print("Beam sections with longitudinal top reinforcement area > 5 sq inches:")
for section_name in qualifying_beam_sections:
    print(f"- {section_name}")

# The 'qualifying_beam_sections' list has been printed to the console.