import re

def meta_parser(name, metadata):

    """
        func:
            Parse the Crossref API metadata & Return a property for Notion API
        args:
            - name: property name of a notion database
            - metadata: Crossref API metadata
        returns:
            - name: property name of a notion database
            - property: property
    """

    if name == "Authors":

        # Extract Author Names
        try:
            authors = [author["given"] + " " + author["family"] for author in metadata["author"]]
        except Exception:   # Terminate if paper with unexpected data
            return False
        
        # Property
        property = {
            "type": "multi_select", 
            "multi_select": [
                {
                    "name": author,
                    "color": "gray",
                }
                for author in authors
            ]
        }
        
        return property

    if name == "Year":

        # Extract Year
        try:
            year = metadata["issued"]["date-parts"][0][0]
        except Exception:   # Terminate if paper with no data
            return False

        # Add Property
        property = {
          "type": "number",
          "number": year,
        }

        return property
    
    if name == "Month":

        # Extract Month
        try:
            month = metadata["issued"]["date-parts"][0][1]
        except Exception:   # Terminate if paper with no data
            return False

        # Add Property
        property =  {
          "type": "number",
          "number": month,
        }

        return property

    if name == "Title":

        # Extract Title
        try:
            title = metadata.get("title")[0]
        except Exception:   # Terminate if paper with no data
            return False

        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": title }
            }]
        }

        return property

    if name == "Journal":

        # Extract Journal Title
        try:
            journal = metadata.get("container-title")[0]
        except Exception:   # Terminate if paper with no data
            return False

        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": journal }
            }]
        }

        return property

    if name == "Abstract":

        # Extract Title
        abstract = metadata.get("abstract")
        
        # Terminate if paper with no title
        if abstract == None: return False

        # Remove JATS-elements
        abstract = re.sub("<(|/)jats:p>|", "", abstract)    

        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": (abstract if abstract else "") }
            }]
        }

        return property

    if name == "DOI":

        DOI = metadata.get("DOI")

        # Add Property
        property = {
            "id": "title",
            "type": "title",
            "title": [{
                "type": "text",
                "text": { "content": DOI }
            }]
        }

        return property
    
    if name == "Citations":

        # Extract Citations
        citations = metadata["is-referenced-by-count"]

        # Add Property
        property = {
          "type": "number",
          "number": citations,
        }

        return property
    
    raise Exception("Error: Unknown name is specified.")