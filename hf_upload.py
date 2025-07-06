from huggingface_hub import login, create_repo, upload_folder

# Log in to your Hugging Face account
login()  # You’ll be prompted for your HF token

# Create a new repo (or skip if already created)
create_repo(repo_id="bert-sentiment-olist", private=False)

# Upload your model folder
upload_folder(
    folder_path="model",
    repo_id="luhtoo/bert-sentiment-olist",
    repo_type="model"
)
