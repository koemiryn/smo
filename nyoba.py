import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
import os
import random
from io import BytesIO
import requests

# Authentication function
def authenticate(username, password, user_info):
    if username in user_info.index and password == user_info.loc[username, "password"]:
        return True
    return False

# Quiz stress detection
def stress_detection_page():
    st.title("STRESS ME OUT")
    st.write("Pilihlah sesuai dengan kondisi Anda hari ini.")

    # Questions
    questions = [
        "Seberapa sering anda merasa kewalahan dengan pekerjaan Anda?",
        "Apakah Anda sering mengalami kesulitan untuk tidur?",
        "Seberapa sering Anda merasakan gugup sebelum melakukan suatu aktivitas?",
    ]

    # User responses
    user_responses = {}

    # Quiz buttons
    for i, question in enumerate(questions, start=1):
        user_response = st.radio(f"Q{i}: {question}", options=["Tidak pernah", "Jarang", "Sering", "Setiap saat"])
        numerical_response = {"Tidak pernah": 0, "Jarang": 1, "Sering": 2, "Setiap saat": 3}
        user_responses[f"Q{i}"] = numerical_response[user_response]

    # Save to CSV
    save_responses(user_responses)

    stress_level = calculate_stress_level(user_responses)

    # Display stress level
    st.subheader("Stress Level:")
    if stress_level == "Rendah":
        st.success(f"😊 Stress level Anda {stress_level}! Menjaga tingkat stres tetap rendah adalah kunci untuk kesejahteraan mental.")
    elif stress_level == "Normal":
        st.warning(f"😐 Stress level Anda {stress_level}. Menjaga tingkat stres tetap normal melibatkan sejumlah kegiatan positif yang bisa mencegah tingkat stres menjadi lebih tinggi.")
    else:
        st.error(f"😰 Stress level Anda {stress_level}. Menurunkan tingkat stres tinggi melibatkan inisiatif dari diri sendiri, apabila tingkat stress sudah tinggi patut diwaspadai dan ditangani.")

    # Display recommendations
    st.subheader("Apa yang harus dilakukan?")
    if stress_level == "Rendah":
        st.success(f"Karena Stress level Anda {stress_level}, Anda dapat meningkatkan ibadah kepada Tuhan Yang Maha Esa, dan tetap melakukan berbagai kegiatan positif!")
    elif stress_level == "Normal":
        st.warning(f"Karena Stress level Anda {stress_level}, Anda dapat berolahraga dengan teratur, melakukan hobi kesukaan Anda, baik itu yang menenangkan atau tidak, dan berkumpul bersama keluarga atau teman.")
    else:
        st.error(f"Karena Stress level Anda {stress_level}. Anda dapat membicarakan keluhan Anda kepada seseorang yang percaya dan mencari bantuan psikologi kepada ahli psikologi dan mencari jalan keluar dari stress Anda.")

# YouTube recommendation page
def youtube_recommendation_page():
    st.title("YouTube Video Recommendations")
    st.write("Check out this stress-relief video!")

    # YouTube video link
    youtube_video_link = "https://youtu.be/LeFkkFCFbmE?feature=shared"
    st.video(youtube_video_link)

    # YouTube thumbnail 
    youtube_thumbnail_link = "https://i.ytimg.com/vi/LeFkkFCFbmE/maxresdefault.jpg"
    
    # Display YouTube thumbnail 
    thumbnail_html = f'<p align="center"><a href="{youtube_video_link}" target="_blank"><img src="{youtube_thumbnail_link}" width="200"></a></p>'
    st.markdown(thumbnail_html, unsafe_allow_html=True)

# Calculate stress level
def calculate_stress_level(user_responses):
    total_response = sum(user_responses.values())
    
    if total_response <= 3:
        return "Rendah"
    elif total_response <= 6:
        return "Normal"
    else:
        return "Tinggi"

# Save responses
def save_responses(user_responses):
    today = datetime.now().date()
    filename = f"weekly_report_{today}.csv"

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date"] + list(user_responses.keys()))

    new_data = pd.DataFrame({"Date": [today], **user_responses})
    df = pd.concat([df, new_data], ignore_index=True)

    df.to_csv(filename, index=False)

# Reset weekly report
def reset_weekly_report():
    filename = f"weekly_report_{datetime.now().date()}.csv"
    try:
        os.remove(filename)
        st.success("🔄 Weekly Report has been reset!")
    except FileNotFoundError:
        st.warning("No Weekly Report to reset.")

# Generate weekly report
def generate_weekly_report():
    st.title("Weekly Stress Report")
    try:
        latest_report = pd.read_csv(f"weekly_report_{datetime.now().date()}.csv")
        st.write("Latest weekly report")
        st.table(latest_report)
    except FileNotFoundError:
        st.warning("No Weekly Report for this week.")

# Recommend nearest psychologist
def recommend_nearest_psychologist_page(user_location, selected_city):
    psychologist_info = {
        "Bandar Lampung": [
            {"name": "Psikolog Yurni, M.Psi.", "profile_link": "https://www.halodoc.com/tanya-dokter/yurni-m-psi-psikolog"}
        ],
        "Metro": [
            {"name": "Octa Reni Setiawati, S.Psi, M.Psi, Psikolog", "profile_link": "https://www.praktikpsikologi.com/"}
        ],
        "Jakarta": [
            {"name": "Jennyfer, M.Psi., Psikolog", "profile_link": "https://www.instagram.com/jen.psikolog/"}
        ],
        "Surabaya": [
            {"name": "Ratna Sari M.Psi.,Psikolog", "profile_link": "https://ertamentari.com/"}
        ],
        "Yogyakarta": [
            {"name": "Mirza Adi Prabowo, M.Psi., Psikolog", "profile_link": "https://mirzaadi.my.id/"}
        ],
        "Medan": [
            {"name": "Dr. Manahap Cerarius Fransiskus Pardosi M.Ked, Sp.KJ", "profile_link": "https://www.halodoc.com/tanya-dokter/dr-manahap-cerarius-fransiskus-pard"}
        ],
        "Makassar": [
            {"name": "Widia Julianti Siddik, S.Psi., M.Psi., Psikolog", "profile_link": "https://widiapsi.carrd.co/"}
        ]
    }

    psychologists = psychologist_info.get(selected_city, [])

    for psychologist in psychologists:
        st.success(f"Nearest psychologist for you in {selected_city}: {psychologist['name']}")
        st.markdown(f"Link Halodoc: [{psychologist['name']}]({psychologist['profile_link']})")

# Sign up function
def sign_up():
    st.title("Sign Up Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Sign Up 👉"):
        # Create a new DataFrame with the new user information
        user_info = pd.DataFrame({"username": [new_username], "password": [new_password]})

        # Save the new user_info to user_info.csv, overwriting existing data
        user_info.to_csv("user_info.csv", index=False)
        st.success("🎉 Successfully signed up!")

# Main function
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Sidebar
    menu = ["Login", "Sign Up", "Deteksi Tingkat Stress", "Weekly Report", "Reset Report", "Psikolog Terdekat", "Rekomendasi Video"]
    choice = st.sidebar.selectbox("Navigation", menu, key="sidebar_navigation")

    selected_city = None  # Define selected_city here to ensure it's accessible

    if choice == "Login":
        if not st.session_state.logged_in:
            st.title("Login Page")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login 👉"):
                user_info = pd.read_csv("user_info.csv", index_col=0)
                if authenticate(username, password, user_info):
                    st.session_state.logged_in = True
                    st.success("🎉 Successfully logged in!")
                else:
                    st.error("❌ Invalid username or password.")
    elif choice == "Sign Up":
        if not st.session_state.logged_in:
            sign_up()
    elif choice == "Deteksi Tingkat Stress":
        if st.session_state.logged_in:
            stress_detection_page()
    elif choice == "Weekly Report":
        if st.session_state.logged_in:
            generate_weekly_report()
    elif choice == "Reset Report":
        if st.session_state.logged_in:
            reset_weekly_report()
    elif choice == "Rekomendasi Video":
        if st.session_state.logged_in:
            youtube_recommendation_page()
    elif choice == "Psikolog Terdekat":
        if st.session_state.logged_in:
            # Recommendation of the Nearest Psychologist
            st.title("Rekomendasi Psikolog Terdekat")
            cities = ["Bandar Lampung", "Metro", "Jakarta", "Surabaya", "Yogyakarta", "Medan", "Makassar"]
            selected_city = st.selectbox("Pilih kota Anda:", cities, key="selected_city_dropdown")

            if st.button("Cari Psikolog Terdekat"):
                try:
                    city_coordinates = {
                        "Bandar Lampung": (-5.3971, 105.2663),
                        "Metro": (-5.1136, 105.3067),
                        "Jakarta": (-6.2088, 106.8456),
                        "Surabaya": (-7.2575, 112.7521),
                        "Yogyakarta": (-7.7971, 110.3688),
                        "Medan": (3.5896, 98.6731),
                        "Makassar": (-5.1477, 119.4327)
                    }
                    user_location = city_coordinates.get(selected_city)

                    if user_location:
                        recommend_nearest_psychologist_page(user_location, selected_city) 
                    else:
                        st.error("Kota tidak valid. Pilih kota dari dropdown.")
                except KeyError:
                    st.error("Terjadi kesalahan dalam memproses. Silakan coba lagi.")

if __name__ == "__main__":
    main()
