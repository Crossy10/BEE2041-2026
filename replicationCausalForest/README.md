# Replication of Oreopoulos (2011): A Machine Learning Extension

**Author:** Damian Clarke  
**Date:** 2026-03-20  
**Contact:** [dcc213@exeter.ac.uk](mailto:dcc213@exeter.ac.uk)

---

## Table of Contents

1. [Overview](#overview)
2. [Data](#data)
3. [Repository Structure](#repository-structure)
4. [Requirements](#requirements)
5. [Running Instructions](#running-instructions)
6. [Outputs](#outputs)
7. [Methods](#methods)
8. [References and Resources](#references-and-resources)

---

## Overview

This project replicates and extends the analysis from:

> Oreopoulos, Philip. 2011. "Why Do Skilled Immigrants Struggle in the Labor Market? A Field Experiment with Thirteen Thousand Resumes." *American Economic Journal: Economic Policy*, 3(4): 148–171. [https://doi.org/10.1257/pol.3.4.148](https://www.aeaweb.org/articles?id=10.1257/pol.3.4.148)

The paper uses a large-scale field experiment — sending over 13,000 fictitious resumes to employers — to study labour market discrimination against skilled immigrants in Canada. This replication extends the original analysis to examine **heterogeneity in treatment effects**: does the effect of having a Canadian name on callback rates vary across applicant characteristics?

This is done using two complementary approaches:

- **OLS regression** with interaction terms, to test for heterogeneity along specific, pre-specified dimensions (gender, BA quality).
- **Causal Forests** (via `econml`), a machine learning method that estimates individualised treatment effects (CATEs) without requiring pre-specification of interaction terms.

---

## Data

The dataset (`Oreopoulos2011skilled.dta`) comes from the published replication materials for Oreopoulos (2011). It is in Stata `.dta` format and is read directly using `pandas`.

The key variables used in this analysis are:

| Variable | Description |
|---|---|
| `callback` | Outcome: whether the resume received a callback (×100 for percent) |
| `canadian_name` | Treatment: whether the resume had a Canadian-sounding name |
| `female` | Applicant gender |
| `ba_quality` | Quality of undergraduate degree |
| `extracurricular_skills` | Extracurricular activities listed |
| `language_skills` | Language skills listed |
| `ma` | Whether applicant has a Masters degree |
| `same_exp` | Whether work experience is in the same field |
| `exp_highquality` | Whether work experience is rated high quality |
| `reference` | Whether references are included |
| `accreditation` | Whether professional accreditation is listed |
| `legal` | Whether applicant has legal right to work |

**Note:** The data file is not included in this repository and must be obtained from the original replication materials, available at the AEA website linked above. Once obtained, place the file at `data/Oreopoulos2011skilled.dta`.

---

## Repository Structure

```
.
├── README.md
├── Makefile
├── immigrationHeterogeneity.tex       # Main LaTeX write-up
├── refs.bib                           # Bibliography
├── data/
│   └── Oreopoulos2011skilled.dta      # Raw data (not tracked — obtain separately)
├── source/
│   └── immigrantEffects.py            # Main analysis script
└── results/
    ├── figures/                       # All generated figures (.pdf)
    └── tables/                        # All generated tables (.tex)
```

All raw data lives in `data/`, all source code in `source/`, and all output is automatically exported to `results/`. The LaTeX write-up reads table and figure files directly from `results/`, so **running the Python script before compiling LaTeX is essential**.

---

## Requirements

### System

- Python 3 (tested on **Python 3.10.12**, Linux)
- XeLaTeX (for compiling the write-up)
- `make` (optional, but recommended)

### Python Packages

Install all dependencies via pip:

```bash
pip install matplotlib==3.10.7 numpy==1.26.4 pandas==2.3.3 scikit-learn==1.4.2 \
            shap==0.49.1 econml==0.15.0 statsmodels==0.14.4 pystout==0.0.8
```

Or install without pinned versions (results may differ slightly):

```bash
pip install matplotlib numpy pandas scikit-learn shap econml statsmodels pystout
```

The exact versions used to produce the original results are listed below:

| Package | Version |
|---|---|
| `matplotlib` | 3.10.7 |
| `numpy` | 1.26.4 |
| `pandas` | 2.3.3 |
| `scikit-learn` | 1.4.2 |
| `shap` | 0.49.1 |
| `econml` | 0.15.0 |
| `statsmodels` | 0.14.4 |
| `pystout` | 0.0.8 |

---

## Running Instructions

### Step 0: Configure the root directory

Before running anything, open `source/immigrantEffects.py` and update the `ROOT` variable (line 29) to point to the top level of this repository on your machine:

```python
ROOT = "/your/path/to/this/project/"
```

### Option A: Using `make` (recommended)

If `make` is available, simply run from the top level of the repository:

```bash
make
```

This will automatically:
1. Run the Python analysis script (if outputs are out of date).
2. Compile the LaTeX write-up into a PDF (including bibliography).

To remove compiled LaTeX auxiliary files:

```bash
make clean
```

To run only the Python script without compiling LaTeX:

```bash
make run_python
```

### Option B: Manual steps

If `make` is not available, run the following steps in order:

**1. Run the Python script:**

```bash
python3 source/immigrantEffects.py
```

This will populate `results/figures/` and `results/tables/` with all output files.

**2. Compile the LaTeX write-up:**

```bash
xelatex immigrationHeterogeneity.tex
bibtex immigrationHeterogeneity.aux
xelatex immigrationHeterogeneity.tex
xelatex immigrationHeterogeneity.tex
```

Four passes are needed to resolve all cross-references and bibliography entries correctly.

---

## Outputs

Running the pipeline produces the following files:

### Figures (`results/figures/`)

| File | Description |
|---|---|
| `treatmentCATEs.pdf` | Histogram of estimated individual treatment effects (CATEs), with ATE marked |
| `orderedCATEs.pdf` | Treatment effects sorted by magnitude, with 95% confidence intervals |
| `CATEbyGroup.pdf` | Distribution of CATEs split by BA quality (high vs. low) |

### Tables (`results/tables/`)

| File | Description |
|---|---|
| `regressionTable.tex` | OLS results across six specifications: baseline, with controls, and with interaction terms for gender and BA quality |

---

## Methods

### OLS with Interaction Terms

Six OLS specifications are estimated (using `statsmodels`):

- **Specifications 1–2:** Baseline — treatment (`canadian_name`) with and without controls.
- **Specifications 3–4:** Add a `canadian_name × female` interaction term.
- **Specifications 5–6:** Add a `canadian_name × ba_quality` interaction term.

This tests whether the callback penalty for a non-Canadian name differs by gender or education quality. A Breusch-Pagan test for heteroscedasticity is also reported.

### Causal Forests

A Causal Forest is estimated using `econml`'s `CausalForestDML`, which uses a double machine learning (DML) framework. Gradient Boosting models are used for both the outcome and treatment nuisance functions. This approach:

- Makes no assumptions about the functional form of heterogeneity.
- Estimates a Conditional Average Treatment Effect (CATE) for every observation.
- Allows comparison of average CATEs across subgroups (e.g., high vs. low BA quality).

For full methodological details, see the [EconML documentation](https://econml.azurewebsites.net/spec/estimation/forest.html).

> **Note:** The SHAP value analysis (section 6 of the script) is commented out by default as it is computationally intensive. It can be enabled by uncommenting the relevant block in `source/immigrantEffects.py`.

---

## References and Resources

- **Paper:** Oreopoulos, P. (2011). Why Do Skilled Immigrants Struggle in the Labor Market? A Field Experiment with Thirteen Thousand Resumes. *AEJ: Economic Policy*, 3(4), 148–171. [https://doi.org/10.1257/pol.3.4.148](https://www.aeaweb.org/articles?id=10.1257/pol.3.4.148)

- **EconML Causal Forest:** [https://econml.azurewebsites.net/spec/estimation/forest.html](https://econml.azurewebsites.net/spec/estimation/forest.html)

- **pystout (LaTeX table export):** [https://github.com/stephenholtz/pystout](https://github.com/stephenholtz/pystout)
