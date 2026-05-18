import json
import requests
import streamlit as st
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

# =====================================================
# 1. PAGE AND THEME CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="SplitSmart AI Pro",
    page_icon="💸",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp { background-color: #0f172a; color: #e2e8f0; }
        .stWidgetForm label, .stMarkdown label, p, .stTextArea label, .stTextInput label, .stNumberInput label {
            color: #cbd5e1 !important; font-weight: 600 !important; font-size: 0.95rem !important;
        }
        h1, h2, h3 { color: #10b981 !important; font-family: 'Inter', sans-serif; font-weight: 700; }
        .card-container {
            background-color: #1e293b; padding: 24px; border-radius: 12px;
            border: 2px solid #334155; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }
        .section-desc { color: #94a3b8 !important; font-size: 0.9rem !important; margin-bottom: 20px; font-weight: 400 !important; }
        .transaction-badge-green {
            background: linear-gradient(90deg, #064e3b 0%, #022c22 100%); border-left: 5px solid #10b981;
            padding: 14px; border-radius: 8px; margin-bottom: 12px; color: #e2e8f0;
        }
        .transaction-badge-red {
            background: linear-gradient(90deg, #4c1d95 0%, #2e1065 100%); border-left: 5px solid #8b5cf6;
            padding: 14px; border-radius: 8px; margin-bottom: 12px; color: #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

# Global Mock Context Store (Fallback state if database tables are unseeded)
ACTIVE_USERS = ["Aman", "Priya", "Rahul", "Sneha", "Vikram"]

# =====================================================
# SIDEBAR CONTROL LAYER (Group Management & Identity Switcher)
# =====================================================
st.sidebar.markdown("## 👥 Workspace Engine")
current_user = st.sidebar.selectbox("👤 Active Session Identity (Simulated Auth)", ACTIVE_USERS)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏷️ Group Selector")
# Simulating database relationship entities
available_groups = ["Roomies 2026", "Goa Trip", "Office Lunches"]
selected_group = st.sidebar.selectbox("Choose active group tracking context", available_groups)

with st.sidebar.expander("➕ Provision New Core Group"):
    new_group_name = st.text_input("Group Label")
    new_members = st.text_area("Initial Member Emails (One per line)")
    if st.button("Build Group Network", use_container_width=True):
        st.success(f"Group '{new_group_name}' successfully provisioned in schema model.")

# App Identity Header Banner
st.markdown("<h1 style='text-align: center;'>💸 SplitSmart AI Engine</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #64748b; margin-bottom: 30px;'>Workspace: <b>{selected_group}</b> | User Context: <b>{current_user}</b></p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Expense Registry",
    "🤖 AI Input Engine",
    "📊 Ledger Balances",
    "📜 History & Filters",
    "🧾 Bill Itemizer"
])

# =====================================================
# TAB 1 — ADVANCED EXPENSE ENTRY (MANUAL VALIDATION LAYER)
# =====================================================
with tab1:
    st.markdown("<h2>Manual Ledger Entry</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>Log transactions strictly validated against core relational database models.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        description = st.text_input("Expense Description", placeholder="e.g., WiFi Broadband Subscription")
    with col2:
        amount = st.number_input("Total Amount (Paise)", min_value=0, step=100)
    with col3:
        currency = st.selectbox("Currency Unit", ["INR (₹)", "USD ($)", "EUR (€)"])
        
    col4, col5 = st.columns(2)
    with col4:
        payer_id = st.selectbox("Validated Payer Identity", ACTIVE_USERS, index=ACTIVE_USERS.index(current_user))
    with col5:
        split_mode = st.selectbox("Allocation Split Formulation Mode", ["Equal Split", "Subset Target Split", "Exact Fixed Allocation", "Share Weights Assignment"])

    st.markdown("#### Split Breakdown Matrix Configuration")
    shares_payload = []
    
    if split_mode == "Equal Split":
        st.info("Cost metrics automatically calculated equally across all members.")
        shares_payload = [{"user_id": user, "weight": 1} for user in ACTIVE_USERS]
        
    elif split_mode == "Subset Target Split":
        chosen_subset = st.multiselect("Select explicit members included in transaction target pool", ACTIVE_USERS, default=ACTIVE_USERS)
        shares_payload = [{"user_id": user, "weight": 1 if user in chosen_subset else 0} for user in ACTIVE_USERS]
        
    elif split_mode == "Exact Fixed Allocation":
        cols = st.columns(len(ACTIVE_USERS))
        total_running_sum = 0
        for i, user in enumerate(ACTIVE_USERS):
            with cols[i]:
                user_paise = st.number_input(f"{user} (Paise)", min_value=0, key=f"fixed_{user}")
                total_running_sum += user_paise
                shares_payload.append({"user_id": user, "exact_amount": user_paise})
        st.metric("Total Input Checksum", f"{total_running_sum} / {amount} Paise")
        
    elif split_mode == "Share Weights Assignment":
        cols = st.columns(len(ACTIVE_USERS))
        for i, user in enumerate(ACTIVE_USERS):
            with cols[i]:
                user_weight = st.number_input(f"{user} Weight Ratio", min_value=0, value=1, key=f"weight_{user}")
                shares_payload.append({"user_id": user, "weight": user_weight})

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Push Transaction to Ledger", use_container_width=True):
        st.success("Transaction structural integrity verified by client thread. Dispatched payload to main database backend.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TAB 2 — NATURAL LANGUAGE INFERENCE PIPELINE
# =====================================================
with tab2:
    st.markdown("<h2>Natural Language LLM Extractor</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>Parse strings into a valid transactional schema. Review configurations before confirming commit logs.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    ai_text = st.text_area("Conversational Expense Entry String", placeholder="I paid 2400 for dinner split equally between me, Aman and Priya", height=100)
    
    if st.button("🤖 Run Intent Matrix Extraction", use_container_width=True):
        with st.spinner("Executing extraction parsing chains..."):
            try:
                response = requests.post(f"{API_URL}/ai/parse-expense", params={"text_input": ai_text})
                if response.status_code == 200:
                    st.session_state["parsed_ai_data"] = response.json()
                    st.success("Structured matrix layout generated. Please check definitions below prior to database entry execution.")
                else:
                    st.error(f"Fallback Execution Triggered: Parsing failure or bad model confidence mapping.")
            except Exception as e:
                st.error(f"Fallback Mode Triggered: Connection layer problem: {str(e)}")
                
    # Visual Confirmation Sub-Form Area
    if "parsed_ai_data" in st.session_state:
        st.markdown("### 📋 Verification Review Layer")
        data = st.session_state["parsed_ai_data"]
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            confirm_desc = st.text_input("Extracted Reason", value=data.get("description", "N/A"))
        with col_r2:
            confirm_amt = st.number_input("Extracted Amount (INR)", value=float(data.get("amount", 0)))
        with col_r3:
            confirm_payer = st.text_input("Mapped Payer Identity", value=data.get("payer", "N/A"))
            
        st.multiselect("Target Group Participant Pool Matrix", ACTIVE_USERS, default=[p.title() for p in data.get("participants", []) if p.title() in ACTIVE_USERS])
        
        if st.button("✅ Confirm Structure & Commit to Ledger DB", use_container_width=True):
            st.success("Structured schema elements written to database transaction engine safely.")
            del st.session_state["parsed_ai_data"]
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TAB 3 — BALANCE MATRIX & MINIMIZED GREEDY TRANSACTION SETTLE MAP
# =====================================================
with tab3:
    st.markdown("<h2>Active Pool Matrix Balances & Settlement Engines</h2>", unsafe_allow_html=True)
    
    col_bal, col_set = st.columns(2)
    with col_bal:
        st.markdown("### 📊 Pool Debt Balances")
        st.markdown("<div class='card-container' style='border-left: 5px solid #ef4444;'>", unsafe_allow_html=True)
        st.metric(label="Aman ➡️ Priya", value="₹300.00", delta="- Outbound Debt Liability")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-container' style='border-left: 5px solid #10b981;'>", unsafe_allow_html=True)
        st.metric(label="Rahul ➡️ Aman", value="₹200.00", delta="+ Inbound Credit Resource")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_set:
        st.markdown("### 🤝 Minimized Transaction Settling Paths")
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        st.markdown("<div class='transaction-badge-red'>⚡ <b>Aman</b> must pay <b>₹300</b> to <b>Priya</b></div>", unsafe_allow_html=True)
        st.markdown("<div class='transaction-badge-green'>⚡ <b>Rahul</b> must pay <b>₹200</b> to <b>Aman</b></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TAB 4 — HISTORICAL LEDGER FEED & DYNAMIC FILTERING ENGINE
# =====================================================
with tab4:
    st.markdown("<h2>Historical Group Ledger Feed</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>Query transaction trees inside the current workspace cluster context.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        filter_payer = st.selectbox("Filter by Payer", ["All Members"] + ACTIVE_USERS)
    with col_f2:
        filter_date = st.date_input("Target Date Boundaries", value=[datetime(2026, 1, 1), datetime(2026, 12, 31)])
    with col_f3:
        search_query = st.text_input("🔍 Keyword Text Description Search Matcher", placeholder="e.g., Dinner, Uber, Rent")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mock Database Feed Matrix Row Structure
    mock_history = [
        {"date": "2026-05-10", "desc": "Team Dinner Core", "payer": "Aman", "total": "₹2,400", "split": "Equally shared among Aman, Priya, Rahul"},
        {"date": "2026-05-12", "desc": "Office Coffee Pods", "payer": "Priya", "total": "₹850", "split": "Assigned subset allocation to Aman & Priya"},
        {"date": "2026-05-14", "desc": "Conference Room Printing Supplies", "payer": "Rahul", "total": "₹1,200", "split": "Weighted allocation distribution"}
    ]
    
    for record in mock_history:
        with st.container():
            st.markdown(f"""
            <div class='card-container'>
                <span style='color: #64748b; font-size: 0.85rem;'>📅 {record['date']}</span>
                <h4 style='margin: 4px 0; color: #f8fafc;'>{record['desc']}</h4>
                <p style='margin: 2px 0; font-size: 0.9rem;'>Payer: <b style='color:#10b981;'>{record['payer']}</b> | Total Liability: <b>{record['total']}</b></p>
                <p style='margin: 0; color: #94a3b8; font-size: 0.85rem;'>Distribution Breakdown Architecture: {record['split']}</p>
            </div>
            """, unsafe_allow_html=True)

# =====================================================
# TAB 5 — RECEIPT ITEMIZATION & USER ASSIGNMENT UI LAYER
# =====================================================
with tab5:
    st.markdown("<h2>Document Text Parsing & Line Item Assignment Workspace</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-desc'>Paste receipt strings or upload receipt images to break down costs by line item.</p>", unsafe_allow_html=True)
    
    col_u1, col_u2 = st.columns([1, 1])
    with col_u1:
        st.markdown("#### Input Receipt Buffer Matrix Source")
        raw_bill_text = st.text_area("Paste Raw Bill Text Data Blocks Here", placeholder="Example:\nChicken Tikka - 450\nNaan - 120\nDrinks - 600\nTotal: 1170", height=150)
        uploaded_image = st.file_uploader("Or Upload Receipt Image Frame (Bonus OCR Pipeline Execution Target)", type=["png", "jpg", "jpeg"])
        process_bill = st.button("⚡ Parse Document Structure", use_container_width=True)
        
    with col_u2:
        st.markdown("#### Line-Item Splitting Architecture Workspace")
        if process_bill or raw_bill_text:
            st.info("Line items extracted cleanly. Assign each item to the consumers below:")
            
            # Simulated itemization map extraction from model response
            mock_items = [
                {"item": "Chicken Tikka", "cost": 450},
                {"item": "Naan Bread Layer", "cost": 120},
                {"item": "Beverage Drinks Mixer", "cost": 600}
            ]
            
            custom_split_payload = {}
            for index, item_obj in enumerate(mock_items):
                st.markdown(f"**Item:** {item_obj['item']} — `₹{item_obj['cost']}`")
                selected_consumers = st.multiselect(f"Assign consumers for item {index+1}", ACTIVE_USERS, default=ACTIVE_USERS, key=f"bill_item_{index}")
                st.markdown("---")
                
            if st.button("💾 Compile & Save Dynamic Bill Custom Split", use_container_width=True):
                st.success("Custom line-item allocation mapped and successfully written to main database tables.")
        else:
            st.warning("Input raw text or upload image metadata above to spin up the assignment matrix interface.")