import os
from dotenv import load_dotenv
from crossref.restful import Works
import requests
import json

from bin.meta_parser import meta_parser

class NotFoundDOI(Exception):
    pass

class updater:

    def __get_metadata(self):

        """
            func:
                Retrieve a metadata of a paper
            args:
                None
            returns:
                - the metadata
        """

        self.response = Works().doi(self.DOI)

        if self.response is None:
            raise NotFoundDOI(f"Specified DOI, {self.DOI} does not exist in CrossRef API")
        
        return self.response
    
    def __get_doi2pageid(self):

        """
            func:
                Refer to the (current) database to obtain a mapping between DOIs and page IDs
            args:
                None
            returns:
                - a mapping between DOIs and page IDs
        """

        # Load Confidential
        load_dotenv()
        if (NOTION_SECRET := os.environ.get("NOTION_SECRET")) is None: raise Exception("Set your NOTION_SECRET in .env file!")
        if (NOTION_DATABASE_ID := os.environ.get("NOTION_DATABASE_ID")) is None: raise Exception("Set your NOTION_DATABASE_ID in .env file!")

        # Get Database Pages
        response = requests.post(
            url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
            headers = {
                "Authorization": f"Bearer {NOTION_SECRET}",
                "Notion-Version": "2022-06-28",
            },
        )
        if not response.ok: raise Exception("Invalid Certification")

        return {
            page["properties"]["DOI"]["title"][0]["plain_text"].lower(): page["id"]
            for page in response.json()["results"]
            if len(page["properties"]["DOI"]["title"]) > 0  # Exclude pages with empty title
        }

    def __add_page_to_database(self):

        """
            func:
                Update a new page (paper data) according to constructed properties
            args:
                None
            returns:
                None
        """

        # Load Confidential
        load_dotenv()
        if (NOTION_SECRET := os.environ.get("NOTION_SECRET")) is None: raise Exception("Set your NOTION_SECRET in .env file!")
        if (NOTION_DATABASE_ID := os.environ.get("NOTION_DATABASE_ID")) is None: raise Exception("Set your NOTION_DATABASE_ID in .env file!")

        # Add to Database
        response = requests.post(
            url = f"https://api.notion.com/v1/pages",
            headers = {
                "Authorization": f"Bearer {NOTION_SECRET}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            data = json.dumps( dict( parent=dict( type="database_id", database_id=NOTION_DATABASE_ID ), properties=self.properties ) ),
        )

        if not response.ok:

            raise Exception( response.content )

        return self
    
    def __update_page_in_database(self):

        """
            func:
                Update a existing page (paper data) according to constructed properties
            args:
                None
            returns:
                None
        """

        # Load Confidential
        load_dotenv()
        if (NOTION_SECRET := os.environ.get("NOTION_SECRET")) is None: raise Exception("Set your NOTION_SECRET in .env file!")
        if (NOTION_DATABASE_ID := os.environ.get("NOTION_DATABASE_ID")) is None: raise Exception("Set your NOTION_DATABASE_ID in .env file!")

        # Add to Database
        page_id = self.doi2pageid[self.DOI]
        response = requests.patch(
            url = f"https://api.notion.com/v1/pages/{page_id}",
            headers = {
                "Authorization": f"Bearer {NOTION_SECRET}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            data = json.dumps( dict( properties=self.properties ) ),
        )

        if not response.ok:

            raise Exception( response.content )

        return self
        
    def set_properties(self, DOI):

        """
            func: construct the properties from the metadata of specified DOI paper
            args:
                - DOI: str
            return: None
        """
        
        # Initialize
        self.DOI = DOI.lower()
        
        # Get the Metadata(s)
        metadata = self.__get_metadata()

        # Construct Properties
        self.properties = [
            meta_parser(name, metadata)
            for name in ["Authors", "Year", "Month", "Title", "Journal", "Abstract", "DOI", "Citations"]
        ]
        self.properties = dict(self.properties)
        
        return self
    
    def send(self):

        """
            func: Send properties to Notion Database
            args: None
            returns: None
        """

        if self.DOI in self.doi2pageid.keys():  # update if the specified paper data exists
            self.__update_page_in_database()
        else:   # add if the specified paper data does not exist
            self.__add_page_to_database()

        return self

    def __init__(self):

        # Get Current Database
        self.doi2pageid = self.__get_doi2pageid()
