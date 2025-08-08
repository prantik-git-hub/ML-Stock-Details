def analyze_financial_data(json_data):
    pros, cons = [], []

    roe = json_data.get('ROE', 0)
    dividend = json_data.get('DividendPayout', 0)
    sales_growth = json_data.get('SalesGrowth', 0)

    if roe > 10:
        pros.append(f"Good ROE: {roe}%")
    else:
        cons.append(f"Low ROE: {roe}%")

    if dividend > 10:
        pros.append(f"Healthy dividend: {dividend}%")
    else:
        cons.append("No significant dividend payout")

    if sales_growth > 10:
        pros.append(f"Strong sales growth: {sales_growth}%")
    else:
        cons.append(f"Weak sales growth: {sales_growth}%")

    return pros, cons