import os

import git


repo = git.Repo(search_parent_directories=True)
version = repo.git.describe("--tags")

with open(os.path.join(os.getcwd(), "src", "zeal", "version.py"), "w") as file:
    file.write(f'build_version = "{version}"\n')

#print(f"::set-output name=version::{version}")