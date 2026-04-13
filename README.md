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
