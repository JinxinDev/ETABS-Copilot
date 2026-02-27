# AI Copilot for Automated Building Design Using Knowledge Graphs and Numerical Models

> **Jinxin Chen, Yi Bao** — Department of Civil, Environmental and Ocean Engineering, Stevens Institute of Technology, Hoboken, NJ 07030, USA
> Corresponding author: yi.bao@stevens.edu

---

## Overview

This repository contains the data, code, and queries associated with the paper:

**"Artificial Intelligence Copilot for Automated Design of Buildings Using Knowledge Graphs and Numerical Models"**

The paper presents an AI Copilot framework that automates structural building design by integrating large language models (LLMs) with a domain-specific knowledge graph in a multi-agent framework. Natural language queries from engineers are converted into executable operations in structural engineering software (ETABS). The Copilot achieves **100% results consistency** with manual operations while reducing total workflow time by **90%**, and demonstrates **~90% functional correctness** on a 90-query benchmark.

---

## Five-Story Building Case Study

<p align="center">
  <img width="400" alt="case study 2D" src="https://github.com/user-attachments/assets/6db12297-3209-40d8-8e6c-086f839d6bcb" />
  <img width="400" alt="case study 3D" src="https://github.com/user-attachments/assets/76c9ef45-edb9-4552-9b39-683a62e9d2a1" />
</p>

---

## Live Demos

### Case 1: Initialize a New Model
![case_1(initialize)](https://github.com/user-attachments/assets/0d071ddc-f96f-4034-8346-dded2060632e)



### Case 2: Create Beams for Specific Axis and Stories
![case_2(create_beam)](https://github.com/user-attachments/assets/3d553db3-16a3-4ec0-922d-877abafd33a8)


### Case 3: Report Beam and Column Information for Specific Story
![case_3(report_frame)](https://github.com/user-attachments/assets/9751e263-7a3f-43bd-a68a-eca3c6a40372)


---

## Repository Structure
```
data/
├── experimental/               # Experimental study (five-story building validation)
│   ├── code/
│   │   ├── model_modification/ # Scripts for modifying the structural model
│   │   ├── post_analysis/      # Scripts for post-processing analysis results
│   │   └── pre_analysis/       # Scripts for pre-processing and model setup
│   └── queries/
│       ├── model_modification_queries.txt  # Queries for model modification tasks
│       ├── post_analysis_queries.txt       # Queries for post-analysis tasks
│       └── pre_analysis_queries.txt        # Queries for pre-analysis tasks
│
└── real_world/                 # Real-world office building case study
    ├── code/
    │   ├── model_creation/     # Scripts for constructing the structural model
    │   └── post_analysis/      # Scripts for post-processing analysis results
    ├── model/
    │   ├── 3d view.jpg         # 3D view of the office building model
    │   ├── office.EDB          # ETABS model file for the office building
    │   └── plane view.jpg      # Plan view of the office building model
    └── queries/
        ├── model_construction_query.txt  # Queries for model construction tasks
        └── post_analysis_queries.txt     # Queries for post-analysis tasks
```

---

## Data Description

### `experimental/`
Contains code and queries used in the controlled experimental validation. The workflow is divided into three stages:
- **Pre-analysis**: Setting up and initializing structural models.
- **Model modification**: Updating model parameters such as cross-sections and material properties.
- **Post-analysis**: Extracting and evaluating structural responses.

### `real_world/`
Contains data for the real-world office building case study, including:
- The ETABS model file (`.EDB`) and visual representations of the building.
- Code for model creation and post-analysis.
- Natural language queries used to drive the AI Copilot during the case study.

---

## Requirements

- [ETABS](https://www.csiamerica.com/products/etabs) (CSI structural analysis software)
- Python 3.x
- An OpenAI-compatible LLM API key (e.g., GPT-4)
- Additional Python dependencies listed in `requirements.txt`

---

## Usage

1. Open the ETABS model file (`real_world/model/office.EDB`) in ETABS.
2. Run the AI Copilot application and connect it to the running ETABS instance.
3. Issue natural language queries (examples provided in the `queries/` folders) to perform modeling, modification, and analysis tasks.
4. Use the scripts in the `code/` folders for pre-processing and post-processing steps.

---

## Citation

If you use this code or data in your research, please cite:
```bibtex
@article{chen2025aicopilot,
  title   = {Artificial Intelligence Copilot for Automated Design of Buildings Using Knowledge Graphs and Numerical Models},
  author  = {Chen, Jinxin and Bao, Yi},
  year    = {2026}
}
```

---

## Contact

For questions or issues, please contact **Yi Bao** at [yi.bao@stevens.edu](mailto:yi.bao@stevens.edu).
