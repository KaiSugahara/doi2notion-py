def notion_property_generator(prop_name: str, value: any) -> tuple[str, dict]:
    if prop_name == "authors":
        return (
            "Authors",
            {
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": author,
                        "color": "gray",
                    }
                    for author in value
                ],
            },
        )

    if prop_name == "year":
        return (
            "Year",
            {
                "type": "number",
                "number": value,
            },
        )

    if prop_name == "month":
        return (
            "Month",
            {
                "type": "number",
                "number": value,
            },
        )

    if prop_name == "title":
        return (
            "Title",
            {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": value}}],
            },
        )

    if prop_name == "journal":
        return (
            "Journal",
            {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": value}}],
            },
        )

    if prop_name == "abstract":
        return (
            "Abstract",
            {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": value}}],
            },
        )

    if prop_name == "doi":
        return (
            "DOI",
            {
                "id": "title",
                "type": "title",
                "title": [{"type": "text", "text": {"content": value}}],
            },
        )

    if prop_name == "citations":
        return (
            "Citations",
            {
                "type": "number",
                "number": value,
            },
        )

    raise Exception("Error: 存在しないプロパティ名が指定されています。")
