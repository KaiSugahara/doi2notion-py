import json
import os

import requests
from dotenv import load_dotenv

from ..interface.arxiv_paper import ArxivPaper
from ..interface.crossref_paper import CrossRefPaper


class NotionManager:
    def __init__(self):
        self.__load_confidential()
        self.__get_exist_page_ids()

    def __load_confidential(self):
        load_dotenv()
        self.NOTION_SECRET = os.environ.get("NOTION_SECRET")
        self.NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
        if self.NOTION_SECRET is None:
            raise Exception("Set your NOTION_SECRET in .env file!")
        if self.NOTION_DATABASE_ID is None:
            raise Exception("Set your NOTION_DATABASE_ID in .env file!")

    def __get_exist_page_ids(self):
        response = requests.post(
            url=f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query",
            headers={
                "Authorization": f"Bearer {self.NOTION_SECRET}",
                "Notion-Version": "2022-06-28",
            },
        )
        if not response.ok:
            raise Exception("Invalid Certification")

        self.doi2pageid = {
            page["properties"]["DOI"]["title"][0]["plain_text"].lower(): page["id"]
            for page in response.json()["results"]
            if len(page["properties"]["DOI"]["title"]) > 0
        }

    def add_paper(self, paper: ArxivPaper | CrossRefPaper):
        if paper.doi in self.doi2pageid.keys():
            return self.update_paper([paper])
        response = requests.post(
            url="https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {self.NOTION_SECRET}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            data=json.dumps(
                dict(
                    parent=dict(
                        type="database_id", database_id=self.NOTION_DATABASE_ID
                    ),
                    properties=paper.get_notion_properties(),
                )
            ),
        )

        if not response.ok:
            raise Exception(response.content)

        return self

    def update_paper(self, paper: ArxivPaper | CrossRefPaper):
        page_id = self.doi2pageid[paper.doi]
        response = requests.patch(
            url=f"https://api.notion.com/v1/pages/{page_id}",
            headers={
                "Authorization": f"Bearer {self.NOTION_SECRET}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            data=json.dumps(dict(properties=paper.get_notion_properties())),
        )

        if not response.ok:
            raise Exception(response.content)

        return self
