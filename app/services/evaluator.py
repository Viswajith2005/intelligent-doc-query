# app/services/evaluator.py

def evaluate_response(query: str, answer: str) -> str:
    if any(word in answer.lower() for word in ["yes", "covered", "approved"]):
        return "Likely Yes"
    elif any(word in answer.lower() for word in ["no", "denied", "not covered"]):
        return "Likely No"
    else:
        return "Uncertain"

def evaluate_accuracy(query: str, answer: str) -> dict:
    """
    Evaluate the accuracy of an answer based on various criteria.
    """
    accuracy_score = 0
    criteria = {
        "policy_references": 0,
        "specific_numbers": 0,
        "comprehensive_coverage": 0,
        "clear_structure": 0,
        "relevant_content": 0
    }
    
    # Check for policy references
    if any(ref in answer.lower() for ref in ["section", "policy", "clause", "act"]):
        criteria["policy_references"] = 1
        accuracy_score += 20
    
    # Check for specific numbers/dates
    if any(char.isdigit() for char in answer):
        criteria["specific_numbers"] = 1
        accuracy_score += 20
    
    # Check for comprehensive coverage
    if len(answer.split()) > 50:  # Detailed answer
        criteria["comprehensive_coverage"] = 1
        accuracy_score += 20
    
    # Check for clear structure
    if any(struct in answer for struct in ["**", "---", "•", "-"]):
        criteria["clear_structure"] = 1
        accuracy_score += 20
    
    # Check for relevant content
    relevant_keywords = ["coverage", "policy", "insurance", "claim", "benefit", "limit"]
    if any(keyword in answer.lower() for keyword in relevant_keywords):
        criteria["relevant_content"] = 1
        accuracy_score += 20
    
    return {
        "accuracy_score": accuracy_score,
        "criteria_met": criteria,
        "overall_rating": "High" if accuracy_score >= 80 else "Medium" if accuracy_score >= 60 else "Low"
    }
