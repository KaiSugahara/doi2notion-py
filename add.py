import sys
from bin.updater import updater

if __name__ == '__main__':
    
    # Get DOI(s)
    doi_list = sys.argv.copy()
    doi_list.pop(0)

    # Check Augments
    if len(doi_list) == 0:
        raise Exception("Error: Arguments is empty")
    
    # Def. updater
    ins = updater()
    
    # Add/update any page of DOI in doi_list
    for doi in doi_list:
        
        # Set latest properties
        ins.set_properties(doi)
        # Add page to database
        ins.send()
    
    print(f"Successful! [{len(doi_list)} papers]")