import dataclasses
from .paper import Paper
from ..lib import crossref_attribute_parser
from ..lib.notion_property_generator import notion_property_generator
from crossref.restful import Works


class CrossRefPaper(Paper):
    def __init__(self, doi: str):
        # 論文データを取得
        response = self.__get_paper_data(doi)

        # 対象のメタ名を取得
        self.attribute_names = [field.name for field in dataclasses.fields(Paper)]

        # 論文のメタデータをセット
        self.__set_attribute(response)

    def __get_paper_data(self, doi: str) -> dict:
        response: dict | None = Works().doi(doi)
        if response is None:
            raise Exception(f"CrossRef API could not find the paper with {doi}.")
        return response

    def __set_attribute(self, response: dict):
        for attribute_name in self.attribute_names:
            setattr(
                self,
                attribute_name,
                getattr(crossref_attribute_parser, attribute_name)(response),
            )

    def get_notion_properties(self) -> dict:
        return dict(
            [
                notion_property_generator(name, value)
                for name in self.attribute_names
                if (value := getattr(self, name)) is not None
            ]
        )
