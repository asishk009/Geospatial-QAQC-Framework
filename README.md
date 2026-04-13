# Geospatial QA/QC Framework for ArcGIS Pro

A reusable ArcPy-based framework for large-scale geospatial QA/QC, comparative feature analysis, and batch validation in ArcGIS Pro.

This repository provides a practical ArcGIS Pro workflow for teams working with one or many file geodatabases that need to be reviewed in a consistent, repeatable, and scalable way. While the framework was initially developed in the context of structured urban geospatial validation, it is not intended to be limited to a single mission or program. It can be adapted across a wide range of geospatial applications such as urban mapping, utilities, cadastral datasets, transportation layers, environmental inventories, infrastructure databases, enterprise GIS updates, and vendor-delivered geodatabases.

The framework supports:

- comparative feature analysis across multiple regions of interest (ROIs)
- batch QA/QC across one or many geodatabases
- rule-based validation of geometry, attributes, and spatial relationships
- review-ready outputs for correction and audit
- customization for new schemas, standards, and project workflows

---

## Why this framework

Large geospatial datasets often contain thousands to millions of features distributed across multiple geodatabases, feature datasets, and thematic layers. Manual QA/QC in such environments is time-consuming, repetitive, and difficult to standardize. It also becomes harder to distinguish whether an unusual pattern represents a real geographic condition or a data problem.

This framework helps move QA/QC from isolated manual checks to a structured, tool-driven workflow inside ArcGIS Pro.

It is designed to support both:

1. **comparative understanding of datasets across ROIs**, and  
2. **repeatable rule-based validation of data quality**.

That makes it useful not only for checking data correctness, but also for understanding how datasets vary from one area to another before detailed interpretation or downstream integration.

---

## Typical use cases

This framework can be used in a wide range of geospatial workflows, including:

- pre-delivery QA/QC for vendor-submitted geodatabases
- data acceptance for enterprise GIS updates
- urban base map validation
- utility and infrastructure data review
- cadastral and parcel dataset screening
- transportation and network layer checking
- environmental and land-use inventory review
- regional or multi-city geospatial program monitoring
- geodatabase comparison across multiple spatial units or project zones

---

## Repository structure

The current repository is organized around the ArcGIS Pro toolbox and supporting source material.

```text
Geospatial-QAQC-Framework/
├── ArcPy_Scripts/
├── Source_Code/
├── EnterpriseSpatialAnalytics.atbx
└── README.md
```

### Key components

- **EnterpriseSpatialAnalytics.atbx**  
  The main ArcGIS Pro toolbox to import into your project and run through the Geoprocessing pane.

- **ArcPy_Scripts/**  
  Supporting ArcPy notebooks or script development files used for tool logic and prototyping.

- **Source_Code/**  
  Supporting source files for execution logic, validation logic, and future customization.

- **README.md**  
  Setup, usage, and adaptation guide for the framework.

Depending on the release or future updates, additional deployment or documentation files may also be added.

---

## Core tools

### 1. Feature Count

The **Feature Count** tool is not limited to basic data inventory. It is designed as a comparative analytical module for examining how feature classes vary across multiple regions of interest, geodatabases, or project areas.

By systematically counting features across datasets, the tool helps users identify:

- unusual feature distributions
- missing or sparse datasets
- unusually dense datasets
- cross-region outliers
- broader spatial context that may explain why an ROI looks different from the rest

For example, if one ROI shows a significantly higher tree count than the other ROIs in the same comparison set, that may indicate a forested tract, plantation area, green belt, park-dominant region, or another land-cover pattern. That observation can then be interpreted together with other layers such as land use, building density, water features, or transport infrastructure.

In this way, the Feature Count tool serves two purposes:

- it confirms that data is present and organized correctly
- it provides a first-level analytical view of how feature distributions differ across geographies

Use this tool to:

- compare feature counts across multiple ROIs
- detect outliers in specific feature classes
- identify missing, sparse, or unusually dense layers
- establish a comparative baseline before validation
- support first-level interpretation of regional spatial character

### 2. Validate Rules

The **Validate Rules** tool is the primary QA/QC engine.

It runs configurable validation checks across the selected geodatabases and produces outputs for review. The tool is intended to identify non-conformities without altering the source data.

Use this tool to:

- run deterministic QA/QC checks at scale
- validate geometry, attributes, and inter-layer relationships
- isolate exceptions for review and correction
- create standardized outputs for audit and reporting
- support repeatable data quality workflows across multiple geodatabases

---

## Requirements

Before using the framework, make sure you have:

- **ArcGIS Pro** installed
- access to the **ArcPy** environment included with ArcGIS Pro
- one or more **File Geodatabases (.gdb)** to process
- permission to read input folders and write outputs
- **Git** installed only if you want to clone the repository from the command line

No separate Python installation is required for standard toolbox use when running inside ArcGIS Pro.

---

## Get the files from GitHub

You can retrieve the framework from GitHub in either of the following ways.

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

To make execution easier:

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
3. Run **Feature Count** to compare feature distributions, detect outliers, and verify data completeness across the selected ROIs.
4. Review the generated comparative output.
5. Run **Validate Rules** to perform rule-based QA/QC checks.
6. Review the output report and any generated exception layers.
7. Correct source data as needed.
8. Re-run validation until the dataset meets your project standards.

---

## Run the Feature Count tool

### Purpose

The Feature Count tool functions as a comparative analytical engine for multi-region geospatial datasets.

Rather than serving only as a checklist for data availability, it helps users examine how feature classes vary across different ROIs, towns, cities, zones, or other spatial units. This enables analysts to detect unusual counts, compare thematic distributions, and derive context from differences in the data.

For example:

- a high count of **Tree** features in one ROI relative to others may indicate a forest patch, plantation zone, protected green area, or park-dominant region
- an unusually low **Building** count combined with high **Waterbody** coverage may suggest a reservoir or open-zone landscape
- an unexpected zero count in an important class may indicate either a genuine absence or a data capture issue that needs review

This makes the Feature Count tool useful for both QA/QC and first-level spatial interpretation.

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

The tool generates a summary report, typically as a CSV, containing feature counts for the discovered feature classes across the selected geodatabases or ROIs.

This output can be used to:

- compare counts across multiple regions
- identify outliers in specific feature classes
- detect missing or empty datasets
- flag unusual spatial patterns for further review
- support interpretation of the underlying geographic character of an ROI
- establish a comparative baseline before running validation rules

### How to interpret the results

Feature counts should not always be treated as simple pass/fail indicators.

Instead, review them comparatively:

- compare one ROI against the rest of the row or batch
- look for extreme highs or lows in key feature classes
- check whether the outlier is explainable by geography, land use, landscape type, or settlement pattern
- use the results as an analytical cue before deciding whether deeper QA/QC is needed

The comparative value of the Feature Count tool is often highest when it is run across multiple related geodatabases rather than just one.

---

## Run the Validate Rules tool

### Purpose

The Validate Rules tool runs rule-based QA/QC checks on the selected geodatabases.

It is intended to identify non-conformities in a structured and repeatable way by evaluating configured rules related to:

- spatial relationships
- geometry conditions
- duplicates
- attribute filters
- thresholds for small features
- topology-oriented checks where applicable

This tool is best used after Feature Count has already helped establish data completeness and cross-ROI context.

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

In many workflows, validation outputs are reviewed alongside the source geodatabases to support correction and re-validation.

---

## Output review

After the tools finish running:

- review the **CSV output** for summary results
- inspect any generated **exception layers**, **review tables**, or **QA/QC outputs** inside ArcGIS Pro
- verify that outputs were written to the location defined in the tool parameters
- use the results to correct the source data and rerun the checks where needed

A practical review cycle is:

1. run Feature Count
2. review cross-ROI differences and completeness
3. run Validate Rules
4. inspect exceptions
5. correct data
6. rerun validation

---

## Suggested analytical workflow

A strong workflow for larger programs is to use the two tools together:

### Step 1: Comparative screening with Feature Count

Use Feature Count to understand whether one ROI or geodatabase behaves differently from the rest. At this stage, you are asking questions such as:

- Does one ROI have an unusually high or low count for a given feature class?
- Does the distribution look reasonable relative to surrounding areas or comparable ROIs?
- Is the outlier likely caused by geography, land use, landscape character, or data omission?

### Step 2: QA/QC validation with Validate Rules

Once the broader pattern is understood, use Validate Rules to determine whether the dataset also contains rule-based geometry, attribute, or spatial inconsistencies that need correction.

This two-step approach is particularly useful because not every outlier is an error, and not every error is visible from counts alone.

---

## Adapting the framework for different geospatial applications

This framework is intentionally structured so it can be extended beyond a single project context. It can be adapted to different applications by changing schema references, rule logic, and threshold values.

### Common adaptation scenarios

- changing feature class names
- changing attribute field names
- aligning rules to a new data model
- adjusting thresholds for different map scales or feature types
- adding new inter-layer logic for a specific business workflow
- replacing project-specific naming conventions with a new project standard

### Example domains where it can be reused

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
- replace project-specific terms with a new domain vocabulary

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
- compare multiple related ROIs together whenever possible
- treat count outliers as analytical signals, not immediate errors
- test changes on a small sample before running a large batch
- keep output folders separate from source data folders
- maintain a consistent folder structure for repeatable runs
- store updated rule logic in version control
- document project-specific customizations for future users

---

## Limitations and notes

- The framework depends on **ArcGIS Pro** and **ArcPy**.
- Validation behavior depends on the configured rule logic and schema mappings.
- Some complex QA/QC cases may still require analyst review after automated screening.
- Feature count outliers do not automatically indicate data issues; they may represent genuine geographic or thematic variation.
- Thresholds and rule selections should be reviewed before operational use in a new application area.

---

## Summary

This repository provides a practical ArcGIS Pro QA/QC framework for large-scale geospatial processing. It supports comparative feature analysis, rule-based validation, batch execution, and review-ready outputs while remaining flexible enough to be adapted across different geospatial domains.

Rather than being restricted to a single project context, the framework should be treated as a reusable foundation for structured geospatial QA/QC workflows in any environment where scalable validation, consistency, and operational clarity are required.

---

## Author

Asish Kandikonda | asishk009 | asishkandikonda@gmail.com

Guide: M Ramadasu | Scientist/Engineer ‘SF’ | Urban Studies Division | National Remote Sensing Center, Indian Space Research Organization
