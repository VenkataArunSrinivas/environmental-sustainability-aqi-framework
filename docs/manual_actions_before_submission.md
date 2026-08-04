# Manual Actions Before Submission

Complete every item below **before exporting the final PDF submitted to Olympus**.

## 1. Obtain mentor approval for the data-driven scope refinements

The current interim report proposes four material refinements discovered during the data audit:

1. coal **consumption at thermal power stations** instead of coal production/mining;
2. Maharashtra and Gujarat as the primary states, with Odisha retained only if coverage becomes adequate;
3. station-month outcomes with state-month industrial exposures, rather than treating repeated state-month values as independent;
4. validated AQI as the preferred outcome, with PM2.5 or PM10 as a formally approved fallback if AQI cannot be reconstructed defensibly.

Record the mentor decision in `docs/scope_change_record.md`. After approval, synchronize the following report locations:

- title page and running project title;
- **Introduction**: final paragraph of Background and Context, Problem Statement, and Purpose of the Study;
- **Scope and Objectives**: scope paragraph and Tables 2-5;
- **Data Description**: Dataset Overview, Tables 8-9, and GitHub Data Availability Statement;
- **Modelling**: Tables 12-14 and the target-leakage paragraph;
- **Preliminary Results**, **Interim Limitations and Risks**, and **Next Steps**;
- repository files: `README.md`, `config/project_config.yaml`, `docs/research_questions.md`, and `docs/scope_change_record.md`.

If the mentor does **not** approve the refinements, do not submit the revised scope as though it were final. Revert the report and configuration to the approved synopsis or explicitly label the changes as pending.

## 2. Upload and verify the GitHub package

1. Extract this package and copy its contents into the root of `environmental-sustainability-aqi-framework`.
2. Preserve the original government workbooks already under `data/raw/`.
3. Remove the obsolete empty `code/sample` path after the new `src/`, `scripts/`, `notebooks/`, and `tests/` folders are visible.
4. Run the commands in `UPLOAD_INSTRUCTIONS.md` and confirm that all tests pass.
5. Open the repository in a signed-out/private browser window and verify that the evaluator can access the README, code, documentation, figures, tables, and report without requesting permission.

## 3. Replace the repository evidence screenshot

After the final GitHub upload, take a fresh browser screenshot showing:

- repository name;
- `Public` label;
- most recent commit time;
- top-level folders/files, including `config`, `data`, `docs`, `notebooks`, `outputs`, `reports`, `scripts`, `src`, and `tests`.

Replace **Appendix A, Figure A2** in the editable Word report with this screenshot. Keep the APA figure number, italicized title, and note. Do not paste the screenshot without a figure label and in-text reference.

## 4. Add the final Git commit identifier

After the last commit, copy the short commit hash and add the following sentence at the end of the **GitHub Repository and Data Access** section on page 2:

> The repository version reviewed for this submission is commit `<short-hash>` dated `<Month Day, Year>`.

Copy the final PDF and editable source to `reports/` before making this last commit. Then update the hash in the report, export the submission PDF, and make one final documentation commit. If the hash necessarily changes because the PDF was added, state the hash of the code/data version used for analysis and label it clearly.

## 5. Confirm title-page and administrative details

Verify these exact fields on page 1:

- project title matches the mentor-approved scope;
- student name;
- Walsh College;
- `QM640: Data Analytics Capstone`;
- mentor name: `Mr. Jainesh Garg`;
- term: `Term 3`;
- submission date.

## 6. Complete the evidence required before claiming final RQ results

The interim report intentionally does not present final sector-association results. Before the final report, the repository must contain:

- a continuous thermal-generation series using one consistent report definition;
- matching monthly coal-consumption statements and a verified plant-to-state mapping;
- meteorological controls with documented source, units, and aggregation;
- a validated AQI derivation or formal mentor approval to use PM2.5/PM10;
- a harmonized panel with duplicate, missingness, coverage, and unit checks;
- chronological/grouped validation and final model outputs.

Do not replace missing industrial values with zero, interpolate missing months without justification, use same-period pollutant components as AQI predictors, or report the interim PM2.5 smoke-test metrics as final RQ4 performance.

## 7. Final PDF quality check

Submit only the PDF to Olympus. Before upload:

1. open the PDF outside Microsoft Word;
2. confirm all 37 pages open and page numbers are visible;
3. verify every table and figure is readable at 100% zoom;
4. test the GitHub hyperlink;
5. confirm APA 7 citations and hanging indents in the References section;
6. search the PDF for `TBD`, `TODO`, `<`, `MANUAL ACTION`, and `Replace this` and remove any unintended placeholder text;
7. keep the DOCX locally as the editable source but do not upload it to Olympus unless separately requested.
