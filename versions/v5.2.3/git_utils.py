# git_utils.py
import os

REPO_PATH = "C:/Users/andy/PyCharmProjects/Solium"

def push_log_to_git(file_path, commit_message):
    if not os.path.exists(file_path):
        print(f"🚫 Git push skipped. File not found: {file_path}")
        return

    rel_path = os.path.relpath(file_path, start=REPO_PATH).replace("\\", "/")
    os.system(f'git -C "{REPO_PATH}" add "{rel_path}"')
    os.system(f'git -C "{REPO_PATH}" commit -m "{commit_message}"')
    os.system(f'git -C "{REPO_PATH}" push')
    print("🚀 Git push complete")