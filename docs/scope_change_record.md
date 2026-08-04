# Interim Scope Change Record

**Project:** Environmental Sustainability: An Explainable AI Framework for Assessing Associations Between Thermal Power Generation, Coal Consumption, and Air Quality in Selected Indian States  
**Status:** Provisional - pending mentor review before final model estimation  
**Recorded:** August 4, 2026  
**Reason for record:** Data availability and data-quality findings identified during the interim audit

## Governance Statement

The refinements documented below are data-driven working decisions used for the interim report. They are not represented as formally mentor-approved changes. They preserve the original project objective of examining relationships between industrial activity and air quality while aligning the proposed analysis with the government data collected so far. The decisions will be reviewed with the mentor before final model estimation and will be confirmed, revised, or reverted in the final report as appropriate.

## Proposed Interim Refinements

| Scope item | Previously submitted synopsis | Interim data-audit finding | Provisional working treatment | Final decision point |
|---|---|---|---|---|
| Second industrial driver | Coal production or mining activity | The collected monthly power-sector files report coal receipts, coal consumption, imported coal, and closing stock at thermal power stations rather than state coal production | Use **coal consumption at thermal power stations** as the measurable operational driver | Confirm with the mentor before final panel construction and model estimation |
| State coverage | Maharashtra, Gujarat, and Odisha as fixed study states | Maharashtra and Gujarat have stronger pollutant coverage; Odisha has a substantially shorter usable period and only eight state-month monitoring summaries under the current provisional readiness rule | Use Maharashtra and Gujarat as the current core analytical scope; retain Odisha as a conditional extension or sensitivity analysis | Include Odisha only if it meets the same common-period, completeness, unit, and station-coverage requirements applied to the core states |
| Unit of analysis | State-month | Air-quality data are available at station-day level, while industrial drivers are expected at state-month level; repeating one exposure value across stations does not create independent exposure periods | Aggregate air quality to **station-month** and link it to grouped state-month industrial exposures; report both station-month row count and unique state-month exposure count | Confirm the final multilevel or grouped specification after the integrated panel is built |
| Primary air-quality outcome | Monthly AQI | The collected air-quality workbooks contain pollutant concentrations but no reported AQI field; units, averaging periods, and CPCB derivation requirements still require verification | Retain AQI as the preferred outcome only if official reported AQI or a defensible CPCB-compliant derivation is available; otherwise use PM2.5 or PM10 as a clearly disclosed fallback outcome | Confirm outcome after source metadata and unit validation; revise title and research questions if a fallback is formally adopted |
| Analytical period | January 2019-December 2023 target | Current files span different and discontinuous periods; a single matched period has not been established | Treat **2019-2026 as the data-search window** and select the longest defensible contiguous common period, currently anticipated to be approximately 12-18 months | Confirm only after air-quality, thermal-generation, coal-consumption, and meteorological availability are verified |
| Interpretation | Industrial impact | The planned design is observational and aggregate, with potential omitted-source and ecological limitations | Use **associations**, predictive relationships, and model explanations; do not claim plant-level causality or source apportionment | Maintain this non-causal interpretation in all final outputs |

## Inclusion and Quality Controls

Odisha or any replacement/additional state will be included in the primary analysis only when all applicable requirements are met:

- at least 12 common contiguous months across the air-quality, thermal-generation, coal-consumption, and weather datasets;
- at least 75% valid daily observations within retained station-month records, subject to sensitivity testing and source-specific validity rules;
- preferably at least two valid monitoring stations per retained state-month;
- verified and consistent pollutant units and averaging periods;
- verified thermal- and coal-station-to-state mappings;
- no prolonged interval in which all required pollutant values are missing; and
- sufficient unique state-month exposure periods for a parsimonious model.

## Current Submission Treatment

For the interim submission:

- the report title uses **selected Indian states** rather than presenting Odisha as guaranteed;
- thermal power generation and coal consumption at thermal power stations are presented as the two current focal industrial drivers;
- Maharashtra and Gujarat are identified as the core states;
- Odisha is explicitly conditional;
- the 2019-2026 range is described as a search window rather than a confirmed analytical period;
- 12-18 months is described as anticipated rather than confirmed;
- final modeling and research conclusions are not claimed; and
- all material refinements are labeled provisional and pending mentor review before final model estimation.

## Mentor Review Record

| Review item | Decision | Date | Notes |
|---|---|---|---|
| Coal consumption as the second operational driver | Pending |  |  |
| Maharashtra and Gujarat as core states; Odisha conditional | Pending |  |  |
| Station-month analytical unit with grouped state-month exposures | Pending |  |  |
| AQI derivation or PM2.5/PM10 fallback outcome | Pending |  |  |
| Final common analytical period | Pending |  |  |

