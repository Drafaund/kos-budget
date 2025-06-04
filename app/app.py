import streamlit as st
import pandas as pd
import altair as alt

# Set page config
st.set_page_config(
    page_title="KosBudget - Manajemen Keuangan Anak Kos", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern colorful UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .css-18ni7ap.e8zbici2 {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .sidebar .stButton>button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    .auth-button {
        background: linear-gradient(45deg, #11998e, #38ef7d) !important;
    }
    
    .delete-button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
    }
    
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stNumberInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
    }
    
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .decision-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .success-message {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .warning-message {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .error-message {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .title-gradient {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .subtitle-gradient {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .avatar {
        float: right;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin-top: -70px;
        margin-right: 20px;
        border: 3px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stProgress .stProgress-bar {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
    }
    
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'users' not in st.session_state:
    st.session_state.users = {}

# Authentication pages
if not st.session_state.authenticated:
    st.markdown('<h1 class="title-gradient">🏠 KosBudget</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: white; text-align: center; margin-bottom: 2rem;">Manajemen Keuangan Cerdas untuk Anak Kos</p>', unsafe_allow_html=True)
    
    auth_tab = st.sidebar.radio("🔐 Pilih Aksi", ["Sign In", "Sign Up"])

    if auth_tab == "Sign In":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="category-card">', unsafe_allow_html=True)
            st.markdown('<h2 class="subtitle-gradient">🔐 Masuk Akun</h2>', unsafe_allow_html=True)
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            if st.button("🚀 Masuk", key="signin_btn"):
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.markdown('<div class="success-message">✅ Selamat datang kembali, {}!</div>'.format(username), unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<div class="error-message">❌ Username atau password salah.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif auth_tab == "Sign Up":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="category-card">', unsafe_allow_html=True)
            st.markdown('<h2 class="subtitle-gradient">📝 Daftar Akun</h2>', unsafe_allow_html=True)
            new_user = st.text_input("👤 Buat Username")
            new_pass = st.text_input("🔒 Buat Password", type="password")
            if st.button("🎉 Daftar", key="signup_btn"):
                if new_user in st.session_state.users:
                    st.markdown('<div class="warning-message">⚠️ Username sudah terdaftar.</div>', unsafe_allow_html=True)
                else:
                    st.session_state.users[new_user] = new_pass
                    st.markdown('<div class="success-message">🎊 Pendaftaran berhasil! Silakan masuk.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Sidebar navigation
    st.sidebar.markdown('<h2 style="color: #667eea; font-weight: 600;">🧭 Navigasi</h2>', unsafe_allow_html=True)
    
    if st.sidebar.button("📝 Form Input"):
        st.session_state.current_page = 'Form Input'
    if st.sidebar.button("📊 Dashboard"):
        st.session_state.current_page = 'Dashboard'
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Form Input'

    if 'monthly_budget' not in st.session_state:
        st.session_state.monthly_budget = 0
    if 'categories' not in st.session_state:
        st.session_state.categories = []
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []

    def calculate_decision_score(urgency, frequency, impact):
        """Calculate decision score based on weighted criteria"""
        urgency_weight = 0.5
        frequency_weight = 0.3
        impact_weight = 0.2
        
        decision_score = (urgency * urgency_weight + 
                         frequency * frequency_weight + 
                         impact * impact_weight)
        return decision_score

    def calculate_allocation():
        """Calculate allocation based on priority and decision scores"""
        if not st.session_state.categories:
            return
            
        # Calculate combined scores
        for cat in st.session_state.categories:
            # Priority score (1-5) normalized to 0-1
            priority_normalized = cat['priority'] / 5.0
            
            # Decision score (already 0-1 range from calculate_decision_score)
            decision_score = calculate_decision_score(
                cat.get('urgency', 3) / 5.0,  # Normalize to 0-1
                cat.get('frequency', 3) / 5.0,
                cat.get('impact', 3) / 5.0
            )
            
            # Combined score with equal weight between priority and decision
            cat['combined_score'] = (priority_normalized * 0.5) + (decision_score * 0.5)
        
        # Calculate allocations based on combined scores
        total_combined_score = sum([cat['combined_score'] for cat in st.session_state.categories])
        
        for cat in st.session_state.categories:
            if total_combined_score > 0:
                weight = cat['combined_score'] / total_combined_score
                cat['allocation'] = round(weight * st.session_state.monthly_budget, 2)
            else:
                cat['allocation'] = 0
            
            # Calculate spent amount
            cat['spent'] = 0
            for exp in st.session_state.expenses:
                if exp['category'] == cat['name']:
                    cat['spent'] += exp['amount']

    if st.session_state.current_page == "Form Input":
        st.markdown('<h1 class="title-gradient">📝 Input Keuangan & Decision Category</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.1rem; color: black; margin-bottom: 2rem;">Atur keuangan bulananmu dan tetapkan kategori pengeluaran dengan prioritas dan kriteria keputusan yang tepat</p>', unsafe_allow_html=True)

        # Budget input section
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

        # Decision Category Information
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

        # Category management section
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
        st.markdown('</div>', unsafe_allow_html=True)

        # Categories display with decision scores
        if st.session_state.categories:
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
            st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown('**📊 Cara Perhitungan Alokasi:**', unsafe_allow_html=True)
            st.markdown('''
            - **Combined Score** = (Prioritas Personal × 50%) + (Decision Score × 50%)
            - **Decision Score** = (Urgensi × 50%) + (Frekuensi × 30%) + (Dampak × 20%)
            - **Alokasi** = (Combined Score / Total Combined Score) × Budget Bulanan
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Delete category section
            with st.expander("🗑️ Hapus Kategori"):
                cat_to_delete = st.selectbox("Pilih kategori yang ingin dihapus", [cat['name'] for cat in st.session_state.categories])
                if st.button("🗑️ Hapus Kategori", key="delete_cat"):
                    st.session_state.categories = [cat for cat in st.session_state.categories if cat['name'] != cat_to_delete]
                    st.session_state.expenses = [e for e in st.session_state.expenses if e['category'] != cat_to_delete]
                    calculate_allocation()
                    st.markdown(f'<div class="success-message">✅ Kategori "{cat_to_delete}" berhasil dihapus.</div>', unsafe_allow_html=True)

    elif st.session_state.current_page == "Dashboard":
        st.markdown('<h1 class="title-gradient">📊 Dashboard Keuangan</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 1.2rem; color: black; margin-bottom: 2rem;">Halo, <strong>{st.session_state.username}</strong> 👋, berikut ringkasan keuanganmu</p>', unsafe_allow_html=True)

        st.markdown('<img class="avatar" src="https://ui-avatars.com/api/?name={}&background=667eea&color=fff&size=50" alt="avatar">'.format(st.session_state.username), unsafe_allow_html=True)

        # Summary metrics
        if st.session_state.categories:
            total_allocated = sum([cat['allocation'] for cat in st.session_state.categories])
            total_spent = sum([cat['spent'] for cat in st.session_state.categories])
            remaining_budget = st.session_state.monthly_budget - total_spent
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'''
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="metric-value">Rp {st.session_state.monthly_budget:,.0f}</div>
                    <div class="metric-label">💰 Budget Bulanan</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                    <div class="metric-value">Rp {total_allocated:,.0f}</div>
                    <div class="metric-label">📊 Total Alokasi</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''
                <div class="metric-card" style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);">
                    <div class="metric-value">Rp {total_spent:,.0f}</div>
                    <div class="metric-label">💸 Total Terpakai</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                color = "#11998e" if remaining_budget >= 0 else "#ff416c"
                st.markdown(f'''
                <div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, #38ef7d 100%);">
                    <div class="metric-value">Rp {remaining_budget:,.0f}</div>
                    <div class="metric-label">💵 Sisa Budget</div>
                </div>
                ''', unsafe_allow_html=True)

        # Add expense section
        st.markdown('<div class="category-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subtitle-gradient">➕ Tambah Pengeluaran</h3>', unsafe_allow_html=True)
        with st.form(key="expense_form"):
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.categories:
                    selected_category = st.selectbox("📂 Pilih Kategori", [c['name'] for c in st.session_state.categories])
                else:
                    st.warning("⚠️ Belum ada kategori. Silakan buat kategori terlebih dahulu di Form Input.")
                    selected_category = None
            with col2:
                amount_spent = st.number_input("💰 Jumlah Pengeluaran (Rp)", min_value=0, step=1000)
            exp_submitted = st.form_submit_button("➕ Tambah Pengeluaran")

        if exp_submitted and selected_category:
            st.session_state.expenses.append({
                'category': selected_category,
                'amount': amount_spent
            })
            calculate_allocation()
            st.markdown(f'<div class="success-message">✅ Pengeluaran Rp{amount_spent:,.0f} untuk kategori "{selected_category}" ditambahkan.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Charts and analysis
        if st.session_state.categories:
            st.markdown('<div class="category-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subtitle-gradient">📈 Grafik Pengeluaran vs Alokasi</h3>', unsafe_allow_html=True)
            df = pd.DataFrame(st.session_state.categories)
            df_chart = pd.DataFrame({
                'Kategori': df['name'],
                'Alokasi': df['allocation'],
                'Terpakai': df['spent']
            })
            df_chart_melted = df_chart.melt('Kategori', var_name='Tipe', value_name='Jumlah')

            chart = alt.Chart(df_chart_melted).mark_bar().encode(
                x=alt.X('Kategori:N', title='Kategori'),
                y=alt.Y('Jumlah:Q', title='Jumlah (Rp)'),
                color=alt.Color('Tipe:N', 
                    scale=alt.Scale(domain=['Alokasi', 'Terpakai'], 
                                  range=['#667eea', '#FF6B6B']))
            ).properties(height=400)

            st.altair_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Detailed breakdown with decision analysis
            st.markdown('<div class="category-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="subtitle-gradient">💼 Detail Keuangan & Analisis Decision</h3>', unsafe_allow_html=True)
            
            # Enhanced dataframe with decision scores
            df_enhanced = []
            for cat in st.session_state.categories:
                decision_score = calculate_decision_score(
                    cat.get('urgency', 3) / 5.0,
                    cat.get('frequency', 3) / 5.0,
                    cat.get('impact', 3) / 5.0
                ) * 100
                
                sisa = cat['allocation'] - cat['spent']
                persentase = (cat['spent'] / cat['allocation'] * 100) if cat['allocation'] > 0 else 0
                status = '✅ Aman' if sisa >= 0 else '⚠️ Over Budget'
                
                df_enhanced.append({
                    '📂 Kategori': cat['name'],
                    '🎯 Decision Score': f"{decision_score:.1f}%",
                    '💰 Alokasi (Rp)': cat['allocation'],
                    '💸 Terpakai (Rp)': cat['spent'],
                    '💵 Sisa (Rp)': sisa,
                    '📊 Persentase (%)': f"{persentase:.1f}%",
                    '🔍 Status': status
                })
            
            df_display_enhanced = pd.DataFrame(df_enhanced)
            st.dataframe(df_display_enhanced, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
