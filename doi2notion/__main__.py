import argparse

from tqdm import tqdm

from .interface.arxiv_paper import ArxivPaper
from .interface.crossref_paper import CrossRefPaper
from .lib.notion_manager import NotionManager

if __name__ == "__main__":
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("action", choices=["add", "update"])
    parser.add_argument("dois", nargs="*")
    args = parser.parse_args()

    # DOIを小文字に統一
    dois = [doi.lower() for doi in args.dois]

    # action = add
    if args.action == "add":
        manager = NotionManager()
        for doi in dois:
            try:
                paper = ArxivPaper(doi) if "/arxiv." in doi else CrossRefPaper(doi)
                manager.add_paper(paper)
            except Exception as e:
                print(doi, e)

    # action = update
    if args.action == "update":
        manager = NotionManager()
        for doi in tqdm(manager.doi2pageid.keys()):
            if doi.startswith("unknown/"):
                continue
            try:
                paper = ArxivPaper(doi) if "/arxiv." in doi else CrossRefPaper(doi)
                manager.update_paper(paper)
            except Exception as e:
                print(doi, e)
