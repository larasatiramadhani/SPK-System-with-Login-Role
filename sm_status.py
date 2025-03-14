import streamlit as st
import requests
import json
import pandas as pd  

def run():
    # URL Apps Script
    API_URL = "https://script.google.com/macros/s/AKfycbyIPK7-A_MYWin9DH_inZn6om5cVALcWmTCMFQsis80zPPTDd3HdyogpfkrvEPh3oL4Kw/exec"

    # Ambil semua data 
    def get_all_data():
        response = requests.get(f"{API_URL}?action=get_data")
        if response.status_code == 200:
            return response.json()
        return []

    # **Styling UI**
    st.markdown(
        """
        <style>
        .header-box {
            background-color: #2C3E50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .data-box {
            background-color: #F8F9F9;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #D5DBDB;
            margin-bottom: 20px;
        }
        .button-style {
            background-color: #28A745;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            width: 100%;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<div class="header-box">📋 Sistem Approval SPK</div>', unsafe_allow_html=True)

    # **Ambil data**
    all_data = get_all_data()

    if all_data:
        # **Konversi ke DataFrame**
        df = pd.DataFrame(all_data, columns=[
            "Nomor SPK", "Tanggal", "BU", "Jenis Produk", "Line", "Jam Start", "Jam Stop", "Total hour",
            "Speed (kg/jam)", "Rencana Total Output (kg)", "Rencana Total Output (Batch)", "Inner (roll)", "SM", "Alasan"
        ])

        # **Pastikan kolom yang digunakan benar**
        if "Nomor SPK" in df.columns and "SM" in df.columns:
            # **Filter data**
            st.markdown('<div class="data-box">🔍 <b>Filter Data</b></div>', unsafe_allow_html=True)
            filter_option = st.selectbox(
                "Pilih Data yang Ingin Ditampilkan",
                ["Data Keseluruhan", "Approved", "Rejected", "Belum Approved/Rejected"]
            )

            # **Filter berdasarkan opsi**
            if filter_option == "Approved":
                df_filtered = df[df["SM"].astype(str) == "Approved"]
            elif filter_option == "Rejected":
                df_filtered = df[df["SM"].astype(str) == "Rejected"]
            elif filter_option == "Belum Approved/Rejected":
                df_filtered = df[df["SM"].astype(str) == ""]
            else:
                df_filtered = df  # Semua data

            # **Tampilkan tabel**
            st.markdown('<div class="data-box">📊 <b>Tabel Data</b></div>', unsafe_allow_html=True)
            st.dataframe(df_filtered, use_container_width=True, height=300)

            # **Pilih ID untuk update**
            if not df_filtered.empty:
                st.markdown('<div class="data-box">🔄 <b>Update Data</b></div>', unsafe_allow_html=True)
                id_to_update = st.selectbox("Pilih ID untuk diupdate", df_filtered["Nomor SPK"])
                
                if id_to_update:
                    record = df[df["Nomor SPK"] == id_to_update]
                    st.dataframe(record, use_container_width=True)

                    kondisi_status = record["SM"].values[0]

                    # **Cek apakah sudah Approved/Rejected**
                    if kondisi_status in ["Approved", "Rejected"]:
                        st.warning("🚫 Data ini sudah Approved/Rejected oleh Anda.")
                    else:
                        # **Pilih kondisi**
                        kondisi_options = ["Approved", "Rejected"]
                        kondisi = st.selectbox("✅ Pilih Kondisi", kondisi_options)

                        # **Alasan hanya muncul jika Rejected**
                        alasan = ""
                        if kondisi == "Rejected":
                            alasan = st.text_area("❌ Alasan Penolakan")

                        # **Tombol Update**
                        if st.button("📌 Update Data", use_container_width=True):
                            data = {
                                "action": "update_data",
                                "updated_row": {
                                    "Nomor SPK": id_to_update,
                                    "SM": kondisi,
                                    "Alasan": alasan,
                                }
                            }

                            response = requests.post(API_URL, data=json.dumps(data))

                            if response.status_code == 200:
                                st.success("✅ Data berhasil diperbarui!")
                                st.session_state.form_add_reset = True
                                st.rerun()
                            else:
                                st.error("❌ Gagal memperbarui data. Cek kembali input dan koneksi.")

        else:
            st.error("❌ Kolom 'Nomor SPK' atau 'Kondisi SM' tidak ditemukan. Periksa struktur data yang diambil!")

    else:
        st.error("❌ Gagal mengambil data dari Google Sheet.")
        
if __name__ == "__main__":
    run()
