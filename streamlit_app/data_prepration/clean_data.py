import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm

# Load dataset
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

# Drop irrelevant columns
def drop_irrelevant_columns(df):
    columns_to_drop = [
        'published_timestamp', 'published_date',
        'published_time', 'year', 'month', 'day', 'profit'
    ]
    return df.drop(columns=columns_to_drop)

# Categorize course status
def categorize_course_status(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        html = response.text

        # Non-English check case
        if '<html lang="en"' not in html and 'lang="en"' not in html:
            return "Non-English"

        # Error page case
        error_tag = soup.find('h1', string=lambda x: x and "we can’t find the page you’re looking for" in x.lower())
        if error_tag:
            return "Error Page"

        # Course unavailable case
        title_check = soup.find('div', {'data-purpose': 'safely-set-inner-html:limited-access-container:title'})
        subtitle_check = soup.find('div', {'data-purpose': 'safely-set-inner-html:limited-access-controller:subtitle'})
        if (title_check and "no longer accepting enrollments" in title_check.get_text(strip=True).lower()) or \
           (subtitle_check and "no longer accepting enrollments" in subtitle_check.get_text(strip=True).lower()):
            return "Course Unavailable"

        # Private course case
        private_tag = soup.find('div', string=lambda x: x and "this is a private course." in x.lower())
        if private_tag:
            return "Private Course"

        # Standard description
        description_container = soup.find('div', {'data-purpose': 'safely-set-inner-html:description:description'})
        if description_container and description_container.find_all('p'):
            return "Valid"

        # Alternate known container
        alt_container = soup.find('div', {'class': 'ud-component--clp--description'})
        if alt_container and alt_container.find_all('p'):
            return "Alternate Description Location"

        # Nothing found
        return "No Description Found"

    except requests.exceptions.HTTPError as err:
        return f"Error {err.response.status_code}"
    except Exception:
        return "Failed"

# Extract course descriptions
def extract_course_description(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Standard description container
        description_container = soup.find('div', {'data-purpose': 'safely-set-inner-html:description:description'})
        if description_container and description_container.find_all('p'):
            return "\n".join([p.get_text(strip=True) for p in description_container.find_all('p')])

        # Alternate known container
        alt_container = soup.find('div', {'class': 'ud-component--clp--description'})
        if alt_container and alt_container.find_all('p'):
            return "\n".join([p.get_text(strip=True) for p in alt_container.find_all('p')])

        return "No Description Found"
    except requests.exceptions.HTTPError as err:
        return f"Error {err.response.status_code}"
    except Exception:
        return "Failed"

# Clean dataset
def clean_dataset(df):
    # Categorize URLs
    urls = df['url'].tolist()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        status_list = list(tqdm(executor.map(categorize_course_status, urls), total=len(urls)))
    df['status'] = status_list

    # Filter valid courses
    df = df[df['status'] == "Valid"].copy()

    # Drop duplicates
    df.drop_duplicates(subset='url', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Extract descriptions
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        description_list = list(tqdm(executor.map(extract_course_description, df['url']), total=len(df)))
    df['descriptions'] = description_list

    # Filter out failed extractions
    df = df[df['descriptions'] != "Failed"].copy()
    df.drop_duplicates(subset='descriptions', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Drop status column
    df.drop(columns=['status'], inplace=True)

    return df