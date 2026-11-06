def rule_based(score, docs, income, fraud):
    if docs == False:
        return "Hold", "Documents are incomplete"
    elif score < 70:
        return "Hold", "Score is less than 70"
    elif income == False:
        return "Hold", "Income is not verified"
    elif fraud == True:
        return "Hold", "Fraud detected"
    else:
        return "Review", "All conditions are satisfied"
cases = [
    ("pass", 82, True, True, False, "Review"),
    ("fail_income", 82, True, False, False, "Hold"),
    ("fail_fraud", 82, True, True, True, "Hold"),
    ("boundary", 70, True, True, False, "Review")
]
print("Name | Score | Docs | Income | Fraud | Expected | Actual | Reason")
print("-" * 85)
for case in cases:
    name = case[0]
    score = case[1]
    docs = case[2]
    income = case[3]
    fraud = case[4]
    expected = case[5]
    actual, reason = rule_based(score, docs, income, fraud)
    print(name, "|", score, "|", docs, "|", income, "|", fraud, "|", expected, "|", actual, "|", reason)