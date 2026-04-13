# 🌐 GeoQC Tools — Automated Geospatial QA/QC Framework for ArcGIS Pro

![ArcGIS Pro](https://img.shields.io/badge/ArcGIS_Pro-3.x-blue?logo=esri)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)
![ArcPy](https://img.shields.io/badge/ArcPy-Enabled-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A portable, scalable, and modular **ArcPy-based geoprocessing toolbox** for automating large-scale Quality Assurance and Quality Control (QA/QC) of geospatial vector databases within ArcGIS Pro. Designed for **batch-processing** multiple File Geodatabases simultaneously, this framework eliminates manual validation bottlenecks and brings deterministic, reproducible spatial integrity checks to any GIS project.

---

## 📋 Table of Contents

- [Why GeoQC Tools?](#-why-geoqc-tools)
- [Key Capabilities](#-key-capabilities)
- [Use Cases](#-use-cases)
- [Architecture Overview](#-architecture-overview)
- [Performance Benchmarks](#-performance-benchmarks)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
  - [Step 1 — Download from GitHub](#step-1--download-from-github)
  - [Step 2 — Import the Toolbox into ArcGIS Pro](#step-2--import-the-toolbox-into-arcgis-pro)
  - [Step 3 — Run the Feature Count Tool](#step-3--run-the-feature-count-tool)
  - [Step 4 — Run the Validate Rules Tool](#step-4--run-the-validate-rules-tool)
  - [Step 5 — Review Outputs](#step-5--review-outputs)
- [Tool Reference](#-tool-reference)
  - [Feature Count Tool](#1-feature-count-tool)
  - [Validate Rules Tool](#2-validate-rules-tool)
- [Validation Rules Engine](#-validation-rules-engine)
- [Outputs Explained](#-outputs-explained)
- [Customization & Extensibility](#-customization--extensibility)
  - [Adding New Validation Rules](#adding-new-validation-rules)
  - [Adapting to a New Project Schema](#adapting-to-a-new-project-schema)
- [Maintenance](#-maintenance)
- [Repository Structure](#-repository-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 Why GeoQC Tools?

Manual validation of high-volume vector datasets using standard GUI tools is **repetitive, time-consuming, and prone to human error**. As geospatial datasets grow in scale — spanning thousands of features across multiple geodatabases — the absence of a unified, automated validation framework leads to:

- **Subjective interpretations** of topology rules by different analysts
- **Inconsistent data quality** and false positives
- **Severe bottlenecks** in production and delivery pipelines

GeoQC Tools replaces this fragmented manual workflow with a **centralized, algorithmic, batch-processing engine** that delivers objective, reproducible results with 100% feature coverage.

---

## ⚡ Key Capabilities

| Capability | Description |
|---|---|
| **Automated Data Inventory** | Recursively traverses directories to discover, catalog, and count every feature class across multiple File Geodatabases in a single run |
| **Deterministic Validation Engine** | Executes 22+ topological and attribute integrity checks using rigid spatial logic |
| **Batch Processing** | Processes multiple GDBs simultaneously — no manual iteration required |
| **Non-Destructive Auditing** | Logs all non-conformities into a separate **Exception Geodatabase** without altering source data |
| **In-Memory Processing** | Leverages `in_memory` workspaces and optimized cursors to process spatial joins entirely in RAM |
| **Configurable Thresholds** | User-defined metric thresholds for line length, polygon area, and building area |
| **Selective Execution** | Choose specific geodatabases and/or specific rules to run — or run everything at once |
| **Portable Deployment** | Delivered as `.atbx` (ArcGIS Toolbox) and `.gpkx` (Geoprocessing Package) — zero external dependencies |
| **Modular Architecture** | Seamlessly add, remove, or modify validation rules without disrupting existing functionality |

---

## 🌍 Use Cases

This framework is **not limited to any single project or domain**. It is designed to be adapted and integrated into any large-scale geospatial QA/QC pipeline, including but not limited to:

| Domain | Example Application |
|---|---|
| **Urban Planning & Smart Cities** | Validate digitized urban features (buildings, roads, land use) from high-resolution satellite imagery |
| **Cadastral / Land Records** | Check for overlapping parcels, gaps between boundaries, and attribute consistency |
| **Utility Network Mapping** | Detect dangles, disconnected lines, and duplicate infrastructure features |
| **Environmental & Forestry GIS** | Validate land cover polygons for slivers, overlaps, and minimum mapping unit compliance |
| **Transportation & Road Networks** | Ensure topological connectivity, detect short line segments, and validate attribute domains |
| **Disaster Management / Emergency Mapping** | Rapid QC of crisis-generated vector data before integration into response platforms |
| **National Mapping Programs** | Batch-validate multi-city, multi-state geodatabases against standardized schema requirements |
| **Defence & Intelligence Geospatial** | Enforce strict geometric and attribute standards across classified datasets |

> **The modular rule engine can be customized to enforce any organization's data standards — simply define your validation logic, map it to the rule engine, and deploy.**

---

## 🏗 Architecture Overview
┌──────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│              (Master Node — Version Control)             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   .atbx Toolbox          .gpkx Geoprocessing Package     │
│   ┌─────────────┐        ┌──────────────────────┐        │
│   │ Embedded    │        │ .atbx + Schema Defs  │        │
│   │ Python      │        │ + Relative Paths     │        │
│   │ Scripts     │        │ (Fully Portable)     │        │
│   └──────┬──────┘        └──────────┬───────────┘        │
│          │                          │                    │
└──────────┼──────────────────────────┼────────────────────┘
│     Clone / Download     │
▼                          ▼
┌──────────────────────────────────────────────────────────┐
│              Local Workstation — ArcGIS Pro              │
│                                                          │
│   Catalog Pane ─► Add Toolbox ─► Geoprocessing Pane      │
│                                                          │
│   ┌─────────────────┐    ┌───────────────────────┐       │
│   │ Feature Count   │    │ Validate Rules        │       │
│   │ Tool            │    │ Tool                  │       │
│   └────────┬────────┘    └──────────┬────────────┘       │
│            │                        │                    │
│            ▼                        ▼                    │
│   CSV Feature Report      Exception GDB + CSV Summary    │
└──────────────────────────────────────────────────────────┘

The framework uses a **five-stage deployment protocol**:

1. **Tool Encapsulation** — Python scripts embedded directly into `.atbx` (no external `.py` files needed)
2. **Package Compilation** — Optional `.gpkx` bundle with schema definitions and standardized relative paths
3. **Version Control Upload** — Pushed to GitHub as the single source of truth
4. **Retrieval & Acquisition** — Users clone or download ZIP (no admin privileges required)
5. **Workspace Integration** — Register toolbox in ArcGIS Pro's Catalog Pane; runs as a native extension

---

## 📊 Performance Benchmarks

Measured against established manual benchmarks:

| Metric | Manual Workflow | Automated Framework | Improvement |
|---|---|---|---|
| **Inventory Latency** | ~15 min / GDB | ~27 sec / GDB | **97% Reduction** |
| **Validation Latency** | ~45 min / GDB | ~2.08 min / GDB | **95% Reduction** |
| **Batch Processing (5 GDBs)** | Sequential / Linear | Iterative — < 11 min total | **21× Acceleration** |
| **Feature Coverage** | Sample-based | 100% Full Audit | **Complete** |

---

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| **ArcGIS Pro** | Version 3.x or later (with active license) |
| **Python** | 3.9+ (bundled with ArcGIS Pro's conda environment) |
| **ArcPy** | Included with ArcGIS Pro — no separate installation needed |
| **Data Format** | Esri File Geodatabases (`.gdb`) |
| **OS** | Windows 10/11 (ArcGIS Pro requirement) |

> **No additional Python packages or external dependencies are required.** Everything is self-contained within the toolbox.

---

## 🚀 Getting Started

### Step 1 — Download from GitHub

**Option A: Clone the repository**
```bash
git clone https://github.com/<your-org>/GeoQC-Tools.git

Option B: Download as ZIP

Navigate to the repository page on GitHub
Click the green <> Code button
Select Download ZIP
Extract the ZIP to a local directory (e.g., C:\GeoQC-Tools\)
Note: No administrative installation privileges are required.

Step 2 — Import the Toolbox into ArcGIS Pro
Launch ArcGIS Pro and open your target project (new or existing).

Open the Catalog Pane:

On the ribbon, click the View tab → Windows group → click Catalog Pane.
Add the Toolbox:

In the Catalog Pane, right-click Toolboxes → select Add Toolbox.
Browse to the downloaded folder and select either:
QAQC_Toolbox.atbx (standalone toolbox), or
QAQC_Toolbox.gpkx (geoprocessing package — double-click to unpack first)
Click OK.
Open a Tool:

Expand the newly added toolbox in the Catalog Pane.
Double-click Feature Count or Validate Rules to launch the tool's GUI interface.
Tip: You can also open the Geoprocessing Pane (View → Geoprocessing) and search for the tool by name after adding it.

Step 3 — Run the Feature Count Tool
Input Folder (Required): Browse to the root directory containing your File Geodatabases (.gdb).

Select Geodatabases (Optional): Once the input folder is set, the dropdown dynamically populates with discovered GDBs. Select specific ones, or leave blank to process all.

Output File (Required): Define the destination path and filename for the report. Defaults to .csv format (e.g., Feature_Count_Report.csv).

Click Run. The tool will recursively traverse all GDB structures, catalog every feature class, and generate a consolidated CSV census.

Step 4 — Run the Validate Rules Tool
Input Folder (Required): Browse to the directory containing the source geodatabases to be audited.

Select Geodatabases (Optional): Dynamically populated after folder selection. Pick specific GDBs or leave blank for all.

Select Rules (Optional): Use the dropdown to select specific validation rules. Leave blank to execute all rules.

Output File (Required): Define the target folder and filename for the quantitative CSV summary report.

Metric Thresholds (Optional — with sensible defaults):

Parameter	Description	Default
Small Length in Lines	Minimum acceptable line length	1.0 Meters
Small Area in Polygons	Minimum acceptable polygon area	5.0 Sq. Meters
Small Area in Buildings	Minimum acceptable building area	5.0 Sq. Meters
Click Run. The geoprocessing window displays real-time, rule-by-rule status updates with a progress bar.

Step 5 — Review Outputs
Output	Location	Description
CSV Summary Report	Path defined in Output File parameter	Quantitative summary of feature counts or validation results. Automatically added to the Contents Pane for quick review.
Exception Geodatabase (QA_Results.gdb)	Same output directory	Contains all flagged non-conformities as spatial features — open in the map canvas to visually inspect error geometries.
📖 Tool Reference
1. Feature Count Tool
Purpose: Automated data inventory and structural discovery — verifies data completeness before spatial validation.

Parameter	Data Type	Required	Description
input_folder	Folder	✅ Yes	Root directory containing project GDBs
select_gdb	String (MultiValue)	❌ Optional	Specific GDBs to process; blank = all
output_file	File (.csv)	✅ Yes	Destination path for the CSV report
What it does:

Uses arcpy.da.Walk to recursively discover all feature classes across all GDBs
Counts records in every feature class
Flags feature classes with zero records (data gaps)
Outputs a consolidated cross-database feature count report
2. Validate Rules Tool
Purpose: Primary diagnostic engine for spatial integrity — executes deterministic topological and attribute checks.

Parameter	Data Type	Required	Description
input_folder	Folder	✅ Yes	Directory containing source GDBs
select_gdb	String (MultiValue)	❌ Optional	Specific GDBs to audit; blank = all
select_rules	String (MultiValue, ValueList)	❌ Optional	Specific rules to run; blank = all rules
output_file	File (.csv)	✅ Yes	Destination for the CSV summary report
small_length	Double	❌ Optional	Min line length threshold (default: 1.0m)
small_area_polygon	Double	❌ Optional	Min polygon area threshold (default: 5.0 sq m)
small_area_building	Double	❌ Optional	Min building area threshold (default: 5.0 sq m)
What it does:

Executes 22+ deterministic validation rules across selected GDBs
Logs all non-conformities into a separate Exception Geodatabase (non-destructive)
Generates a quantitative CSV summary report
Displays real-time progress with rule-by-rule status updates
🔬 Validation Rules Engine
The framework implements validation rules across four core ArcGIS Pro geoprocessing logic categories:

Logic Category	ArcPy Implementation	Example Rules
Topology / Data Reviewer	CreateTopology, ValidateTopology	No Gaps, No Overlaps, Building Overlap, Dangles
Spatial Relations	SelectLayerByLocation	Features crossing boundaries, Features on restricted zones
Redundancy Check	FindIdentical	Duplicate points, lines, polygons
Geometric Metrics	CalculateGeometryAttributes	Small length lines, Small area polygons/buildings
Attribute Filter	SelectLayerByAttribute	Attribute domain violations, NULL field checks
💡 All rules are deterministic — they produce objective pass/fail results with no subjective interpretation, ensuring consistency across analysts and sessions.

📤 Outputs Explained
CSV Summary Report
Consolidated tabular report with rule-by-rule counts of flagged features per GDB
Auto-added to the ArcGIS Pro Contents Pane after execution for immediate review
Exception Geodatabase (QA_Results.gdb)
Contains the actual error geometries as feature classes — one per rule
Open directly in the Map Canvas to visually inspect and spatially locate every flagged anomaly
Source data remains completely untouched — the Exception GDB is an immutable audit trail
🔧 Customization & Extensibility
Adding New Validation Rules
The modular architecture allows seamless integration of new rules:

Define Logic — Identify the spatial/attribute relationship to validate
Edit Script — In the Catalog Pane, right-click the tool → Edit to open the embedded Python script
Duplicate an Existing Rule Block — Copy a function that matches your desired logic pattern
Customize:
Rename the function
Update input_layer and target_layer variables
Assign a unique Rule ID in the error logging dictionary
Register the Rule — Add the new function call to the main execution loop under the run_diagnostics class method
Adapting to a New Project Schema
To deploy the tool on a completely different project with different feature class naming conventions:

Branch the Toolbox — Create a copy of the .atbx file
Global Search/Replace — Use the script editor's Find & Replace to update all schema-specific naming conventions to match your new project's nomenclature
Test & Verify — Run a test validation on a sample dataset to ensure all functions correctly identify the new feature classes
🛠 Maintenance
Updating Tool Logic (e.g., when your source schema changes):

In the Catalog Pane, right-click the script tool → select Edit
Scroll to the initialization block where feature classes and layer names are defined
Modify the specific string values to match the new schema requirements
Save (Ctrl+S) and close the editor
The tool automatically recompiles with the updated logic upon the next execution
📁 Repository Structure
