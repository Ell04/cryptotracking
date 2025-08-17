"""

Script to build prompts for LLMs using predefined templates.

"""

import os
import re

def get_articles(articles_dir):
    """
    Get a list of articles from the specified directory.

    Args:
        articles_dir (str): The directory containing the article files.

    Returns:
        list: A list of article contents with their corresponding dates.
    """
    files = []
    for file in os.listdir(articles_dir):
        if file.endswith(".json"):
            with open(os.path.join(articles_dir, file), 'r') as f:
                files.append(f.read() + "<date>" + get_date_from_filename(file) + "</date>")
    return files

def get_date_from_filename(filename):
    """

    Extract the date from the filename.

    Args:
        filename (str): The name of the file to extract the date from.

    Returns:
        str: The extracted date, or None if no date is found.

    """
    match = re.search(r'processed_events_for_(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None

if __name__ == "__main__":

    print(get_articles(os.path.join(os.getcwd(), "data", "bitcoin_events")))