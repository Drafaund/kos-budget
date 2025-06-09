# utils/state_manager.py

import streamlit as st
from config.settings import SESSION_KEYS, PAGES

def initialize_session_state():
    """Initialize all session state variables"""
    # Authentication
    if SESSION_KEYS["AUTHENTICATED"] not in st.session_state:
        st.session_state[SESSION_KEYS["AUTHENTICATED"]] = False
    if SESSION_KEYS["USERNAME"] not in st.session_state:
        st.session_state[SESSION_KEYS["USERNAME"]] = ""
    if SESSION_KEYS["USERS"] not in st.session_state:
        st.session_state[SESSION_KEYS["USERS"]] = {}
    
    # Navigation
    if SESSION_KEYS["CURRENT_PAGE"] not in st.session_state:
        st.session_state[SESSION_KEYS["CURRENT_PAGE"]] = PAGES["FORM_INPUT"]
    
    # Financial data
    if SESSION_KEYS["MONTHLY_BUDGET"] not in st.session_state:
        st.session_state[SESSION_KEYS["MONTHLY_BUDGET"]] = 0
    if SESSION_KEYS["CATEGORIES"] not in st.session_state:
        st.session_state[SESSION_KEYS["CATEGORIES"]] = []
    if SESSION_KEYS["EXPENSES"] not in st.session_state:
        st.session_state[SESSION_KEYS["EXPENSES"]] = []

def authenticate_user(username, password):
    """Authenticate user login"""
    users = st.session_state.get(SESSION_KEYS["USERS"], {})
    
    if username in users and users[username] == password:
        st.session_state[SESSION_KEYS["AUTHENTICATED"]] = True
        st.session_state[SESSION_KEYS["USERNAME"]] = username
        return True, "Selamat datang kembali!"
    else:
        return False, "Username atau password salah."

def register_user(username, password):
    """Register new user"""
    users = st.session_state.get(SESSION_KEYS["USERS"], {})
    
    if username in users:
        return False, "Username sudah terdaftar."
    else:
        st.session_state[SESSION_KEYS["USERS"]][username] = password
        return True, "Pendaftaran berhasil! Silakan masuk."

def logout_user():
    """Logout current user"""
    st.session_state[SESSION_KEYS["AUTHENTICATED"]] = False
    st.session_state[SESSION_KEYS["USERNAME"]] = ""

def add_category(name, priority, urgency, frequency, impact):
    """Add or update category"""
    categories = st.session_state.get(SESSION_KEYS["CATEGORIES"], [])
    
    # Check if category exists
    category_exists = False
    for cat in categories:
        if cat['name'] == name:
            cat['priority'] = priority
            cat['urgency'] = urgency
            cat['frequency'] = frequency
            cat['impact'] = impact
            category_exists = True
            break
    
    if not category_exists:
        categories.append({
            'name': name,
            'priority': priority,
            'urgency': urgency,
            'frequency': frequency,
            'impact': impact,
            'allocation': 0,
            'spent': 0,
            'combined_score': 0
        })
    
    st.session_state[SESSION_KEYS["CATEGORIES"]] = categories
    return "diperbarui" if category_exists else "ditambahkan"

def delete_category(category_name):
    """Delete category and related expenses"""
    categories = st.session_state.get(SESSION_KEYS["CATEGORIES"], [])
    expenses = st.session_state.get(SESSION_KEYS["EXPENSES"], [])
    
    # Remove category
    st.session_state[SESSION_KEYS["CATEGORIES"]] = [
        cat for cat in categories if cat['name'] != category_name
    ]
    
    # Remove related expenses
    st.session_state[SESSION_KEYS["EXPENSES"]] = [
        exp for exp in expenses if exp['category'] != category_name
    ]

def add_expense(category, amount):
    """Add expense to category"""
    expenses = st.session_state.get(SESSION_KEYS["EXPENSES"], [])
    expenses.append({
        'category': category,
        'amount': amount
    })
    st.session_state[SESSION_KEYS["EXPENSES"]] = expenses