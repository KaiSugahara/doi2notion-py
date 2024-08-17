import dataclasses

import arxiv

from ..lib import arxiv_attribute_parser
from ..lib.notion_property_generator import notion_property_generator
from .paper import Paper


class ArxivPaper(Paper):
    def __init__(self, doi: str):
        # 論文データを取得
        response = self.__get_paper_data(doi)

        # 対象のメタ名を取得
        self.attribute_names = [field.name for field in dataclasses.fields(Paper)]

        self.response = response
        # 論文のメタデータをセット
        self.__set_attribute(response)

    def __get_paper_data(self, doi: str) -> dict:
        arxiv_id = doi.rsplit("/", 1)[-1].replace("arxiv.", "")
        client = arxiv.Client()
        search = arxiv.Search(query=f"id:{arxiv_id}", max_results=1)
        search_results = list(client.results(search))
        if len(search_results) == 0:
            raise Exception(f"ArXiv API could not find the paper with {doi}.")
        response = search_results[0].__dict__
        response["doi"] = doi
        return response

    def __set_attribute(self, response: dict):
        for attribute_name in self.attribute_names:
            setattr(
                self,
                attribute_name,
                getattr(arxiv_attribute_parser, attribute_name)(response),
            )

    def get_notion_properties(self) -> dict:
        return dict(
            [
                notion_property_generator(name, value)
                for name in self.attribute_names
                if (value := getattr(self, name)) is not None
            ]
        )
