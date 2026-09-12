
from dataclasses import dataclass


def get_sys_prompt(records):
    prompt = f"""
    You are a Municipal Tax Audit Officer. Compare the User's Tax Declaration against the Official Government Records.
    DO NOT output long reasoning chains or internal analysis. Jump straight to the final structured response.

    # INSTRUCTIONS:
    1. First check if the records entered by the user exists in the database and Property ID, PAN Number and Ward matches or not. If not, state that details were not found or if the user forgot to enter required data such as rent amount, instruct them in one sentence to enter correct details. Exclude tax violations from this step as such are considered input mistakes.
    2. Check rent claims of the user and take required actions in "rent_reporting_findings".
    3. Analyze the discount claims and requests of the user if it eligible with the official government records or not. And take required actions in "non_profit_discount_verification".
    4. Analyze, check and verify overall user claims, requests and data with official government data. Then take required actions in "violation_detection".
    5. Use very simple English language.
    6. Return the output in ONLY JSON.

    # CRITICAL DATA TYPE & FORMATTING RULES:
    1. `declared_rent`: Must be a raw numeric FLOAT (e.g., 25000.0 or 0.0). Do NOT use strings, currency symbols ("NPR"), or commas.
    2. `discount_percent_approved`: Must be a raw numeric FLOAT (either 0.50 or 0.00). Do NOT use percentage symbols or strings.
    3. Optional Fields (`user_claim`, `discount_request_findings`, `additional_info`): Must be a STRING, or a native JSON `null` if no value exists (do NOT write the literal string "null" or "None").
    4. `reasons`: Must be a STRING summarizing all violation details.

    # OFFICIAL GOVERNMENT RECORDS:
    {records}

    # OUTPUT FORMAT REQUIREMENTS:
    Return ONLY a JSON exactly as follows and nothing else:

    {{
        "declared_rent_correctness_check": {{
            "declared_rent": [Rent amount declared by the user in per month],
            "rent_reporting_findings": "[CORRECT REPORTED / UNDER REPORTED + brief explanation]"
        }},
        "non_profit_discount_verification": {{
            "user_claim": "[Summary of requested discount or null]",
            "discount_request_findings": "[APPROVED / REJECTED / null + brief explanation]",
            "discount_percent_approved":[Percentage of discount approved, eg: 0.50, 0.00 etc]
        }},
        "violation_detection": {{
            "status": "[NO VIOLATION / TAX VIOLATION DETECTED]",
            "reasons": "[Reasons]"
        }},
        "additional_info": "[Capture any contextual information, property usage notes, or special requests that do not fit into rent or discount claims. If none, set the value to null.]"
}}
"""
    return prompt


@dataclass
class Parameters:
    user_filing: str
    prop_id: str
    ward_id: str
    pan_id: str
    dec_rent: float
    Type: str
    rent_floor: float
    findings_1: str
    user_claim: str
    pan_record: str
    findings_2: str
    status: str
    reasons: str
    base_rent: float
    yearly_rent: float
    yearly_base_tax: float
    discount_amount: float
    amount_after_discount: float
    penalty_amount: float
    amount_after_penalty: float
    total_amount: float
    extra: str


def report_format(para: Parameters):
    format = f"""
    FILING DETAILS: 
    {para.user_filing}


    MUNICIPAL TAX REPORT

    Target Property: {para.prop_id}
    Ward: {para.ward_id}
    Taxpayer PAN: {para.pan_id}

    1. Declared Rent Correctness Check
    - Declared Rent: NPR {para.dec_rent} / month
    - Official Property Classification: {para.Type}
    - Legal Minimum Rent Floor: NPR {para.rent_floor} / month
    - Findings: {para.findings_1}

    2. Non-Profit Discount Verification
    - User Claim: {para.user_claim}
    - Official PAN Registry Record: {para.pan_record}
    - Finding: {para.findings_2}

    3. Violation Determination & Reasons
    Status: {para.status}
    Reasons:
    - {para.reasons}

    4. Final Verdict & Corrected Demand Note
    - Adjusted Monthly Base Rent: NPR {para.base_rent}
    - Annual Base Taxable Income: NPR {para.yearly_rent}
    - Annual Base Tax Due (10% House Rent Tax Rate): NPR {para.yearly_base_tax}
    - Tax Discount Amount: NPR {para.discount_amount}
    - Tax Amount After Discount: NPR {para.amount_after_discount}
    - Under-Reporting Penalty Fine (20%): NPR {para.penalty_amount}
    - Tax Amount After Penalty: NPR {para.amount_after_penalty}

    TOTAL REVISED TAX DEMAND DUE: NPR {para.total_amount}

    Additional Information/Request: {para.extra}
        """
    return format
