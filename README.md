# Tax Report Generator — Agentic AI (Yantra)

*Repository: `tax_report_generator_agentic_ai`*

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Powered by Groq](https://img.shields.io/badge/LLM-Groq%20API-orange.svg)
![Status](https://img.shields.io/badge/status-prototype%2Fdemo-yellow.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

> An agentic AI system that takes a taxpayer's plain-English rental tax filing, cross-audits it against official municipal records, and produces a fully calculated, human-readable municipal tax report — modeled on a simulated Nepali metropolitan city (Kathmandu / Lalitpur) house-rent tax system.

| | |
|---|---|
| **Language** | Python 3 |
| **Interface** | Command-line (interactive prompts) |
| **AI Provider** | [Groq](https://groq.com) API |
| **Model used** | `qwen/qwen3.8-27b` |
| **Domain** | Municipal rental/house tax audit (simulated Nepali metropolitan city context) |
| **Input** | Property ID, PAN (taxpayer) ID, free-text filing declaration |
| **Output** | Plain-text (`.txt`) municipal tax report written to disk |
| **License** | Proprietary — All Rights Reserved (see [License](#license)) |

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [How It Works](#how-it-works)
4. [Key Features](#key-features)
5. [Project Structure](#project-structure)
6. [Requirements](#requirements)
7. [Installation and Setup](#installation-and-setup)
8. [Usage](#usage)
9. [Example Input and Output](#example-input-and-output)
10. [Understanding the Report](#understanding-the-report)
11. [Tax Calculation Logic](#tax-calculation-logic)
12. [The Mock Government Dataset](#the-mock-government-dataset)
13. [Who This Is For](#who-this-is-for)
14. [Design Philosophy](#design-philosophy)
15. [Limitations and Notes](#limitations-and-notes)
16. [Possible Future Enhancements](#possible-future-enhancements)
17. [Disclaimer](#disclaimer)
18. [License](#license)
19. [Author](#author)

---

## Overview

**Tax Report Generator** is a small **agentic AI** proof-of-concept that plays the role of a **Municipal Tax Audit Officer**.

A taxpayer describes their rental income filing in their own words — e.g. *"I collect 25,000 rupees a month in rent and I'd like the non-profit discount"* — along with their **Property ID** and **PAN (Permanent Account Number)**. The system then:

1. Looks up the *actual* official records for that property and taxpayer (from a simulated municipal database),
2. Sends the taxpayer's free-text claim, together with the official records, to a large language model acting as an auditor,
3. Has the model return a **strict, structured JSON verdict** (is the declared rent correct? is the discount claim legitimate? is there a violation?),
4. Then — critically — hands the *numbers* off to **plain deterministic Python code**, which independently computes the actual tax, discount, and penalty amounts,
5. And finally assembles everything into a formatted **Municipal Tax Report** text file.

The project is built around a fictional/simulated Nepali context: **Kathmandu Metropolitan City** and **Lalitpur Metropolitan City**, four wards, NPR (Nepalese Rupee) currency, 9-digit IRD-style PAN numbers, and a 10% house-rent tax rate with a 20% under-reporting penalty — all defined in a small mock "government database" module.

---

## Quick Start

For readers who just want to run it immediately (see [Installation and Setup](#installation-and-setup) for the full walkthrough):

```bash
# 1. Move into the project folder (note the spaces/parentheses — quote the path)
cd "Agentic AI (Yantra)"

# 2. Install the two external dependencies
pip install groq python-dotenv

# 3. Put your Groq API key in an .env file, e.g.:
echo 'GROQ_API_KEY="your_groq_api_key"' > .env

# 4. Open main.py and set KEY_PATH and REPORT_PATH (see below) — this is required,
#    the script will not run with the placeholder values left in place.

# 5. Run it
python main.py
```

When prompted, try Property ID `PROP_KTM_101`, PAN `PAN600123456`, and a filing declaration like *"My monthly rent is 25000 and I want the non-profit discount"* — this reproduces the exact scenario already included in the repo at `Agentic AI (Yantra)/output report/example_report.txt` (see [Example Input and Output](#example-input-and-output)).

---

## How It Works

The pipeline is a single linear run through `main.py`, orchestrating `records.py` (data) and `formats.py` (prompt + report templates):

```text
User (CLI)
   │
   ▼
[1] load_key() — reads GROQ_API_KEY from your .env file (KEY_PATH)
   │
   ▼
[2] get_user_prompt() — prompts for Property ID, re-asks until it
    exists in WARD_REGISTRY
   │
   ▼
[3] get_user_prompt() — prompts for PAN ID, re-asks until it
    exists in PAN_REGISTRY
   │
   ▼
[4] get_user_prompt() — prompts for the filing declaration
    (free-form natural language, typed by the taxpayer)
   │
   ▼
[5] get_required_data() — pulls the property record, that ward's
    rent standards, the PAN record, the tax rates, and the discount
    registry, and serializes them into the system prompt as
    "OFFICIAL GOVERNMENT RECORDS"
   │
   ▼
[6] get_json_output() — calls the Groq chat completion API
    (model: qwen/qwen3.8-27b, temperature 0.0, JSON mode,
    reasoning hidden) → the model returns a strict JSON verdict
   │
   ▼
[7] extract_required_json_data() — pulls declared rent, discount
    claim/approval, violation status/reasons, and any extra notes
    out of that JSON
   │
   ▼
[8] calculate() — pure, deterministic Python: computes the annual
    taxable rent, base tax (10%), any discount, any 20%
    under-reporting penalty, and the final total — the LLM never
    touches the arithmetic
   │
   ▼
[9] report_format() — assembles everything into the final
    plain-text Municipal Tax Report
   │
   ▼
[10] Report written to REPORT_PATH and a confirmation is printed
     to the console
```

`main.py` has no `if __name__ == "__main__":` guard — it is a straight top-to-bottom script. Running `python main.py` executes the whole flow; it is not meant to be imported as a module.

---

## Key Features

- **Natural-language filing intake** — taxpayers describe their situation in plain English instead of filling out a rigid form.
- **Automatic ID validation** — Property ID and PAN ID are checked against the mock registries before any AI call is made, with the CLI re-prompting until valid values are entered.
- **LLM-powered compliance reasoning** — a single Groq call performs three checks in one structured pass: rent-correctness, non-profit discount eligibility, and overall violation detection.
- **Deterministic, auditable math** — every rupee in the final report (base tax, discount, penalty, total) is computed by ordinary Python arithmetic, not generated by the model. This means the same inputs always produce the same numbers.
- **Automatic 20% under-reporting penalty** whenever the declared rent is below the ward's legal minimum standard for that property type.
- **50% non-profit educational discount** logic, cross-verified against the PAN registry's `is_non_profit` flag and `category` field.
- **Self-contained mock government database** — 10 sample properties across 4 wards, 10 sample PAN taxpayer entities, ward-by-property-type rent floors, and a discount registry, all in a single `records.py` file, so the tool runs with zero external database setup.
- **Human-readable output report** — a clean, structured `.txt` file suitable for printing or filing, saved automatically to disk.

---

## Project Structure

```text
tax_report_generator_agentic_ai-main/
├── Agentic AI (Yantra)/
│   ├── main.py                    # Entry point — orchestrates the full audit pipeline
│   ├── formats.py                 # System prompt template + report Parameters/formatter
│   ├── records.py                 # Mock "official government" datasets
│   ├── output report/
│   │   └── example_report.txt     # A real, pre-generated sample report
│   └── .gitignore/
│       └── .env                   # Placeholder for GROQ_API_KEY (see note below)
├── .gitignore                     # Standard Python .gitignore (root)
├── LICENCE                        # Proprietary license
└── README.md                      # This file
```

**Note on the `.env` location:** in this repository, the placeholder `.env` file lives inside a folder that is literally named `.gitignore/` (not a `.gitignore` *file* — a folder with that name), rather than at the project root. You can leave it there, or move/rename it to a conventional `Agentic AI (Yantra)/.env` — either works, as long as the `KEY_PATH` constant in `main.py` (see [Installation and Setup](#installation-and-setup)) points to wherever it actually lives.

---

## Requirements

- **Python 3.9+** recommended (the code uses f-strings and `dataclasses`, so anything 3.7+ will technically run it, but a current interpreter is recommended). No specific version is pinned in the repo.
- **External packages** (not bundled — no `requirements.txt` is included in the repo):
  - [`groq`](https://pypi.org/project/groq/) — official Groq Python SDK
  - [`python-dotenv`](https://pypi.org/project/python-dotenv/) — loads the `.env` file
- **A Groq API key** — free tier available at [console.groq.com](https://console.groq.com).
- **An internet connection** — the script makes a live call to the Groq API every time it runs; it will not work offline.
- Standard library only, otherwise: `os`, `sys`, `json`, `dataclasses`.

---

## Installation and Setup

1. **Get the code**
   Download or clone the repository, then move into the project's actual source folder:
   ```bash
   cd "Agentic AI (Yantra)"
   ```
   (The folder name has spaces and parentheses — always quote it in shell commands.)

2. **(Optional but recommended) create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install groq python-dotenv
   ```

4. **Set up your Groq API key**
   Create (or reuse) an `.env` file containing:
   ```
   GROQ_API_KEY="your_groq_api_key"
   ```
   Get a key from the [Groq Console](https://console.groq.com) if you don't have one.

5. **Edit the two path constants at the top of `main.py`.** This is the most important setup step and the one most likely to trip up a first run — the script ships with literal placeholder strings that **must** be replaced before it will work:
   ```python
   KEY_PATH = "path_to_groq_api_key_env_file"
   REPORT_PATH = "path_to_save_tax_report"
   ```
   For example, if you keep the `.env` where it currently sits and want reports saved into the existing `output report/` folder:
   ```python
   KEY_PATH = ".gitignore/.env"
   REPORT_PATH = "output report/my_tax_report.txt"
   ```
   `REPORT_PATH` must include the **filename**, not just a folder — `main.py` creates any missing parent directories automatically (`os.makedirs(..., exist_ok=True)`) but it still needs a full file path to write to.

6. **Run it**
   ```bash
   python main.py
   ```

There are currently no command-line arguments, environment-variable overrides, or config files for these two paths — they are hardcoded constants you edit directly in the source.

---

## Usage

Once running, `main.py` walks you through three interactive prompts:

| Prompt | What to enter | Validation |
|---|---|---|
| `Enter your Property ID (for eg: PROP_KTM_101):` | A Property ID from the mock registry | Re-prompts until the ID exists in `WARD_REGISTRY` |
| `Enter your PAN ID (for eg: PAN600123456):` | A PAN from the mock registry | Re-prompts until the ID exists in `PAN_REGISTRY` |
| `Enter your filing details in simple language:` | A free-text description of your rent and any claims | Not validated — passed straight to the AI auditor |

Both IDs are automatically upper-cased and trimmed, so `prop_km_101` and `PROP_KTM_101` are treated the same. See [The Mock Government Dataset](#the-mock-government-dataset) below for the full list of valid Property IDs and PAN IDs you can experiment with — for example:

- Declare a rent **below** the ward's standard for that property type → triggers the 20% under-reporting penalty.
- Declare a rent **at or above** the standard → no penalty.
- File under a PAN with `is_non_profit: true` **and** `category: "Educational Trust School"` while requesting the discount → the 50% discount should be approved (only two PANs in the sample data currently satisfy both conditions — see [The Mock Government Dataset](#the-mock-government-dataset)).
- File under any other PAN while requesting the discount → it should be rejected.

The final report is written to whatever path you configured in `REPORT_PATH`, and a confirmation line — `Your Tax Report has been generated.` — is printed to the console.

---

## Example Input and Output

Below is the exact scenario already captured in the repository at `Agentic AI (Yantra)/output report/example_report.txt`, reconstructed as a full terminal session.

### Sample terminal session

```text
Successfully loaded the API key.

Enter your Property ID (for eg: PROP_KTM_101): PROP_KTM_101
Property data found.

Enter your PAN ID (for eg: PAN600123456): PAN600123456
PAN ID found.

Enter your filing details in simple language:
We operate a community school. Our collected monthly rent is 25,000 NPR. We request our 50% non-profit educational discount.

Your Tax Report has been generated.
```

### Resulting report (`output report/example_report.txt`)

```text
FILING DETAILS:
We operate a community school. Our collected monthly rent is 25,000 NPR. We request our 50% non-profit educational discount.


MUNICIPAL TAX REPORT

Target Property: PROP_KTM_101
Ward: WARD_1
Taxpayer PAN: PAN600123456

1. Declared Rent Correctness Check
- Declared Rent: NPR 25,000.00 / month
- Official Property Classification: Commercial
- Legal Minimum Rent Floor: NPR 60,000.00 / month
- Findings: UNDER REPORTED: The property is registered as Commercial with a standard rent of 60000.0, but the user declared 25000.0.

2. Non-Profit Discount Verification
- User Claim: 50% non-profit educational discount for community school
- Official PAN Registry Record: {'name': 'Sagarmatha Commercial Bank Ltd.', 'is_non_profit': False, 'category': 'Private Bank Enterprise'}
- Finding: REJECTED: The PAN registry shows the entity is a Private Bank Enterprise and is not a non-profit educational trust.

3. Violation Determination & Reasons
Status: TAX VIOLATION DETECTED
Reasons:
- User under-reported rent by 35000.0 (declared 25000.0 vs standard 60000.0) and falsely claimed a non-profit discount for a commercial bank entity.

4. Final Verdict & Corrected Demand Note
- Adjusted Monthly Base Rent: NPR 60,000.00
- Annual Base Taxable Income: NPR 720,000.00
- Annual Base Tax Due (10% House Rent Tax Rate): NPR 72,000.00
- Tax Discount Amount: NPR 0.00
- Tax Amount After Discount: NPR 72,000.00
- Under-Reporting Penalty Fine (20%): NPR 14,400.00
- Tax Amount After Penalty: NPR 86,400.00

TOTAL REVISED TAX DEMAND DUE: NPR 86,400.00

Additional Information/Request: None
```

This example deliberately shows the system catching **two problems at once**: the taxpayer under-reported their rent (PROP_KTM_101 is officially a Commercial property, so its true rent floor is far higher than 25,000), *and* they tried to claim an educational non-profit discount despite the PAN on file belonging to a commercial bank. Both findings are visible in the report, and the final tax demand reflects the corrected rent plus the 20% penalty — with the (rejected) discount contributing NPR 0.

---

## Understanding the Report

Every generated report follows the same four-part structure defined in `formats.py`:

1. **Filing Details** — a verbatim echo of what the taxpayer originally typed, kept at the top for reference.
2. **Declared Rent Correctness Check** — compares the declared monthly rent against the property's official classification and that ward's legal minimum rent floor, plus the AI's plain-English findings (`CORRECT REPORTED` or `UNDER REPORTED`, with an explanation).
3. **Non-Profit Discount Verification** — restates the user's discount claim (if any), the official PAN registry record on file, and whether the discount request was `APPROVED` or `REJECTED`.
4. **Violation Determination & Reasons** — an overall status (`NO VIOLATION` or `TAX VIOLATION DETECTED`) with a written explanation.
5. **Final Verdict & Corrected Demand Note** — the fully itemized calculation: adjusted monthly rent, annual taxable income, base tax, discount amount, penalty amount, and the final **Total Revised Tax Demand Due**.

---

## Tax Calculation Logic

All of the financial math happens in `calculate()` inside `main.py`, using values from `TAX_RATES` and `DISCOUNT_REGISTRY` in `records.py`. It is deliberately kept out of the LLM's hands. The formula, step by step:

```
adjusted_monthly_rent   = RENT_STANDARDS[ward][property_type]     # the official floor — see note below
annual_taxable_rent     = adjusted_monthly_rent × 12
annual_base_tax         = annual_taxable_rent × 10%               # TAX_RATES["Rent_Tax_Rate"]

if a discount is approved:
    discount_amount      = annual_base_tax × discount_rate         # e.g. 0.50 for the non-profit educational discount
    amount_after_discount = annual_base_tax − discount_amount
else:
    amount_after_discount = annual_base_tax

if declared_rent < adjusted_monthly_rent:                          # under-reporting
    penalty_amount        = amount_after_discount × 20%             # TAX_RATES["False_Reporting_Penalty"]
    total_due              = amount_after_discount + penalty_amount
else:
    total_due              = amount_after_discount
```

> **Important nuance:** the *adjusted monthly rent* used for the tax base is always the ward's official standard for that property type — **not** the taxpayer's declared figure, even when the declared rent is *higher* than the standard. The declared rent is only used for one purpose: deciding whether the 20% under-reporting penalty applies (i.e., whether it falls below the standard).

### Worked example (a compliant filing, no violation)

To illustrate the "clean" path — no under-reporting, no discount claimed — here's `PROP_KTM_105` (a Residential property in `WARD_3`, where the standard Residential rent is NPR 15,000/month), with a taxpayer who declares rent exactly at the legal floor and requests no discount:

| Step | Value |
|---|---|
| Adjusted monthly rent | NPR 15,000.00 |
| Annual taxable rent (× 12) | NPR 180,000.00 |
| Annual base tax (× 10%) | NPR 18,000.00 |
| Discount amount | NPR 0.00 |
| Amount after discount | NPR 18,000.00 |
| Declared rent (15,000) < adjusted rent (15,000)? | No → **no penalty** |
| **Total Revised Tax Demand Due** | **NPR 18,000.00** |

### Discount illustration

If the same NPR 72,000 base tax from the main example *had* been paired with an approved 50% non-profit educational discount instead of a rejected one:

| Step | Value |
|---|---|
| Annual base tax | NPR 72,000.00 |
| Discount rate | 50% |
| Discount amount | NPR 36,000.00 |
| Amount after discount | NPR 36,000.00 |

(All figures on this page were computed directly from the repository's own `calculate()` logic, not estimated by hand.)

---

## The Mock Government Dataset

Everything the auditor "knows" lives in `records.py` as plain Python dictionaries — there is no external database, file, or API for the underlying records. This doubles as the full reference list of valid test inputs.

### Ward & Property Registry (`WARD_REGISTRY`)

| Property ID | Stories | Type | Owner | Ward | Registered Use |
|---|---|---|---|---|---|
| `PROP_KTM_101` | 6 | Commercial | Everest Business Tower Pvt. Ltd. | WARD_1 | Commercial Bank Lease |
| `PROP_KTM_102` | 3 | Commercial | Rajesh Sharma | WARD_1 | Retail Showroom – Electronics |
| `PROP_KTM_103` | 4 | Residential | Sunita Shrestha | WARD_2 | Residential Flat – Rented Apartments |
| `PROP_KTM_104` | 2 | Commercial | Himal Softwares Pvt. Ltd. | WARD_2 | Private IT Office |
| `PROP_KTM_105` | 3 | Residential | Prakash Tamang | WARD_3 | Residential Flat |
| `PROP_KTM_106` | 2 | Commercial | Sarita Rai | WARD_3 | Restaurant & Lounge |
| `PROP_KTM_107` | 4 | Residential | Kamala Adhikari | WARD_1 | Residential Flat – Rented Apartments |
| `PROP_LTP_201` | 1 | Industrial | Bagmati Garments Manufacturing Pvt. Ltd. | WARD_4 | Manufacturing Unit – Garments |
| `PROP_LTP_202` | 2 | Industrial | Valley Cold Storage Pvt. Ltd. | WARD_4 | Warehouse – Cold Storage |
| `PROP_LTP_203` | 5 | Commercial | Dipendra Bhandari | WARD_2 | Commercial Bank Lease |

### Ward Rent Standards (`RENT_STANDARDS`) — NPR / month

| Ward | Commercial | Residential | Industrial |
|---|---|---|---|
| WARD_1 | 60,000 | 25,000 | 45,000 |
| WARD_2 | 45,000 | 20,000 | 35,000 |
| WARD_3 | 30,000 | 15,000 | 25,000 |
| WARD_4 | 25,000 | 12,000 | 50,000 |

### PAN (Taxpayer) Registry (`PAN_REGISTRY`)

| PAN | Name | Non-Profit? | Category |
|---|---|---|---|
| `PAN600123456` | Sagarmatha Commercial Bank Ltd. | No | Private Bank Enterprise |
| `PAN600123457` | Bright Future Educational Trust | **Yes** | **Educational Trust School** |
| `PAN600123458` | Kathmandu Valley Welfare Society | Yes | Registered NGO |
| `PAN600223456` | Namaste Retail Traders Pvt. Ltd. | No | Retail Enterprise |
| `PAN600223457` | Himal Softwares Pvt. Ltd. | No | Private IT Enterprise |
| `PAN300123456` | Bagmati Garments Manufacturing Pvt. Ltd. | No | Industrial Manufacturing Enterprise |
| `PAN300223456` | Newa Heritage Restaurant Pvt. Ltd. | No | Hospitality Enterprise |
| `PAN500123456` | Rising Star Academy Trust | **Yes** | **Educational Trust School** |
| `PAN500223456` | Valley Cold Storage Pvt. Ltd. | No | Warehousing Enterprise |
| `PAN700123456` | Green Nepal Environmental Society | Yes | Registered NGO |

### Tax Rates (`TAX_RATES`)

| Rate | Value |
|---|---|
| `Rent_Tax_Rate` | 10% |
| `False_Reporting_Penalty` | 20% |

### Discount Registry (`DISCOUNT_REGISTRY`)

| Discount | Rate | Eligibility |
|---|---|---|
| `NON_PROFIT_EDUCATIONAL_DISCOUNT` | 50% | PAN entity has `is_non_profit = true` **and** `category = "Educational Trust School"` |

Only one discount currently exists in the registry. Note that eligibility requires **both** conditions — being non-profit alone isn't enough: `PAN600123458` and `PAN700123456` are both non-profits, but their category is "Registered NGO," not "Educational Trust School," so under the current rule they do **not** qualify for this discount. Only `PAN600123457` and `PAN500123456` currently satisfy both conditions.

Also note: the Property Registry and the PAN Registry are validated **independently** — the tool does not check that the PAN you enter actually belongs to the owner listed for the Property ID you enter (see [Limitations and Notes](#limitations-and-notes)).

---

## Who This Is For

- **Students and developers learning agentic AI / LLM-orchestration patterns** — a compact, readable example of combining structured LLM output (JSON mode, strict schema) with deterministic downstream logic.
- **Civic-tech / GovTech enthusiasts** prototyping ideas for Nepali municipal tax-audit tooling, or similar rent/property tax systems elsewhere.
- **Portfolio reviewers, recruiters, or collaborators** evaluating a hybrid "AI reasoning + rule-based calculation" system design.
- **Educators or workshop instructors** looking for a small, self-contained example of why financial arithmetic in an AI-assisted pipeline is often better handled by ordinary code than by the model itself.
- **Hobbyists experimenting with the Groq API** who want a working, minimal example of JSON-mode structured extraction feeding into business logic.

This is **not** intended for production tax administration, is not affiliated with any real government body, and should not be relied on for actual filings — see the [Disclaimer](#disclaimer).

---

## Design Philosophy

The core design decision in this project is the split between what the **LLM** is trusted to do and what **plain Python** is trusted to do:

- The **LLM** (`qwen/qwen3.8-27b` via Groq, called with `temperature=0.0` and a strict JSON response format) is used for the things language models are actually good at: reading a free-text human explanation, comparing it against structured records, and rendering a judgment call — is this rent correct, is this discount claim legitimate, is there a violation — in natural, simple language.
- **Plain deterministic Python** (`calculate()`) is used for the thing you never want an LLM improvising: money. Once the LLM has extracted the declared rent and a discount decision as clean numeric fields, every downstream calculation — annual rent, base tax, discount amount, penalty, and total due — is ordinary arithmetic. The same inputs will always produce the same financial output, which matters a great deal in a tax context.

`temperature=0.0` and JSON mode are used to keep the model's reasoning as consistent as possible run-to-run, though (as with any hosted LLM) bit-for-bit identical output across calls isn't a guarantee — which is exactly why the money math is not left to the model.

The exact system prompt sent to the model (from `formats.py`) instructs it to act as a Municipal Tax Audit Officer and return **only** JSON in this shape:

```json
{
    "declared_rent_correctness_check": {
        "declared_rent": 0.0,
        "rent_reporting_findings": "CORRECT REPORTED / UNDER REPORTED + brief explanation"
    },
    "non_profit_discount_verification": {
        "user_claim": "Summary of requested discount or null",
        "discount_request_findings": "APPROVED / REJECTED / null + brief explanation",
        "discount_percent_approved": 0.0
    },
    "violation_detection": {
        "status": "NO VIOLATION / TAX VIOLATION DETECTED",
        "reasons": "Reasons"
    },
    "additional_info": "Any contextual info that doesn't fit elsewhere, or null"
}
```

The prompt also explicitly forbids currency symbols, strings, or commas in the numeric fields, and forbids the literal strings `"null"` / `"None"` in place of a real JSON `null` — small but important guardrails that make the model's output safe to parse directly with `json.loads()`.

---

## Limitations and Notes

Documented honestly, since this is a prototype rather than a finished product:

- **Two hardcoded path constants must be edited by hand** — `KEY_PATH` and `REPORT_PATH` in `main.py` are placeholder strings, not environment variables or CLI flags. The script will not run until you set them.
- **No `requirements.txt`** is included; dependencies must be installed manually (`groq`, `python-dotenv`).
- **The "official records" are entirely in-memory and synthetic** — ten sample properties and ten sample PAN entities, hardcoded in `records.py`. There is no real database, no persistence between runs, and no way to add new records without editing the Python source directly.
- **Property ID and PAN ID are validated independently.** The tool checks that each ID individually exists in its registry, but does **not** verify that the PAN you enter actually belongs to the property's registered owner.
- **The tax base is always the ward's official standard rent for that property type — never the taxpayer's declared rent —** even in cases where the declared rent is honestly reported *above* the standard. Only the *penalty* decision depends on the declared figure.
- **Only one discount type currently exists** (`NON_PROFIT_EDUCATIONAL_DISCOUNT`, 50%). The system prompt is written generally enough to reason about discount eligibility, but the sample dataset only defines this one rule.
- **Minimal defensive error handling around the LLM's JSON response** — `extract_required_json_data()` uses `.get()` for the top-level keys (which softens missing-section errors), but a genuinely malformed or unexpected response from the model could still cause a downstream error, since the response isn't validated against a formal schema before use.
- **The property `type` field must exactly match a key in `RENT_STANDARDS`** (`"Commercial"`, `"Residential"`, or `"Industrial"`) — there's no fuzzy matching or validation layer, so a typo'd or unrecognized type would cause a runtime error rather than a friendly message.
- **Output is plain `.txt` only** — no PDF, HTML, or structured data (JSON/CSV) export of the final report.
- **Single-session CLI only** — there is no report history, no database of past filings, and no way to look up a previously generated report other than the file itself.
- **Requires a live Groq API call every run** — there is no offline or cached mode.

---

## Possible Future Enhancements

Some natural directions this project could grow in (none of these are currently implemented):

- Move `KEY_PATH`/`REPORT_PATH` (and the model name) into environment variables or a small config file instead of hardcoded constants.
- Add a `requirements.txt` / `pyproject.toml` for one-command dependency installation.
- Cross-validate that the entered PAN actually corresponds to the registered owner of the entered Property ID.
- Expand `DISCOUNT_REGISTRY` with additional rules — for example a senior-citizen residential rebate or an early-payment incentive — alongside the existing non-profit educational discount.
- Add automated tests around `calculate()` given its central role in producing legally/financially meaningful numbers.
- Validate the LLM's JSON response against a formal schema before use, with a clear error message on mismatch.
- Export reports as PDF/HTML in addition to plain text.
- A lightweight web UI or API wrapper around the existing CLI logic.
- Persistent storage (even just a local SQLite file) for filing history.

---

## Disclaimer

This project uses **entirely fictional, synthetic data** for demonstration and educational purposes. It is **not affiliated with, endorsed by, or connected to** the Kathmandu Metropolitan City, the Lalitpur Metropolitan City, Nepal's Inland Revenue Department, or any other real government body. Property records, PAN numbers, owner names, rent standards, and tax rates are all invented sample data. Nothing produced by this tool constitutes an official tax assessment, legal advice, or financial advice, and it should not be used to make real tax filings or decisions.

---

## License

This repository is **proprietary and confidential**. Per the included `LICENCE` file:

> Copyright © 2026 Safal Adhikari. All Rights Reserved.
> This code is proprietary and confidential. Unauthorized distribution via any medium is strictly prohibited.

This is **not** an open-source license (e.g. MIT, Apache, GPL) — no rights to copy, modify, or redistribute this code are granted. See the [`LICENCE`](./LICENCE) file for the full, authoritative text. As the project is closed/proprietary, it is not currently set up to accept external pull requests or contributions; reach out to the author directly if you'd like to discuss the project.

---

## Author

**Safal Adhikari**
