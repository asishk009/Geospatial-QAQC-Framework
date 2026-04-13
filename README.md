# Geospatial QA/QC Framework for ArcGIS Pro

A scalable ArcGIS Pro framework for batch QA/QC of large geospatial datasets.

This repository provides ArcPy-based tools for data inventory, rule-driven validation, and exception reporting across one or many file geodatabases. While the framework can support urban mapping programs, it is intentionally designed to be adaptable to a wide range of geospatial applications, including utilities, cadastral datasets, land records, environmental mapping, transportation layers, infrastructure inventories, and enterprise GIS data acceptance workflows.

## Overview

Large geospatial deliveries often contain thousands to millions of features distributed across multiple geodatabases, feature datasets, and thematic layers. Manual QA/QC in such environments is slow, repetitive, and difficult to standardize.

This framework helps teams move from manual inspection to repeatable, parameter-driven validation inside ArcGIS Pro. It supports:

- inventorying feature classes and record counts across multiple geodatabases
- running deterministic QA/QC checks on geometry, attributes, and spatial relationships
- producing review-ready outputs for correction and audit
- batch execution across multiple datasets from a single interface
- adapting the logic to different schemas, naming conventions, and project standards

## Typical Use Cases

This framework can be used in many geospatial QA/QC contexts, such as:

- pre-delivery validation of vendor-submitted geodatabases
- acceptance checks for enterprise GIS updates
- land use and base map quality control
- utility and infrastructure layer validation
- building, parcel, and polygon geometry screening
- multi-city or multi-region geospatial program monitoring
- project-based geodatabase audits before publication or integration

## Core Tools

### 1. Feature Count

The **Feature Count** tool acts as a data inventory and completeness check.

It scans geodatabases, identifies feature classes, and produces a consolidated feature count report. This is useful as a first-pass validation step before running deeper QA/QC checks.

Use this tool to:

- verify that expected layers are present
- compare record counts across geodatabases
- identify missing or empty feature classes
- create a quick inventory report for large submissions

### 2. Validate Rules

The **Validate Rules** tool acts as the primary QA/QC engine.

It runs deterministic validation checks across datasets and generates structured outputs for review. The tool is intended to identify non-conformities without altering the source data.

Use this tool to:

- run repeatable QA/QC checks at scale
- flag geometry, attribute, and inter-layer issues
- isolate exceptions for review and correction
- create standardized outputs for reporting and audit

## Requirements

Before using the tools, make sure you have:

- **ArcGIS Pro** installed
- access to **ArcPy** through the ArcGIS Pro Python environment
- one or more **File Geodatabases (.gdb)** to process
- permission to download or clone the repository from GitHub
- a local folder where outputs can be written

## Access the Repository from GitHub

You can retrieve the tools from the hosted GitHub repository in either of the following ways.

### Option A: Clone the repository

```bash
git clone <repository-url>

## Option B: Download as ZIP
Open the repository in GitHub.
Click Code.
Click Download ZIP.
Extract the ZIP to a local folder.

After download, confirm that the repository contains the toolbox/package files and supporting scripts needed for ArcGIS Pro.

Look for items such as:

ArcGIS toolbox files (.atbx)
geoprocessing packages (.gpkx), if provided
source scripts or notebooks
supporting documentation
Import the Tool into ArcGIS Pro
Add the toolbox
Open ArcGIS Pro.
Create a new project or open an existing one.
Open the Catalog pane.
Right-click Toolboxes.
Select Add Toolbox.
Browse to the downloaded repository folder.
Select the .atbx file and click OK.

The toolbox will now appear in the project under Toolboxes.

Open the geoprocessing interface

To make the tools easier to use:

Go to the View tab.
Open the Geoprocessing pane if it is not already visible.
Expand the imported toolbox in the Catalog pane.
Double-click a tool to open its parameter interface.
If a .gpkx package is provided

If the repository includes a geoprocessing package (.gpkx), use it as a packaged delivery option for portable deployment. The toolbox-based workflow above remains the recommended path for direct import, testing, and ongoing development.

How to Run the Tools
Run the Feature Count Tool
Open Feature Count from the toolbox.
Set Input Folder to the root directory containing the geodatabases to inventory.
Use Select Geodatabases only if you want to process a subset.
Leave it blank to process all geodatabases found in the input folder.
Set Output File to the location and name of the output report.
Recommended output: .csv
Click Run.
Feature Count Parameters
Input Folder: Folder containing source geodatabases
Select Geodatabases (optional): Specific geodatabases to process
Output File: Destination path for the generated report
Feature Count Output

The tool generates a summary report showing feature counts across geodatabases and feature classes. This output can be used to review completeness, compare submissions, and identify gaps before deeper validation.

Run the Validate Rules Tool
Open Validate Rules from the toolbox.
Set Input Folder to the directory containing the source geodatabases.
Use Select Geodatabases to choose specific datasets, or leave it blank to process all detected geodatabases.
Use Select Rules to run specific checks, or leave it blank to run the full available rule set.
Set Output File for the validation summary report.
Review and adjust threshold values if needed.
Click Run.
Validate Rules Parameters
Input Folder: Folder containing source geodatabases
Select Geodatabases (optional): Choose one or more geodatabases
Select Rules (optional): Choose one or more validation rules
Output File: Destination path for the generated report
Threshold - Small Length in Lines (optional): Default 1 meter
Threshold - Small Area in Polygons (optional): Default 5 square meters
Threshold - Small Area in Buildings (optional): Default 5 square meters
Validate Rules Output

The tool produces:

a summary output file, typically in .csv format
exception outputs for review inside ArcGIS Pro
review-ready QA/QC outputs that can be used to correct source data

Where configured, validation outputs can also be added back into the ArcGIS Pro project for quick inspection.

Recommended Workflow

For most projects, the recommended sequence is:

Download or clone the repository from GitHub
Add the toolbox to ArcGIS Pro
Run Feature Count first to confirm data availability and completeness
Review the inventory output
Run Validate Rules to perform QA/QC checks
Review the report and exception outputs
Correct source data as needed
Re-run validation until the dataset meets project standards
Adapting the Framework to Other Geospatial Applications

This repository is not intended to be limited to a single mission, program, or schema.

The framework can be adapted to new geospatial applications by updating:

feature class names
attribute field references
rule definitions
layer relationships
naming conventions
thresholds and project-specific standards

Examples of where the framework can be extended include:

city-scale base mapping
utility network QA/QC
parcel and cadastral validation
transportation datasets
environmental inventory layers
infrastructure asset databases
multi-agency geospatial data integration workflows
Customization

To adapt the framework for a new project:

Create a schema map for the target data model.
Identify the feature classes and fields used by the new workflow.
Update project-specific names and references in the validation logic.
Add, remove, or modify rule blocks as required.
Test the updated toolbox on a sample geodatabase before full deployment.

This approach makes it possible to reuse the same framework across different geospatial domains while keeping the logic aligned to local standards.

Maintenance

If the source schema changes over time, update the tool logic accordingly.

Typical maintenance tasks include:

updating renamed feature classes
revising attribute field names
adjusting thresholds
refining rule logic
adding new validation checks

After updates, re-test the tool on a representative sample dataset before operational use.

Notes
Use the toolbox (.atbx) for direct integration into ArcGIS Pro.
Use the geoprocessing package (.gpkx) when a packaged, portable delivery is preferred.
Keep repository paths organized and consistent to simplify deployment and maintenance.
Validate against sample datasets before scaling to production runs.
Treat the framework as a reusable QA/QC engine that can be tailored to multiple geospatial programs.
