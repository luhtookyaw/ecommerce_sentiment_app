import streamlit_authenticator as stauth

# List of plain-text passwords
passwords = ['luhtookyaw730', 'welcome2023']

# Initialize Hasher and generate hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Print hashed passwords
print(hashed_passwords)