
WARD_REGISTRY = {
    "PROP_KTM_101": {
        "stories": 6,
        "type": "Commercial",
        "owner": "Everest Business Tower Pvt. Ltd.",
        "ward": "WARD_1",
        "registered_use": "Commercial Bank Lease"
    },
    "PROP_KTM_102": {
        "stories": 3,
        "type": "Commercial",
        "owner": "Rajesh Sharma",
        "ward": "WARD_1",
        "registered_use": "Retail Showroom - Electronics"
    },
    "PROP_KTM_103": {
        "stories": 4,
        "type": "Residential",
        "owner": "Sunita Shrestha",
        "ward": "WARD_2",
        "registered_use": "Residential Flat - Rented Apartments"
    },
    "PROP_KTM_104": {
        "stories": 2,
        "type": "Commercial",
        "owner": "Himal Softwares Pvt. Ltd.",
        "ward": "WARD_2",
        "registered_use": "Private IT Office"
    },
    "PROP_KTM_105": {
        "stories": 3,
        "type": "Residential",
        "owner": "Prakash Tamang",
        "ward": "WARD_3",
        "registered_use": "Residential Flat"
    },
    "PROP_KTM_106": {
        "stories": 2,
        "type": "Commercial",
        "owner": "Sarita Rai",
        "ward": "WARD_3",
        "registered_use": "Restaurant & Lounge"
    },
    "PROP_KTM_107": {
        "stories": 4,
        "type": "Residential",
        "owner": "Kamala Adhikari",
        "ward": "WARD_1",
        "registered_use": "Residential Flat - Rented Apartments"
    },
    "PROP_LTP_201": {
        "stories": 1,
        "type": "Industrial",
        "owner": "Bagmati Garments Manufacturing Pvt. Ltd.",
        "ward": "WARD_4",
        "registered_use": "Manufacturing Unit - Garments"
    },
    "PROP_LTP_202": {
        "stories": 2,
        "type": "Industrial",
        "owner": "Valley Cold Storage Pvt. Ltd.",
        "ward": "WARD_4",
        "registered_use": "Warehouse - Cold Storage"
    },
    "PROP_LTP_203": {
        "stories": 5,
        "type": "Commercial",
        "owner": "Dipendra Bhandari",
        "ward": "WARD_2",
        "registered_use": "Commercial Bank Lease"
    }
}

RENT_STANDARDS = {
    "WARD_1": {
        "Commercial": 60000,
        "Residential": 25000,
        "Industrial": 45000
    },
    "WARD_2": {
        "Commercial": 45000,
        "Residential": 20000,
        "Industrial": 35000
    },
    "WARD_3": {
        "Commercial": 30000,
        "Residential": 15000,
        "Industrial": 25000
    },
    "WARD_4": {
        "Commercial": 25000,
        "Residential": 12000,
        "Industrial": 50000
    }
}

PAN_REGISTRY = {
    "PAN600123456": {
        "name": "Sagarmatha Commercial Bank Ltd.",
        "is_non_profit": False,
        "category": "Private Bank Enterprise"
    },
    "PAN600123457": {
        "name": "Bright Future Educational Trust",
        "is_non_profit": True,
        "category": "Educational Trust School"
    },
    "PAN600123458": {
        "name": "Kathmandu Valley Welfare Society",
        "is_non_profit": True,
        "category": "Registered NGO"
    },
    "PAN600223456": {
        "name": "Namaste Retail Traders Pvt. Ltd.",
        "is_non_profit": False,
        "category": "Retail Enterprise"
    },
    "PAN600223457": {
        "name": "Himal Softwares Pvt. Ltd.",
        "is_non_profit": False,
        "category": "Private IT Enterprise"
    },
    "PAN300123456": {
        "name": "Bagmati Garments Manufacturing Pvt. Ltd.",
        "is_non_profit": False,
        "category": "Industrial Manufacturing Enterprise"
    },
    "PAN300223456": {
        "name": "Newa Heritage Restaurant Pvt. Ltd.",
        "is_non_profit": False,
        "category": "Hospitality Enterprise"
    },
    "PAN500123456": {
        "name": "Rising Star Academy Trust",
        "is_non_profit": True,
        "category": "Educational Trust School"
    },
    "PAN500223456": {
        "name": "Valley Cold Storage Pvt. Ltd.",
        "is_non_profit": False,
        "category": "Warehousing Enterprise"
    },
    "PAN700123456": {
        "name": "Green Nepal Environmental Society",
        "is_non_profit": True,
        "category": "Registered NGO"
    }
}

TAX_RATES = {
    "Rent_Tax_Rate": 0.10,
    "False_Reporting_Penalty": 0.20
}

DISCOUNT_REGISTRY = {
    "NON_PROFIT_EDUCATIONAL_DISCOUNT": {
        "description": "Rebate on assessed rental tax for properties registered under a certified non-profit educational trust or school.",
        "rate": 0.50,
        "eligibility": "PAN entity has is_non_profit = true and category = 'Educational Trust School'"
    }
}


def get_dict_names():
    dict_name = []

    for name, value in globals().items():
        if name.isupper() and isinstance(value, dict):
            dict_name.append(name)

    return dict_name


dict_names = get_dict_names()
