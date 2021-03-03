import os
import sys
import argparse
import zipfile
import shutil
from project_creator import logging_utils
import requests

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "WARN")
logger = logging_utils.get_logger(__name__, LOGGING_LEVEL)


def display_message(msg):
    print(msg)


def exit_with_error(msg):
    display_message(f"Error: {msg}")
    sys.exit(1)


def create_url(username, repo_name, branch="master"):
    return f"https://github.com/{username}/{repo_name}/archive/{branch}.zip"


def download_file(url, local_prefix=""):
    local_filename = os.path.join(local_prefix, url.split("/")[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def current_directory_is_empty():
    current_path = os.getcwd()
    files = [f for f in os.listdir(current_path)]
    return len(files) == 0


def extract_username_repo(repo_url):
    return repo_url.split("/")


def convert_repo_url(repo_url):
    """Converts the following to "username/repo":

    https://github.com/username/repo.git
    https://github.com/username/repo
    username/repo
    """
    return repo_url.split(".com/")[-1].split(".git")[0]


def extract_zip(filename):
    current_directory = os.getcwd()
    with zipfile.ZipFile(filename, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.filename[-1] == os.path.sep:
                continue
            filename_parts = zip_info.filename.split(os.path.sep)
            zip_info.filename = os.path.join(*filename_parts[1:])
            zip_ref.extract(zip_info, current_directory)


def init(args):
    logger.debug("Repo url: %s", args.repo_url)
    logger.debug("Branch name: %s", args.branch_name)
    logger.debug("Checking that current directory is empty...")
    if not current_directory_is_empty():
        exit_with_error("Current directory is not empty")

    username, repo = extract_username_repo(convert_repo_url(args.repo_url))
    logger.debug("Username: %s", username)
    logger.debug("Repo: %s", repo)
    logger.debug("Branch: %s", args.branch_name)
    display_message(f"Downloading files from {username}/{repo}...")

    github_zip_url = create_url(username, repo, branch=args.branch_name)
    logger.debug("Zip url: %s", github_zip_url)

    logger.debug("Downloading template zip to current directory...")
    try:
        local_zip_file = download_file(github_zip_url)
    except Exception as exception:
        logger.debug("Download exception occurred")
        logger.debug(exception)
        display_message("An error occured during the repo download")
        display_message(f"Repo: {username}/{repo}, Branch: {args.branch_name}")
        exit_with_error(f"Please ensure the following url exists: {github_zip_url}")

    logger.debug("Extracting template zip...")
    extract_zip(local_zip_file)

    logger.debug("Cleaning up...")
    os.remove(local_zip_file)

    display_message("Project setup complete")


def process_arguments():
    parser = argparse.ArgumentParser(description="Creates projects")

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda args: parser.print_help())

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init")
    parser_init.add_argument("repo_url", type=str, metavar="repo-url")
    parser_init.add_argument("--branch-name", type=str, default="master")
    parser_init.set_defaults(func=init)

    args = parser.parse_args()
    args.func(args)


def main():
    process_arguments()
