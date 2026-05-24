import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

# =========================
# =========================
# 🔐 CLASSY LOGIN SYSTEM (PAKISTANI ECOMMERCE SaaS STYLE)
# =========================

PASSWORD = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(
        """
        <style>
        /* Background */
        .stApp {
            background: linear-gradient(120deg, #0f172a, #1e293b);
        }

        /* Floating blur blobs */
        .stApp::before {
            content: "";
            position: fixed;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(0,198,255,0.25), transparent 60%);
            top: -100px;
            left: -100px;
            filter: blur(60px);
        }

        .stApp::after {
            content: "";
            position: fixed;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(0,114,255,0.25), transparent 60%);
            bottom: -100px;
            right: -100px;
            filter: blur(60px);
        }

   .login-container {
    max-width: 300px;
    margin: auto;
    margin-top: 90px;
    padding: 17px;
    border-radius: 20px;

    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);

    color: white;
    text-align: center;
}

/* 👇 LOGIN TEXT INSIDE CARD */
.login-container::before {
    content: "LOGIN";
    display: block;
    font-size: 40px;
    font-weight: 700;
    color: white;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

        /* Logo */
        .logo {
            font-size: 44px;
            margin-bottom: 10px;
        }

        /* Title */
        .title {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }

        /* Subtitle */
        .subtitle {
            font-size: 13px;
            color: rgba(255,255,255,0.7);
            margin-bottom: 25px;
        }

        /* Input */
        input {
            border-radius: 10px !important;
        }

        /* Button */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white;
            font-weight: bold;
            padding: 10px;
            border: none;
            transition: 0.3s;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,114,255,0.3);
        }

        /* Footer */
        .footer {
            margin-top: 18px;
            font-size: 11px;
            color: rgba(255,255,255,0.5);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    # Logo / Branding
    st.markdown("<div class='logo'>🛒</div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Shopkeeper Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Pakistan Ecommerce Business Dashboard 🇵🇰</div>", unsafe_allow_html=True)

    # Input
    password_input = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 1])

    with col1:
        login_btn = st.button("🚀 Login")

    with col2:
        st.button("Forgot Password")

    if login_btn:
        if password_input == PASSWORD:
            st.session_state.logged_in = True
            st.success("Welcome back 👋")
            st.rerun()
        else:
            st.error("Incorrect password")

    st.markdown("<div class='footer'>Secure • Ecommerce Ready • Built for Pakistan 🇵🇰</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()



# =========================
# 🏪 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Pakistan Shopkeeper Analytics",
    page_icon="🏪",
    layout="wide"
)

# =========================
# 🎨 TITLE
# =========================
st.title("🏪 Pakistan Shopkeeper Analytics System")
st.markdown("### 📊 Smart Business Insights for Pakistani Shopkeepers")

st.write(
    "Upload your CSV or Excel sales file and get instant analytics, "
    "AI predictions, profit insights, and visual reports."
)

st.divider()

# =========================
# 📁 FILE UPLOAD
# =========================
file = st.file_uploader("📂 Upload CSV or Excel File", type=["csv", "xlsx"])

if file is None:
    st.info("👆 Upload a CSV or Excel file to begin analysis")
    st.stop()

# =========================
# 📁 READ FILE SAFELY
# =========================
try:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
except Exception as e:
    st.error(f"❌ Error reading file: {e}")
    st.stop()

# =========================
# 🧹 CLEAN DATA
# =========================
required_cols = ["date","product","category","branch","quantity","price","cost"]

missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    st.error(f"❌ Missing columns: {missing_cols}")
    st.stop()

df.dropna(inplace=True)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
df.dropna(inplace=True)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df.dropna(subset=["date"], inplace=True)

# =========================
# 💰 CALCULATIONS
# =========================
df["total_sales_pkr"] = df["quantity"] * df["price"]
df["profit_pkr"] = (df["price"] - df["cost"]) * df["quantity"]

df["profit_margin_%"] = (df["profit_pkr"] / df["total_sales_pkr"]) * 100

# =========================
# 📅 MONTHLY ANALYSIS
# =========================
df["month"] = df["date"].dt.to_period("M")
monthly_sales = df.groupby("month")["total_sales_pkr"].sum()

# =========================
# 📊 KPIs
# =========================
total_revenue = df["total_sales_pkr"].sum()
total_profit = df["profit_pkr"].sum()
total_orders = len(df)
avg_order_value = df["total_sales_pkr"].mean()

# =========================
# 📦 PRODUCT ANALYSIS
# =========================
product_sales = df.groupby("product")["quantity"].sum().sort_values(ascending=False)
product_profit = df.groupby("product")["profit_pkr"].sum().sort_values(ascending=False)

best_product = product_sales.idxmax() if not product_sales.empty else "N/A"
top5_products = product_sales.head(5)

# ✅ NEW ADDITION: TOP 10 BEST PRODUCTS
top10_best_products = product_sales.head(10)

# =========================
# 🆕 NEW ADDITION: WORST PRODUCTS
# =========================
worst10_products = product_sales.tail(10)

# =========================
# 🏬 BRANCH ANALYSIS
# =========================
branch_sales = df.groupby("branch")["profit_pkr"].sum().sort_values(ascending=False)
best_branch = branch_sales.idxmax() if not branch_sales.empty else "N/A"

# =========================
# 📊 CUSTOMER BEHAVIOR (NEW)
# =========================
repeat_products = product_sales[product_sales > product_sales.mean()].head(5)

# =========================
# 📦 INVENTORY FORECAST (NEW)
# =========================
restock_suggestion = product_sales.head(5)

# =========================
# 📅 PEAK DAY (NEW)
# =========================
peak_day = df.groupby("date")["total_sales_pkr"].sum().idxmax()

# =========================
# 📉 RISK DETECTION (NEW)
# =========================
daily_sales = df.groupby("date")["quantity"].sum().sort_index()

if len(daily_sales) > 3:
    if daily_sales.iloc[-1] < daily_sales.mean() * 0.5:
        risk = "🚨 Sales dropping fast!"
    else:
        risk = "✅ Stable performance"
else:
    risk = "ℹ Not enough data"

# =========================
# 🤖 PREDICTION
# =========================
window = 3
prediction = int(daily_sales.tail(window).mean()) if len(daily_sales) >= window else int(daily_sales.mean())

# =========================
# 🧠 BUSINESS SCORE (NEW)
# =========================
profit_ratio = total_profit / total_revenue if total_revenue > 0 else 0
business_score = min(100, int((profit_ratio * 100) + (total_orders / 100)))

# =========================
# 📊 DASHBOARD
# =========================
st.success("✅ File analyzed successfully!")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"PKR {total_revenue:,.0f}")
col2.metric("💸 Profit", f"PKR {total_profit:,.0f}")
col3.metric("📦 Best Product", best_product)
col4.metric("⭐ Business Score", business_score)

st.divider()

# =========================
# 🧠 INSIGHTS
# =========================
st.subheader("🧠 AI Business Insights")

st.write(f"🏬 Best Branch: **{best_branch}**")
st.write(f"💰 Avg Order Value: PKR {avg_order_value:.2f}")
st.write(f"📅 Peak Sales Day: {peak_day}")
st.write(f"⚠ Risk Status: {risk}")

st.info(f"🤖 Next Day Sales Prediction: ~{prediction} units")

# =========================
# 🔥 TOP PRODUCTS
# =========================
st.subheader("🔥 Top Products (Top 5)")
st.bar_chart(top5_products)

# =========================
# 🆕 TOP 10 BEST PRODUCTS
# =========================
st.subheader("🏆 Top 10 Best Products")
st.bar_chart(top10_best_products)

# =========================
# 🆕 WORST 10 PRODUCTS
# =========================
st.subheader("💀 Top 10 Worst Products")
st.bar_chart(worst10_products)

# =========================
# 📦 RESTOCK
# =========================
st.subheader("📦 Restock Suggestions")
st.write(restock_suggestion)

# =========================
# 📦 RETAIL INVENTORY STATUS
# =========================

LOW_STOCK_THRESHOLD = 5

# Detect low stock products
low_stock = product_sales[product_sales <= LOW_STOCK_THRESHOLD]

if not low_stock.empty:

    st.warning("⚠ Low Inventory Products Detected")

    inventory_df = pd.DataFrame({
        "Product": low_stock.index,
        "Units Left": low_stock.values,
        "Status": ["Restock Needed"] * len(low_stock)
    })

    st.dataframe(inventory_df)


    

else:
    st.success("✅ Inventory levels are healthy")







# =========================
# 📊 VISUALS
# =========================
st.subheader("📊 Visual Analytics")

left, right = st.columns(2)

with left:
    st.bar_chart(product_sales)

with right:
    st.bar_chart(branch_sales)

st.line_chart(daily_sales)


# =========================
# 📊 VISUALS
# =========================

st.subheader("🥧 Sales Distribution by Category")

category_sales = df.groupby("category")["total_sales_pkr"].sum()

fig, ax = plt.subplots(figsize=(2, 2))  # 👈 THIS controls size

ax.pie(
    category_sales,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.axis("equal")

st.pyplot(fig)

















# =========================
# 📁 DOWNLOAD
# =========================
st.download_button(
    "📥 Download Report",
    df.to_csv(index=False).encode("utf-8"),
    "report.csv",
    "text/csv"
)

# =========================
# =========================
# 🇵🇰 PREMIUM WHOLESALERS NETWORK
# =========================
st.subheader("🇵🇰 Premium Pakistani Wholesalers Network")

st.markdown(
    "💡 *Trusted wholesale markets for fast restocking and bulk purchasing across Pakistan*"
)

# Create structured data
wholesalers_df = pd.DataFrame({
    "🏷 Category": [
        "General Retail 🛒",
        "Groceries 🥫",
        "Electronics 📱",
        "Fashion 👕",
        "Cosmetics 💄",
        "Mobile Accessories 🔌"
    ],
    "🏪 Market / Supplier": [
        "Metro Cash & Carry",
        "Imtiaz Super Market Wholesale",
        "Hall Road Electronics Market",
        "Khaadi Wholesale Center",
        "WB by Hemani Distributors",
        "Saddar Mobile Market"
    ],
    "📍 City": [
        "Karachi",
        "Karachi",
        "Lahore",
        "Karachi",
        "Karachi",
        "Karachi"
    ]
})

# Show styled table
st.dataframe(
    wholesalers_df,
    use_container_width=True,
    hide_index=True
)

# Highlight cards (extra classy feel)
st.markdown("### 🌟 Quick Highlights")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🚚 Fast Restocking Support\nMetro & Imtiaz Networks")

with col2:
    st.info("💰 Bulk Pricing Advantage\nHall Road & Saddar Markets")

with col3:
    st.warning("📦 High Demand Inventory\nElectronics & Fashion Ready Supply")

st.markdown(
    """
    ---
    💡 **Pro Tip:** Always compare 2–3 wholesalers before bulk buying to maximize profit margins and reduce stock risk.
    """
)

# =========================
# 📄 PDF REPORT GENERATION
# =========================
def generate_pdf(df, total_revenue, total_profit, best_product, best_branch, business_score):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from io import BytesIO

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    # ================= TITLE =================
    elements.append(Paragraph("🏪 Pakistan Shopkeeper Analytics FULL REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    # ================= KPI =================
    elements.append(Paragraph("📊 KPI SUMMARY", styles["Heading2"]))

    kpi_data = [
        ["Revenue", f"{total_revenue:,.0f} PKR"],
        ["Profit", f"{total_profit:,.0f} PKR"],
        ["Best Product", best_product],
        ["Best Branch", best_branch],
        ["Business Score", f"{business_score}/100"],
        ["Total Orders", str(len(df))],
        ["Avg Order Value", f"{total_revenue/len(df):.2f}" if len(df) > 0 else "0"],
    ]

    table = Table(kpi_data)
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # ================= TOP PRODUCTS =================
    elements.append(Paragraph("🔥 TOP 10 PRODUCTS", styles["Heading2"]))
    top10 = df.groupby("product")["quantity"].sum().sort_values(ascending=False).head(10)

    for i, (p, v) in enumerate(top10.items(), 1):
        elements.append(Paragraph(f"{i}. {p} - {v} units", styles["Normal"]))

    elements.append(Spacer(1, 15))

    # ================= WORST PRODUCTS =================
    elements.append(Paragraph("💀 WORST 10 PRODUCTS", styles["Heading2"]))
    worst10 = df.groupby("product")["quantity"].sum().sort_values().head(10)

    for i, (p, v) in enumerate(worst10.items(), 1):
        elements.append(Paragraph(f"{i}. {p} - {v} units", styles["Normal"]))

    elements.append(Spacer(1, 15))

    # ================= INSIGHTS =================
    elements.append(Paragraph("🧠 BUSINESS INSIGHTS", styles["Heading2"]))

    profit_ratio = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    insights = [
        f"Profit Margin: {profit_ratio:.2f}%",
        f"Business Health Score: {business_score}/100",
        "Higher score = better business performance",
        "Low selling products should be reviewed or removed"
    ]

    for i in insights:
        elements.append(Paragraph("• " + i, styles["Normal"]))

    elements.append(Spacer(1, 15))

    # ================= SAMPLE DATA =================
    elements.append(Paragraph("📦 SAMPLE DATA (TOP 10 ROWS)", styles["Heading2"]))

    preview = df.head(10)
    data = [preview.columns.tolist()] + preview.values.tolist()

    table2 = Table(data)
    table2.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 7),
    ]))

    elements.append(table2)

    doc.build(elements)
    buffer.seek(0)
    return buffer

# =========================
# 📥 PDF DOWNLOAD BUTTON
# =========================
pdf_buffer = generate_pdf(
    df,
    total_revenue,
    total_profit,
    best_product,
    best_branch,
    business_score
)

st.download_button(
    "📄 Download PDF Report",
    pdf_buffer,
    file_name="shop_report.pdf",
    mime="application/pdf"
)

st.success("🎉 Advanced Analytics Ready 🚀 🇵🇰")