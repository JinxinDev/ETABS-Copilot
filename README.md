# ETABS Copilot - AI-Powered Structural Engineering Code Generator

A VS Code extension that revolutionizes ETABS structural modeling by combining specialized AI agents with GitHub Copilot for intelligent code generation and enhancement.

## Overview

ETABS Copilot bridges the gap between natural language descriptions and production-ready ETABS API code. The extension generates clean, functional ETABS scripts while creating domain-specific knowledge files that enable GitHub Copilot to provide contextually-aware code enhancements.

## Key Features

### 🚀 Intelligent Code Generation
- **Natural Language Input**: Transform comments like `# etabs: create steel frame building` into complete ETABS scripts
- **Domain-Specific AI**: Leverages specialized agents trained on structural engineering knowledge
- **Clean Output**: Generates production-ready ETABS code without embedded comments or clutter

### 🤖 GitHub Copilot Integration  
- **Domain Knowledge Injection**: Automatically creates `.etabs-knowledge.md` files with architectural context
- **Enhanced Code Suggestions**: GitHub Copilot references structural engineering knowledge for better enhancements
- **Seamless Workflow**: Generated code + domain knowledge = smarter AI assistance

### ⚡ Multiple Trigger Methods
- **Auto-Generation**: Type trigger comments and press Enter for instant code generation
- **Manual Selection**: Select text and right-click for on-demand generation
- **Command Palette**: Access via `Ctrl+Shift+P` → "ETABS Copilot: Generate Script"

### 🏗️ Comprehensive ETABS Support
- Model initialization and connection handling
- Material property definitions
- Geometric element creation
- Load pattern and case management
- Analysis execution and result extraction
- Error handling and validation patterns

## How It Works

### 1. AI-Powered Generation
The extension connects to a sophisticated AI framework featuring:
- **Planner Agent**: Develops architectural plans from user queries
- **Code Generator Agent**: Creates ETABS API code following best practices  
- **Knowledge Graph**: Retrieves domain-specific engineering knowledge
- **Multiple LLM Integration**: Utilizes DeepSeek, Gemini, and Claude for specialized tasks

### 2. Domain Knowledge Creation
For every generation, the extension creates a workspace knowledge file containing:
- Architectural planning context
- Domain-specific engineering steps
- ETABS API patterns and best practices
- Structural engineering validation rules

### 3. GitHub Copilot Enhancement
With domain knowledge available, GitHub Copilot can provide:
- Structural engineering-specific error handling
- ETABS API compliance suggestions
- Design validation and engineering checks
- Context-aware code improvements

## Live Demo: Counting Beams and Columns
![Animation_3-ezgif com-optimize](https://github.com/user-attachments/assets/fadc14cb-35f6-47d0-9914-2bd36642ba96)
### Step 1: Natural Language Input
```python
# etabs: Please help me count the number of beams and columns in each story.
```
*Press Enter → Extension generates clean ETABS code*

### Step 2: Generated Code (20 lines)
```python
import comtypes.client
helper = comtypes.client.CreateObject('ETABSv1.Helper')
helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
SapModel = helper.GetObject("CSI.ETABS.API.ETABSObject").SapModel

# Retrieve story names and initialize counters
num_stories, story_names, ret = SapModel.Story.GetNameList()
story_beam_counts = {story: 0 for story in story_names}
story_column_counts = {story: 0 for story in story_names}

# Count beams and columns per story
for story in story_names:
    frame_obj_num, frame_ID_tuple, ret = SapModel.FrameObj.GetNameListOnStory(story)
    for frame_ID in frame_ID_tuple:
        point_1, point_2, ret = SapModel.FrameObj.GetPoints(frame_ID)
        X1, Y1, Z1, ret = SapModel.PointObj.GetCoordCartesian(point_1)
        X2, Y2, Z2, ret = SapModel.PointObj.GetCoordCartesian(point_2)
        
        tolerance = 1e-3
        if abs(Z1 - Z2) < tolerance:
            story_beam_counts[story] += 1
        else:
            story_column_counts[story] += 1

# Display results
for story in story_names:
    print(f"Story: {story}, Beams: {story_beam_counts[story]}, Columns: {story_column_counts[story]}")
```

### Step 3: Domain Knowledge File Created
```markdown
# ETABS Domain Knowledge
**User Query:** Please help me count the number of beams and columns in each story.

## Domain-Specific Knowledge Steps
### Step 1: ETABS API Knowledge
- GetNameList - Retrieves story names
- GetNameListOnStory - Gets frame objects on specific story
- GetPoints - Gets end point coordinates for classification...
```

### Step 4: GitHub Copilot Enhancement
With both the generated code and .etabs-knowledge.md file in workspace:

**User**: "Please help me enhance the code"

**GitHub Copilot automatically references the domain knowledge file and transforms the basic code into production-ready software.**

### Step 5: Enhanced Code Features
- **Robust Error Handling**: COM API exception handling with meaningful messages
- **Modular Architecture**: Separate functions for connection, classification, and export
- **Command Line Interface**: `--tolerance` and `--csv` options for flexibility  
- **Engineering Validation**: Proper tolerance handling and coordinate validation
- **Professional Documentation**: Comprehensive docstrings and usage examples
- **Data Export**: CSV export capability for further analysis
- **Input Validation**: Bounds checking and type validation for all parameters

## ETABS Copilot Case Study - Supplementary Materials

### Repository Contents
- **90 Experimental Queries**: Comprehensive test dataset spanning pre-analysis, model modification, and post-analysis tasks
- **Real-World Case Study**: Five-story office building model with construction and analysis queries
- **Generated Code**: Python scripts using ETABS API for all queries

### ETABS Model Specifications
- Building type: Five-story office building
- Plan dimensions: 60 ft × 80 ft
- Total height: 63 ft
- Grid: 4×5 at 20 ft spacing
- Structural elements: 100 columns, 175 beams, 60 slabs
- Load combinations: 4 ASCE 7 combinations

### Usage
1. Open the ETABS model: `data/real_world/model/office.EDB`
2. Run construction script in: `python data/real_world/code`
3. Run post-analysis queries as needed
<img width="1010" height="1263" alt="case study_2" src="https://github.com/user-attachments/assets/76c9ef45-edb9-4552-9b39-683a62e9d2a1" />
<img width="1010" height="1263" alt="case study_1" src="https://github.com/user-attachments/assets/6db12297-3209-40d8-8e6c-086f839d6bcb" />

## Key Transformation Metrics

**From Natural Language to Production Code:**
- **Input**: Single comment line requesting beam/column counting
- **Generated**: 20 lines of functional ETABS code  
- **Enhanced**: 100+ lines of production-ready software
- **Features Added**: Error handling, CLI, CSV export, validation, documentation

**Domain Knowledge Impact:**
- GitHub Copilot referenced specific ETABS API patterns from knowledge file
- Applied structural engineering tolerance concepts (1e-3 precision)
- Implemented COM interface error handling best practices
- Added engineering-specific validation and warning messages

**Professional Software Features:**
- Command-line arguments (`--tolerance`, `--csv`)
- Modular function architecture for reusability
- Comprehensive error handling with meaningful messages
- Data export capabilities for engineering analysis
- Input validation and bounds checking
- Professional documentation and type hints

## Technical Highlights

### ETABS API Expertise
- Proper object initialization sequences
- Unit management and coordinate systems
- Error handling and validation patterns

### VS Code Integration
- Native extension architecture
- Real-time document change detection
- Progress notifications and cancellation support
- Command palette and context menu integration

## Use Cases

### Structural Engineers
- Rapid prototyping of ETABS models
- Learning ETABS API patterns and best practices
- Generating boilerplate code for common operations
- Exploring structural modeling approaches

### Engineering Software Developers  
- ETABS API code examples and templates
- Integration patterns for structural analysis workflows
- Error handling and validation implementations
- Educational resource for ETABS programming

### Research Applications
- Automated model generation for parametric studies
- Batch processing workflows for structural analysis
- Integration with optimization algorithms
- Educational tool for structural engineering courses

## Benefits

### For Individual Engineers
- **Faster Development**: Minutes instead of hours for model setup
- **Learning Tool**: Understand ETABS API through generated examples
- **Error Reduction**: AI-generated code follows established patterns
- **Enhanced Productivity**: Focus on engineering instead of programming syntax

### For Engineering Teams
- **Standardization**: Consistent code patterns across projects
- **Knowledge Sharing**: Domain expertise embedded in generated code
- **Onboarding**: New team members learn ETABS programming faster  
- **Quality Assurance**: AI-validated code reduces bugs and errors

### For the Engineering Community
- **Accessibility**: Makes ETABS programming accessible to more engineers
- **Innovation**: Enables rapid exploration of structural modeling ideas
- **Education**: Provides practical examples for learning structural programming
- **Collaboration**: Shared knowledge base improves with each generation

## Future Enhancements

- Support for additional structural analysis software (SAP2000, PKPM, YJK, MIDAS, ABAQUS, etc.)
- Integration with other AI coding assistants
- Custom domain knowledge training
- Team collaboration features
- Enhanced validation and verification capabilities

---

**Note**: This is a research demonstration showcasing the integration of specialized AI agents with GitHub Copilot for domain-specific code generation in structural engineering.
