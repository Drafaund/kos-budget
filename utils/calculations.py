# utils/calculations.py

import streamlit as st
from config.settings import DECISION_WEIGHTS, SCORE_WEIGHTS, SESSION_KEYS

def calculate_decision_score(urgency, frequency, impact):
    """Calculate decision score based on weighted criteria"""
    decision_score = (urgency * DECISION_WEIGHTS["urgency"] + 
                     frequency * DECISION_WEIGHTS["frequency"] + 
                     impact * DECISION_WEIGHTS["impact"])
    return decision_score

def calculate_allocation():
    """Calculate allocation based on priority and decision scores"""
    if not st.session_state.get(SESSION_KEYS["CATEGORIES"]):
        return
        
    categories = st.session_state[SESSION_KEYS["CATEGORIES"]]
    expenses = st.session_state.get(SESSION_KEYS["EXPENSES"], [])
    monthly_budget = st.session_state.get(SESSION_KEYS["MONTHLY_BUDGET"], 0)
    
    # Calculate combined scores
    for cat in categories:
        # Priority score (1-5) normalized to 0-1
        priority_normalized = cat['priority'] / 5.0
        
        # Decision score (already 0-1 range from calculate_decision_score)
        decision_score = calculate_decision_score(
            cat.get('urgency', 3) / 5.0,  # Normalize to 0-1
            cat.get('frequency', 3) / 5.0,
            cat.get('impact', 3) / 5.0
        )
        
        # Combined score with equal weight between priority and decision
        cat['combined_score'] = (priority_normalized * SCORE_WEIGHTS["priority"] + 
                               decision_score * SCORE_WEIGHTS["decision"])
    
    # Calculate allocations based on combined scores
    total_combined_score = sum([cat['combined_score'] for cat in categories])
    
    for cat in categories:
        if total_combined_score > 0:
            weight = cat['combined_score'] / total_combined_score
            cat['allocation'] = round(weight * monthly_budget, 2)
        else:
            cat['allocation'] = 0
        
        # Calculate spent amount
        cat['spent'] = 0
        for exp in expenses:
            if exp['category'] == cat['name']:
                cat['spent'] += exp['amount']

def get_financial_summary():
    """Get summary of financial data"""
    categories = st.session_state.get(SESSION_KEYS["CATEGORIES"], [])
    monthly_budget = st.session_state.get(SESSION_KEYS["MONTHLY_BUDGET"], 0)
    
    if not categories:
        return {
            'total_allocated': 0,
            'total_spent': 0,
            'remaining_budget': monthly_budget
        }
    
    total_allocated = sum([cat['allocation'] for cat in categories])
    total_spent = sum([cat['spent'] for cat in categories])
    remaining_budget = monthly_budget - total_spent
    
    return {
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget
    }