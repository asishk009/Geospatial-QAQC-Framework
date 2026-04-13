# Geospatial QA/QC Framework for ArcGIS Pro

A reusable ArcPy-based QA/QC framework for large-scale geospatial data processing in ArcGIS Pro.

This repository is designed for organizations and teams that need to inventory, validate, and review large geospatial deliveries in a consistent and scalable way. Although the framework was developed in the context of structured urban geospatial validation, its design is not limited to any single mission or program. It can be adapted for multiple geospatial applications such as urban mapping, utilities, cadastral datasets, transportation layers, environmental inventories, infrastructure databases, enterprise GIS updates, and vendor-delivered geodatabases.

The framework supports batch processing across one or many file geodatabases, helps standardize QA/QC workflows, and reduces dependence on repetitive manual inspection.

---

## Why this framework

Large geospatial datasets often include thousands to millions of features distributed across multiple geodatabases and thematic layers. Manual QA/QC in such environments is time-consuming, difficult to standardize, and prone to inconsistent interpretation.

This framework helps move QA/QC from isolated manual checks to a repeatable, tool-driven workflow inside ArcGIS Pro.

It is built to support:

- geodatabase inventory and completeness checks
- rule-based validation of geometry, attributes, and spatial relationships
- batch QA/QC across multiple geodatabases
- review-ready outputs for correction and audit
- customization for different schemas, naming conventions, and project standards

---

## Typical use cases

This framework can be used in a wide range of geospatial workflows, including:

- pre-delivery QA/QC for vendor-submitted geodatabases
- data acceptance for enterprise GIS updates
- validation of base maps and thematic urban layers
- utility and infrastructure data quality review
- cadastral and parcel dataset screening
- environmental and land-use data validation
- regional or multi-city geospatial program monitoring
- repeatable QA/QC before integration into a central spatial repository

---

## What the framework includes

The repository currently contains the ArcGIS Pro toolbox and supporting source material used to run and extend the workflow.

### Repository contents

```text
Geospatial-QAQC-Framework/
├── ArcPy_Scripts/
├── Source_Code/
├── EnterpriseSpatialAnalytics.atbx
└── README.md
```

### Key components

- **EnterpriseSpatialAnalytics.atbx**  
  The main ArcGIS Pro toolbox to import and run inside a project.

- **ArcPy_Scripts/**  
  Supporting ArcPy notebooks or script development files used for tool logic and prototyping.

- **Source_Code/**  
  Underlying source files for execution logic, validation logic, and future customization.

- **README.md**  
  Documentation for setup, usage, and adaptation.

---

## Core tools

### 1. Feature Count

The **Feature Count** tool is the data inventory module.

It scans one or more file geodatabases, discovers feature classes, and creates a consolidated feature count report. This is useful as a first-pass completeness check before deeper QA/QC is performed.

Use this tool to:

- verify that expected geodatabases and layers are present
- identify empty or missing feature classes
- compare datasets across submissions, towns, zones, or project units
- create a quick inventory report before validation

### 2. Validate Rules

The **Validate Rules** tool is the main QA/QC engine.

It runs configurable validation checks across the selected geodatabases and produces outputs for review. The validation workflow is intended to identify non-conformities without modifying the source data.

Use this tool to:

- run deterministic QA/QC checks at scale
- validate geometry, attributes, and inter-layer relationships
- isolate exceptions for review and correction
- create standardized outputs for audit and reporting

---

## Requirements

Before using the framework, make sure you have the following:

- **ArcGIS Pro** installed
- access to the **ArcPy** environment included with ArcGIS Pro
- one or more **File Geodatabases (.gdb)** to process
- permission to read input folders and write outputs
- **Git** installed only if you want to clone the repository from the command line

No separate software installation is required beyond ArcGIS Pro for standard toolbox use.

---

## Get the files from GitHub

You can retrieve the framework from the hosted GitHub repository in either of the following ways.

### Option A: Clone the repository

```bash
git clone https://github.com/asishk009/Geospatial-QAQC-Framework.git
```

### Option B: Download as ZIP

1. Open the repository in GitHub.
2. Click **Code**.
3. Click **Download ZIP**.
4. Extract the ZIP to a local folder on your machine.

After download, confirm that the extracted folder contains at least the following:

- `EnterpriseSpatialAnalytics.atbx`
- `ArcPy_Scripts/`
- `Source_Code/`
- `README.md`

---

## Add the toolbox to ArcGIS Pro

Once the repository is available on your local machine, import the toolbox into ArcGIS Pro.

### Steps

1. Open **ArcGIS Pro**.
2. Create a new project or open an existing project.
3. Open the **Catalog** pane.
4. In the Catalog pane, locate **Toolboxes**.
5. Right-click **Toolboxes**.
6. Click **Add Toolbox**.
7. Browse to the local repository folder.
8. Select **EnterpriseSpatialAnalytics.atbx**.
9. Click **OK**.

The toolbox will now appear inside your ArcGIS Pro project and can be run like a native geoprocessing toolbox.

---

## Open the tool interface

To make tool execution easier:

1. Go to the **View** tab in ArcGIS Pro.
2. Open the **Geoprocessing** pane if it is not already visible.
3. In the **Catalog** pane, expand **Toolboxes**.
4. Expand **EnterpriseSpatialAnalytics.atbx**.
5. Double-click the tool you want to run.

---

## Quick start workflow

A recommended execution sequence is:

1. Download or clone the repository from GitHub.
2. Add `EnterpriseSpatialAnalytics.atbx` to ArcGIS Pro.
3. Run **Feature Count** to verify data availability and completeness.
4. Review the generated inventory output.
5. Run **Validate Rules** to perform QA/QC checks.
6. Review the output report and any generated exception layers.
7. Correct source data as needed.
8. Re-run validation until the dataset meets your project standards.

---

## Run the Feature Count tool

### Purpose

The Feature Count tool inventories the data structure and record availability across one or more geodatabases.

### Parameters

- **Input Folder**  
  The root folder containing the source file geodatabases.

- **Select Geodatabases** *(optional)*  
  Select specific geodatabases to process. Leave blank to process all geodatabases found in the input folder.

- **Output File**  
  The destination path and filename for the generated report.

### How to run

1. Open **Feature Count** from the toolbox.
2. Set **Input Folder** to the folder containing the geodatabases.
3. Use **Select Geodatabases** only when you want to process a subset.
4. Set **Output File** to the desired output location.
5. Click **Run**.

### Expected output

The tool generates a summary report, typically as a CSV, containing feature counts for the discovered feature classes across the selected geodatabases.

This output can be used to:

- confirm that expected layers are populated
- identify missing or empty datasets
- compare dataset completeness across multiple submissions
- perform a quick readiness check before running validation

---

## Run the Validate Rules tool

### Purpose

The Validate Rules tool runs rule-based QA/QC checks on the selected geodatabases.

### Parameters

- **Input Folder**  
  The folder containing the source geodatabases to be audited.

- **Select Geodatabases** *(optional)*  
  Select one or more geodatabases from the detected list. Leave blank to process all available geodatabases in the folder.

- **Select Rules** *(optional)*  
  Select specific validation rules to run. Leave blank to execute the full available rule set configured in the tool.

- **Output File**  
  The destination path and filename for the validation summary report.

- **Threshold - Small Length in Lines** *(optional)*  
  Minimum line length threshold. Default value is typically **1 meter**.

- **Threshold - Small Area in Polygons** *(optional)*  
  Minimum polygon area threshold. Default value is typically **5 square meters**.

- **Threshold - Small Area in Buildings** *(optional)*  
  Minimum building area threshold. Default value is typically **5 square meters**.

### How to run

1. Open **Validate Rules** from the toolbox.
2. Set **Input Folder** to the folder containing the geodatabases to review.
3. Use **Select Geodatabases** to process a subset, or leave blank to process all.
4. Use **Select Rules** to run only specific checks, or leave blank to run all configured rules.
5. Set **Output File** for the validation report.
6. Review or adjust the threshold parameters as needed for your project.
7. Click **Run**.

### Expected output

Depending on the configured implementation, the tool can produce:

- a validation summary report, usually as a CSV
- exception outputs for review in ArcGIS Pro
- review-ready layers or tables that help isolate issues for correction
- processing messages in the Geoprocessing pane during execution

In many workflows, exception geometries and tabular summaries are reviewed alongside the source geodatabases to support correction and re-validation.

---

## Output review

After the tools finish running:

- review the **CSV output** for summary results
- inspect any generated **exception layers** or **QA/QC outputs** inside ArcGIS Pro
- verify that outputs were written to the location defined in the tool parameters
- use the results to correct the source data and rerun the checks where needed

A practical review cycle is:

1. run inventory
2. verify completeness
3. run validation
4. inspect exceptions
5. correct data
6. rerun validation

---

## Adapting the framework for different geospatial applications

This framework is intentionally structured so it can be extended beyond a single domain or program. It can be adapted to different projects by changing schema references, rule logic, and threshold values.

### Common adaptation scenarios

- changing feature class names
- changing attribute field names
- aligning rules to a new data model
- adjusting thresholds for different map scales or feature types
- adding new inter-layer logic for a specific business workflow
- replacing project-specific naming conventions with a new standard

### Examples of domains where this can be reused

- urban base mapping
- utilities and network mapping
- cadastral and parcel systems
- transportation GIS
- environmental and resource inventories
- infrastructure asset databases
- enterprise GIS data acceptance workflows

---

## Customization guidance

There are two common ways to customize the framework.

### Option 1: Modify the supporting source files

Use the files in:

- `ArcPy_Scripts/`
- `Source_Code/`

This is the best option when you want to inspect logic, refactor code, add new rules, or maintain version-controlled changes.

### Option 2: Edit the embedded script tools in ArcGIS Pro

Inside ArcGIS Pro:

1. In the **Catalog** pane, expand the imported toolbox.
2. Right-click the relevant script tool.
3. Click **Edit**.
4. Update the embedded logic as needed.
5. Save the changes and rerun the tool.

### Typical customization tasks

- update layer references
- update field mappings
- add new validation rules
- remove obsolete checks
- modify default thresholds
- refine output naming and report structure

After any customization, test the workflow on a sample geodatabase before using it on production data.

---

## Maintenance

Ongoing maintenance may be required when:

- schemas change
- layer names are revised
- attribute fields are renamed
- rule definitions evolve
- new deliverable standards are introduced

A recommended maintenance cycle is:

1. identify the affected schema or rule change
2. update the relevant script logic
3. test on a representative sample dataset
4. verify outputs
5. publish the updated toolbox to the repository

Keeping the toolbox and source files under version control helps maintain a reliable change history.

---

## Recommended good practices

- run **Feature Count** before **Validate Rules**
- test changes on a small sample before running a large batch
- keep output folders separate from source data folders
- maintain a consistent folder structure for repeatable runs
- store updated rule logic in version control
- document project-specific rule customizations for future users

---

## Limitations and notes

- The framework depends on **ArcGIS Pro** and **ArcPy**.
- Validation behavior depends on the configured rule logic and schema mappings.
- Some complex QA/QC cases may still require analyst review after automated screening.
- Thresholds and rule selections should be reviewed before operational use in a new application area.

---

## Summary

This repository provides a practical ArcGIS Pro QA/QC framework for large-scale geospatial processing. It supports inventory, rule-based validation, batch execution, and review-ready outputs while remaining flexible enough to be adapted across different geospatial domains.

Rather than being restricted to a single project context, the framework should be treated as a reusable foundation for structured geospatial QA/QC workflows in any environment where scalable validation, consistency, and operational clarity are required.

---

## Author

Asish Kandikonda | asishk009 | asishkandikonda@gmail.com

Guide: M Ramadasu | Scientist/Engineer ‘SF’ | Urban Studies Division | National Remote Sensing Center, Indian Space Research Organization
