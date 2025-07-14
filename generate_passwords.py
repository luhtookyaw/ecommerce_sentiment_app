import streamlit_authenticator as stauth

# List of plain-text passwords
passwords = ['admin123']

# Initialize Hasher and generate hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Print hashed passwords
print(hashed_passwords)