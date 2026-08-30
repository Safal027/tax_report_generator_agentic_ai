
import os
import sys
import json
from dotenv import load_dotenv
from groq import Groq
from formats import *
from records import *

KEY_PATH = r"C:\Users\safal\OneDrive\Documents\Programing\Python\Agentic AI (Yantra)\.gitignore\.env"
REPORT_PATH = r"C:\Users\safal\OneDrive\Documents\Programing\Python\Agentic AI (Yantra)\output report\report.txt"


def load_key():
    load_dotenv(
        dotenv_path=KEY_PATH)

    Key = os.getenv("GROQ_API_KEY")

    if not Key:
        print("\nAPI key not found. Please check your .env file!")
        sys.exit()

    print("\nSuccessfully loaded the API key.")

    return Key


def get_user_prompt():
    while True:
        prop_id = input(
            "\nEnter your Property ID (for eg: PROP_KTM_101): ").upper().strip()

        if prop_id in WARD_REGISTRY:
            print("Property data found.")
            break
        else:
            print("\nPlease enter correct Property ID.")

    while True:
        pan_id = input(
            "\nEnter your PAN ID (for eg: PAN600123456): ").upper().strip()

        if pan_id in PAN_REGISTRY:
            print("PAN ID found.")
            break
        else:
            print("\nPlease enter correct PAN ID.")

    filing_detail = input(
        "\nEnter your filing details in simple language: \n").strip()

    user_input = f"Property: {prop_id}\nPAN: {pan_id}\n\n{filing_detail}"

    user_prompt = f"""
    # USER DECLARATION:
    {user_input}
    """
    return prop_id, pan_id, user_prompt, filing_detail


def get_required_data(prop_id, pan_id):
    prop_details = WARD_REGISTRY.get(prop_id)
    prop_ward_rent_standard = RENT_STANDARDS.get(prop_details.get("ward"))
    pan_details = PAN_REGISTRY.get(pan_id)

    string_data = ""
    data_list = [prop_details, prop_ward_rent_standard,
                 pan_details, TAX_RATES, DISCOUNT_REGISTRY]
    i = 0

    for name in dict_names:
        string_data += f"""
            <{name}>
            {json.dumps(data_list[i], indent=2)}"""
        i += 1

    individual_data = [prop_details, prop_ward_rent_standard, pan_details]

    return string_data, individual_data


def get_json_output():
    response = client.chat.completions.create(
        messages=[{"role": "system",
                   "content": sys_prompt},
                  {"role": "user",
                   "content": prompt_data_dict[2]}],
        max_tokens=4096,
        temperature=0.0,
        response_format={"type": "json_object"},
        reasoning_format="hidden",
        model="qwen/qwen3.8-27b")

    output = response.choices[0].message.content

    return output


def extract_required_json_data(json_data):
    rent_check = json_data.get("declared_rent_correctness_check", {})
    discount_check = json_data.get("non_profit_discount_verification", {})
    violation_check = json_data.get("violation_detection", {})

    dec_rent = rent_check.get("declared_rent") or 0.0
    rent_reporting_findings = rent_check.get(
        "rent_reporting_findings", "No findings provided.")

    user_claim = discount_check.get("user_claim")
    discount_request_findings = discount_check.get("discount_request_findings")
    discount_percent_approved = discount_check.get(
        "discount_percent_approved") or 0.0

    status = violation_check.get("status", "UNKNOWN")
    reasons = violation_check.get("reasons", "No reasons specified.")

    additional_info = json_data.get("additional_info")

    results = [dec_rent, rent_reporting_findings, user_claim,
               discount_request_findings, discount_percent_approved, status, reasons, additional_info]

    return results


def calculate(official_data, extracted_data):
    adj_rent = round(official_data[1].get(official_data[0].get("type")), 2)
    yearly_adj_rent = round(adj_rent * 12, 2)
    yearly_base_tax = round(yearly_adj_rent * 0.10, 2)

    discount_amount = 0.00
    penalty_amount = 0.00

    if extracted_data[4] > 0.00:
        discount_amount = round(yearly_base_tax * extracted_data[4], 2)
        amount_after_discount = round(yearly_base_tax - discount_amount, 2)
    else:
        amount_after_discount = yearly_base_tax

    if extracted_data[0] < adj_rent:
        penalty_amount = round(amount_after_discount * 0.20, 2)
        amount_after_penalty = amount_after_discount + penalty_amount
    else:
        amount_after_penalty = amount_after_discount

    final_amount = amount_after_penalty

    results = [adj_rent, yearly_adj_rent, yearly_base_tax, discount_amount,
               amount_after_discount, penalty_amount, amount_after_penalty, final_amount]

    return results


GROQ_API_KEY = load_key()
client = Groq(api_key=GROQ_API_KEY)

prompt_data_dict = get_user_prompt()
required_data = get_required_data(prompt_data_dict[0], prompt_data_dict[1])

records = required_data[0]
official_data = required_data[1]

sys_prompt = get_sys_prompt(records)
json_output = json.loads(get_json_output())
extracted_data = extract_required_json_data(json_output)

calculated_data = calculate(official_data, extracted_data)

user_filing = prompt_data_dict[3]
prop_id = prompt_data_dict[0]
ward_id = official_data[0].get("ward")
pan_id = prompt_data_dict[1]
dec_rent = extracted_data[0]
Type = official_data[0].get("type")
rent_floor = official_data[1].get(Type)
findings_1 = extracted_data[1]
user_claim = extracted_data[2]
pan_record = official_data[2]
findings_2 = extracted_data[3]
status = extracted_data[5]
reasons = extracted_data[6]

base_rent = calculated_data[0]
yearly_rent = calculated_data[1]
yearly_base_tax = calculated_data[2]
discount_amount = calculated_data[3]
amount_after_discount = calculated_data[4]
penalty_amount = calculated_data[5]
amount_after_penalty = calculated_data[6]
total_amount = calculated_data[7]
extra = extracted_data[7]

para = Parameters(
    user_filing=user_filing,
    prop_id=prop_id,
    ward_id=ward_id,
    pan_id=pan_id,
    dec_rent=f"{dec_rent:,.2f}",
    Type=Type,
    rent_floor=f"{rent_floor:,.2f}",
    findings_1=findings_1,
    user_claim=user_claim or "None",
    pan_record=pan_record,
    findings_2=findings_2 or "None",
    status=status,
    reasons=reasons,
    base_rent=f"{base_rent:,.2f}",
    yearly_rent=f"{yearly_rent:,.2f}",
    yearly_base_tax=f"{yearly_base_tax:,.2f}",
    discount_amount=f"{discount_amount:,.2f}",
    amount_after_discount=f"{amount_after_discount:,.2f}",
    penalty_amount=f"{penalty_amount:,.2f}",
    amount_after_penalty=f"{amount_after_penalty:,.2f}",
    total_amount=f"{total_amount:,.2f}",
    extra=extra or "None"
)

final_report = report_format(para)

os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as report:
    report.write(final_report)

print("\n\nYour Tax Report has been generated.\n")
