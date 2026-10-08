import streamlit as st
from datetime import datetime
# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="centered"
)
# ============================================================
# CSS - GIAO DIỆN
# ============================================================
st.markdown("""
<style>
    .main {
        background-color: #fffaf7;
    }
    .title {
        text-align: center;
        color: #8B4513;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #777;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .invoice {
        background-color: #fff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #eee;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    .total {
        font-size: 25px;
        font-weight: bold;
        color: #d35400;
    }
    .thank-you {
        text-align: center;
        font-size: 18px;
        color: #8B4513;
        font-weight: bold;
        margin-top: 20px;
    }
    div.stButton > button {
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# ============================================================
# DỮ LIỆU MENU
# ============================================================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu": 35000,
    "Trà sữa matcha": 40000,
    "Trà sữa socola": 40000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Matcha latte": 45000,
    "Cà phê sữa": 30000
}
SIZE_PRICE = {
    "M": 0,
    "L": 10000
}
TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding": 7000,
    "Kem cheese": 10000
}
SUGAR_LEVEL = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]
ICE_LEVEL = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]
# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""
if "invoice" not in st.session_state:
    st.session_state.invoice = None
# ============================================================
# TIÊU ĐỀ
# ============================================================
st.markdown(
    '<div class="title">🧋 QUÁN TRÀ SỮA</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Hệ thống tính tiền hóa đơn</div>',
    unsafe_allow_html=True
)
st.divider()
# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================
st.subheader("👤 Thông tin khách hàng")
customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)
st.session_state.customer_name = customer_name
# ============================================================
# CHỌN MÓN
# ============================================================
st.subheader("🥤 Thêm món")
col1, col2 = st.columns(2)
with col1:
    drink = st.selectbox(
        "Loại trà sữa / nước",
        list(MENU.keys())
    )
    size = st.selectbox(
        "Size",
        list(SIZE_PRICE.keys())
    )
    topping = st.selectbox(
        "Topping",
        list(TOPPING_PRICE.keys())
    )
with col2:
    sugar = st.selectbox(
        "Đường",
        SUGAR_LEVEL,
        index=0
    )
    ice = st.selectbox(
        "Đá",
        ICE_LEVEL,
        index=0
    )
    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=99,
        value=1,
        step=1
    )
# ============================================================
# TÍNH GIÁ MÓN
# ============================================================
base_price = MENU[drink]
size_price = SIZE_PRICE[size]
topping_price = TOPPING_PRICE[topping]
unit_price = base_price + size_price + topping_price
item_total = unit_price * quantity
st.info(
    f"💰 Đơn giá: **{unit_price:,.0f} VNĐ**  |  "
    f"Thành tiền: **{item_total:,.0f} VNĐ**"
)
# ============================================================
# THÊM MÓN VÀO HÓA ĐƠN
# ============================================================
if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    use_container_width=True,
    type="primary"
):
    if not customer_name.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước.")
    else:
        item = {
            "Tên món": drink,
            "Size": size,
            "Topping": topping,
            "Đường": sugar,
            "Đá": ice,
            "Số lượng": quantity,
            "Đơn giá": unit_price,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item)
        st.success(
            f"✅ Đã thêm {quantity} x {drink} vào hóa đơn."
        )
# ============================================================
# HIỂN THỊ GIỎ HÀNG
# ============================================================
if st.session_state.cart:
    st.divider()
    st.subheader("🛒 Các món đã chọn")
    for index, item in enumerate(st.session_state.cart):
        with st.container(border=True):
            col1, col2, col3 = st.columns([5, 2, 1])
            with col1:
                st.markdown(
                    f"**{index + 1}. {item['Tên món']}**"
                )
                st.caption(
                    f"Size {item['Size']} | "
                    f"Topping: {item['Topping']} | "
                    f"Đường: {item['Đường']} | "
                    f"Đá: {item['Đá']}"
                )
            with col2:
                st.write(
                    f"{item['Số lượng']} x "
                    f"{item['Đơn giá']:,.0f}đ"
                )
            with col3:
                if st.button(
                    "🗑️",
                    key=f"delete_{index}"
                ):
                    st.session_state.cart.pop(index)
                    st.rerun()
            st.write(
                f"**Thành tiền: {item['Thành tiền']:,.0f} VNĐ**"
            )
# ============================================================
# TỔNG TIỀN
# ============================================================
if st.session_state.cart:
    total = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 💰 Tổng tiền")
    with col2:
        st.markdown(
            f'<div class="total">{total:,.0f} VNĐ</div>',
            unsafe_allow_html=True
        )
# ============================================================
# THANH TOÁN
# ============================================================
if st.session_state.cart:
    st.divider()
    if st.button(
        "💳 THANH TOÁN",
        use_container_width=True,
        type="primary"
    ):
        if not customer_name.strip():
            st.error("❌ Vui lòng nhập tên khách hàng.")
        else:
            # Tạo mã hóa đơn
            invoice_id = datetime.now().strftime(
                "HD%Y%m%d%H%M%S"
            )
            # Lưu hóa đơn
            st.session_state.invoice = {
                "id": invoice_id,
                "customer": customer_name,
                "items": st.session_state.cart.copy(),
                "total": total,
                "time": datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            }
            # Xóa giỏ hàng
            st.session_state.cart = []
            st.rerun()
# ============================================================
# HIỂN THỊ HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================
if st.session_state.invoice:
    invoice = st.session_state.invoice
    st.divider()
    st.markdown(
        '<div class="invoice">',
        unsafe_allow_html=True
    )
    st.markdown(
        "<h2 style='text-align:center;'>🧋 HÓA ĐƠN THANH TOÁN</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align:center;'>"
        f"Mã hóa đơn: <b>{invoice['id']}</b>"
        f"</p>",
        unsafe_allow_html=True
    )
    st.write(f"**Khách hàng:** {invoice['customer']}")
    st.write(f"**Thời gian:** {invoice['time']}")
    st.divider()
    # Chi tiết từng món
    for index, item in enumerate(invoice["items"]):
        st.markdown(
            f"**{index + 1}. {item['Tên món']} - Size {item['Size']}**"
        )
        st.write(
            f"- Topping: {item['Topping']}"
        )
        st.write(
            f"- Đường: {item['Đường']} | "
            f"Đá: {item['Đá']}"
        )
        st.write(
            f"- Số lượng: {item['Số lượng']} | "
            f"Đơn giá: {item['Đơn giá']:,.0f} VNĐ"
        )
        st.write(
            f"**Thành tiền: {item['Thành tiền']:,.0f} VNĐ**"
        )
        if index < len(invoice["items"]) - 1:
            st.divider()
    st.divider()
    st.markdown(
        f"""
        <div style="text-align:right;">
            <p style="font-size:18px;">Tổng số món:
            <b>{sum(item['Số lượng'] for item in invoice['items'])}</b>
            </p>
            <p style="font-size:25px; color:#d35400;">
                <b>TỔNG THANH TOÁN: {invoice['total']:,.0f} VNĐ</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="thank-you">❤️ Cảm ơn quý khách! Hẹn gặp lại!</div>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    # Tạo hóa đơn mới
    if st.button(
        "🆕 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):
        st.session_state.invoice = None
        st.session_state.customer_name = ""
        st.rerun()
# ============================================================
# CHÂN TRANG
# ============================================================
st.divider()
st.caption(
    "🧋 Milk Tea POS • Ứng dụng quản lý hóa đơn trà sữa"
)
