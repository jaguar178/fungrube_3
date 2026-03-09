import streamlit as st
from supabase import create_client, Client

# Supabase Verbindung
SUPABASE_URL = "DEINE_SUPABASE_URL"
SUPABASE_KEY = "DEIN_ANON_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Fundgrube App")

# -------------------------
# LOGIN
# -------------------------

st.sidebar.header("Login")

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    try:
        user = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = user
        st.success("Eingeloggt")
    except:
        st.error("Login fehlgeschlagen")

if "user" not in st.session_state:
    st.stop()

user_id = st.session_state.user.user.id

# -------------------------
# FUNDSTÜCK HINZUFÜGEN
# -------------------------

st.header("Fundstück melden")

category = st.selectbox(
    "Kategorie",
    ["hose", "pullover", "muetze"]
)

fundort = st.text_input("Fundort")
farbe = st.text_input("Farbe")
groesse = st.text_input("Größe")
marke = st.text_input("Marke")

if st.button("Speichern"):

    data = {
        "user_id": user_id,
        "category": category,
        "fundort": fundort,
        "farbe": farbe,
        "groesse": groesse,
        "marke": marke
    }

    supabase.table("clothing").insert(data).execute()

    st.success("Fundstück gespeichert")

# -------------------------
# SUCHE
# -------------------------

st.header("Suche")

search_farbe = st.text_input("Farbe suchen")
search_fundort = st.text_input("Fundort suchen")

query = supabase.table("clothing").select("*")

if search_farbe:
    query = query.eq("farbe", search_farbe)

if search_fundort:
    query = query.eq("fundort", search_fundort)

result = query.execute()

# -------------------------
# ERGEBNISSE
# -------------------------

st.header("Fundstücke")

for item in result.data:

    st.write("Kategorie:", item["category"])
    st.write("Fundort:", item["fundort"])
    st.write("Farbe:", item["farbe"])
    st.write("Größe:", item["groesse"])
    st.write("Marke:", item["marke"])

    if st.button(f"Löschen {item['id']}"):
        supabase.table("clothing").delete().eq("id", item["id"]).execute()
        st.experimental_rerun()

    st.divider()
