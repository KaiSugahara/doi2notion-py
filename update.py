import sys
from bin.updater import updater, NotFoundDOI
from tqdm import tqdm

if __name__ == '__main__':
    
    # Def. updater
    ins = updater()
    
    # list of doi
    doi_list = ins.doi2pageid.keys()

    # Update any page of DOI in doi_list
    for doi in tqdm(doi_list):

        try: 
            # Set latest properties
            ins.set_properties(doi)
            # Add page to database
            ins.send()
        except NotFoundDOI:
            print(f"Skip: Updating of {doi}")
    
    print(f"Successful! [{len(doi_list)} papers]")