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
        authors = [author["given"] + " " + author["family"] for author in metadata["author"]]
        
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
        
        return name, property

    if name == "Year":

        # Extract Year/Month
        year, month = metadata["issued"]["date-parts"][0][:2]

        # Add Property
        property = {
          "type": "number",
          "number": year
        }

        return name, property
    
    if name == "Month":

        # Extract Year/Month
        year, month = metadata["issued"]["date-parts"][0][:2]

        # Add Property
        property =  {
          "type": "number",
          "number": month,
        }

        return name, property

    if name == "Title":

        # Extract Title
        title = metadata.get("title")[0]

        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": title }
            }]
        }

        return name, property

    if name == "Journal":

        # Extract Title
        journal = metadata.get("container-title")[0]

        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": journal }
            }]
        }

        return name, property

    if name == "Abstract":

        # Extract Title
        abstract = metadata.get("abstract")
        abstract = abstract if abstract else ""
        abstract = re.sub("<(|/)jats:p>|", "", abstract)    # Remove JATS-elements


        # Add Property
        property = {
            'type': 'rich_text',
            'rich_text': [{
                "type": "text",
                "text": { "content": (abstract if abstract else "") }
            }]
        }

        return name, property

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

        return name, property
    
    if name == "Citations":

        # Extract Citations
        citations = metadata["is-referenced-by-count"]

        # Add Property
        property = {
          "type": "number",
          "number": citations,
        }

        return name, property
    
    raise Exception("Error: Unknown name is specified.")