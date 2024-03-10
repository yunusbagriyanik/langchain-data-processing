import json
import os
import requests


def readJsonFromFile(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            linkedin_data = json.load(file)

        return linkedin_data

    except FileNotFoundError:
        print(f"{filename} not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"{filename} Error: {e}")
        return None


def filter_data(data):
    filtered_data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if filtered_data.get("groups"):
        for group_dict in filtered_data.get("groups"):
            group_dict.pop("profile_pic_url")

    return filtered_data


def scrape_linkedin(linkedin_profile_url: str):
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    data = response.json()
    filtered_data = filter_data(data)

    return filtered_data


def findDataFromJson():
    return readJsonFromFile("linkedin_data.json")
