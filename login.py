import streamlit as st
import re


# Konfigurasi halaman utama
st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")

# Dummy database (bisa diganti dengan database nyata)
USER = {
    "SPV": {"username": "supervisor", "password": "spv123"},
    "SM": {"username": "manager", "password": "sm123"}
}

# Session state
if "role" not in st.session_state:
    st.session_state.role = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar untuk navigasi login/logout
with st.sidebar:
    st.title("🔐 Login System")

    if not st.session_state.logged_in:
        st.info("Silakan pilih role untuk login.")
        if st.button("🛠 Supervisor (SPV)", use_container_width=True):
            st.session_state.role = "SPV"
            st.rerun()

        if st.button("📊 Section Manager (SM)", use_container_width=True):
            st.session_state.role = "SM"
            st.rerun()
    else:
        st.success(f"✅ Anda masuk sebagai **{st.session_state.role}**")
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

# Header dengan tampilan lebih profesional
st.markdown(
    f"""
    <div style="text-align: center; padding: 15px; background-color: {'#2C3E50' if st.session_state.logged_in else '#34495E'}; 
    border-radius: 10px; color: white; font-size: 24px;">
        {'✅ Welcome ' + st.session_state.role  if st.session_state.logged_in else '🔐 Welcome to the SPK System'}
    </div>
    """,
    unsafe_allow_html=True
)

# Halaman sebelum login agar tidak kosong
if not st.session_state.logged_in:
    st.markdown(
        """
        <div style="text-align: center;">
            <p style='font-size: 18px; color: gray;'>
                Sistem ini digunakan untuk pengelolaan dan persetujuan SPK oleh Supervisor dan Section Manager.
                Silakan login untuk mengakses fitur.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Menampilkan fitur utama dalam bentuk kartu
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="background-color: #ECF0F1; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #2C3E50;">🔎 Monitoring SPK</h4>
                <p style="color: gray;">Lihat status dan detail SPK dengan mudah.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="background-color: #ECF0F1; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #2C3E50;">📝 Persetujuan SPK</h4>
                <p style="color: gray;">Supervisor & Manager dapat menyetujui atau menolak SPK.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    import overview
    overview.overview()


# Form login jika role sudah dipilih
if st.session_state.role and not st.session_state.logged_in:
    st.markdown(
        f"""
        <div style="background-color: #D5DBDB; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px;">
            <b>🔑 Login sebagai {st.session_state.role}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(key="login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit_button = st.form_submit_button("✅ Login")

    if submit_button:
        creds = USER.get(st.session_state.role, {})
        if username == creds.get("username") and password == creds.get("password"):
            st.session_state.logged_in = True
            st.success("✅ Login berhasil! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")
    

# Navigasi halaman setelah login
if st.session_state.logged_in:
    st.sidebar.subheader("📂 Pilih Halaman")

    if st.session_state.role == "SPV":
        page = st.sidebar.selectbox("📌 Pilih Halaman:", ["Tambah SPK", "Update SPK"], index=0)

        if page == "Tambah SPK":
            import add_SPV
            add_SPV.run()
        elif page == "Update SPK":
            import update_SPV
            update_SPV.run()

    elif st.session_state.role == "SM":
        import sm_status
        sm_status.run()
