import streamlit as st
from utils.calculations import calculate_decision_score, calculate_allocation
from utils.state_manager import initialize_session_state
import pandas as pd

def render_form_input():
    """Render the form input page"""
    initialize_session_state()
    
    st.markdown('<h1 class="title-gradient">📝 Input Keuangan & Decision Category</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.1rem; color: black; margin-bottom: 2rem;">Atur keuangan bulananmu dan tetapkan kategori pengeluaran dengan prioritas dan kriteria keputusan yang tepat</p>', unsafe_allow_html=True)

    # Budget input section
    render_budget_input()
    
    # Decision Category Information
    render_decision_info()
    
    # Category management section
    render_category_form()
    
    # Categories display with decision scores
    render_categories_display()

def render_budget_input():
    """Render budget input section"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">💰 Uang Bulanan</h3>', unsafe_allow_html=True)
    st.session_state.monthly_budget = st.number_input(
        "💵 Masukkan uang bulanan Anda (Rp)", 
        min_value=0, 
        step=10000, 
        value=st.session_state.monthly_budget,
        help="Masukkan total uang bulanan yang Anda terima"
    )
    st.markdown('</div>', unsafe_allow_html=True)

def render_decision_info():
    """Render decision category information"""
    st.markdown('<div class="decision-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: black; font-weight: 600;">🎯 Panduan Decision Category</h3>', unsafe_allow_html=True)
    st.markdown('''
    <div style="color: black;">
    <p><strong>🚨 Urgensi (50%):</strong> Seberapa mendesak kategori ini (1=Tidak mendesak, 5=Sangat mendesak)</p>
    <p><strong>🔄 Frekuensi (30%):</strong> Seberapa sering dibutuhkan (1=Jarang, 5=Sangat sering)</p>
    <p><strong>💥 Dampak (20%):</strong> Dampak jika terlewati (1=Ringan, 5=Sangat berat)</p>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_category_form():
    """Render category form for adding/editing categories"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">📂 Tambah / Edit Kategori Pengeluaran</h3>', unsafe_allow_html=True)
    
    with st.form(key="category_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cat_name = st.text_input("🏷️ Nama Kategori", placeholder="Contoh: Makanan, Transport, dll")
            cat_priority = st.slider("⭐ Prioritas Personal", 1, 5, 3, help="1=Rendah, 5=Tinggi")
        
        with col2:
            st.markdown("**🎯 Decision Category:**")
            cat_urgency = st.slider("🚨 Urgensi", 1, 5, 3, help="Seberapa mendesak kategori ini")
            cat_frequency = st.slider("🔄 Frekuensi", 1, 5, 3, help="Seberapa sering dibutuhkan")
            cat_impact = st.slider("💥 Dampak jika Terlewati", 1, 5, 3, help="Dampak jika kategori ini diabaikan")
        
        submitted = st.form_submit_button("💾 Simpan Kategori")

    if submitted and cat_name:
        handle_category_submission(cat_name, cat_priority, cat_urgency, cat_frequency, cat_impact)
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_category_submission(cat_name, cat_priority, cat_urgency, cat_frequency, cat_impact):
    """Handle category form submission"""
    # Check if category exists
    category_exists = False
    for cat in st.session_state.categories:
        if cat['name'] == cat_name:
            cat['priority'] = cat_priority
            cat['urgency'] = cat_urgency
            cat['frequency'] = cat_frequency
            cat['impact'] = cat_impact
            category_exists = True
            break
    
    if not category_exists:
        st.session_state.categories.append({
            'name': cat_name,
            'priority': cat_priority,
            'urgency': cat_urgency,
            'frequency': cat_frequency,
            'impact': cat_impact,
            'allocation': 0,
            'spent': 0,
            'combined_score': 0
        })
    
    calculate_allocation()
    action = "diperbarui" if category_exists else "ditambahkan"
    st.markdown(f'<div class="success-message">✅ Kategori "{cat_name}" berhasil {action}.</div>', unsafe_allow_html=True)

def render_categories_display():
    """Render categories display with decision scores"""
    if not st.session_state.categories:
        return
        
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">📋 Daftar Kategori & Analisis Decision</h3>', unsafe_allow_html=True)
    
    # Create detailed dataframe
    df_categories = []
    for cat in st.session_state.categories:
        decision_score = calculate_decision_score(
            cat.get('urgency', 3) / 5.0,
            cat.get('frequency', 3) / 5.0,
            cat.get('impact', 3) / 5.0
        ) * 100  # Convert to percentage for display
        
        df_categories.append({
            '📂 Kategori': cat['name'],
            '⭐ Prioritas': cat['priority'],
            '🚨 Urgensi': cat.get('urgency', 3),
            '🔄 Frekuensi': cat.get('frequency', 3),
            '💥 Dampak': cat.get('impact', 3),
            '🎯 Decision Score (%)': f"{decision_score:.1f}%",
            '💰 Alokasi (Rp)': f"Rp {cat['allocation']:,.0f}"
        })
    
    df_display = pd.DataFrame(df_categories)
    st.dataframe(df_display, use_container_width=True)
    
    # Show allocation explanation
    render_allocation_explanation()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Delete category section
    render_delete_category_section()

def render_allocation_explanation():
    """Render allocation calculation explanation"""
    st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown('**📊 Cara Perhitungan Alokasi:**', unsafe_allow_html=True)
    st.markdown('''
    - **Combined Score** = (Prioritas Personal × 50%) + (Decision Score × 50%)
    - **Decision Score** = (Urgensi × 50%) + (Frekuensi × 30%) + (Dampak × 20%)
    - **Alokasi** = (Combined Score / Total Combined Score) × Budget Bulanan
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_delete_category_section():
    """Render delete category section"""
    if not st.session_state.categories:
        return
        
    with st.expander("🗑️ Hapus Kategori"):
        cat_to_delete = st.selectbox(
            "Pilih kategori yang ingin dihapus", 
            [cat['name'] for cat in st.session_state.categories]
        )
        if st.button("🗑️ Hapus Kategori", key="delete_cat"):
            st.session_state.categories = [
                cat for cat in st.session_state.categories 
                if cat['name'] != cat_to_delete
            ]
            st.session_state.expenses = [
                e for e in st.session_state.expenses 
                if e['category'] != cat_to_delete
            ]
            calculate_allocation()
            st.markdown(
                f'<div class="success-message">✅ Kategori "{cat_to_delete}" berhasil dihapus.</div>', 
                unsafe_allow_html=True
            )