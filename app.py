import streamlit as st

from pawpal_system import Owner, Pet


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")


owner = st.session_state.owner


st.title("🐾 PawPal+")
st.write("This first Streamlit step lets you create pets for one owner.")

st.subheader("Owner")
st.write(f"Current owner: **{owner.name}**")

st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    submitted = st.form_submit_button("Add Pet")

    if submitted:
        pet_name = pet_name.strip()

        if pet_name:
            new_pet = Pet(name=pet_name, species=species)
            owner.add_pet(new_pet)
            st.success(f"{pet_name} was added.")
        else:
            st.warning("Please enter a pet name.")


st.subheader("Current Pets")

if owner.get_pets():
    for index, pet in enumerate(owner.get_pets(), start=1):
        st.write(f"{index}. {pet.name} ({pet.species})")
else:
    st.info("No pets added yet.")
