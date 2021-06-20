# Linked Art CSV

Draft.

Utility for generating [Linked Art](https://linked.art/) JSON-LD documents from `.csv` files, by specifying data patterns as XPath-like paths.

## Quickstart

Add a row of headings to a `.csv` file where [Linked Art patterns](https://linked.art/model/index.html) are expressed as paths. Each subsequent row of the file represents an entity. Paths may be identified with a zero-indexed integer. For example, data in the column `identified_by[1]/Identifier/content` will be written to the second occurence of the property.

```bash
pip install lxml requests rdflib rdflib-jsonld pyld
python linked_art_csv.py /path/to/file.csv
```

## Example

| type            | id                                      | identified_by/Name/content | identified_by/Name/langauge/Language/id  | identified_by/Name/language/Language/_label |
|-----------------|-----------------------------------------|----------------------------|------------------------------------------|---------------------------------------------|
| HumanMadeObject | http://www.wikidata.org/entity/Q166937  | De brieflezende vrouw      | http://vocab.getty.edu/aat/300388256     | Dutch                                       |
| HumanMadeObject | http://www.wikidata.org/entity/Q3567592 | Whaam!                     | http://vocab.getty.edu/aat/300388277     | English                                     |


```json
[
  {
    "@context": "https://linked.art/ns/v1/linked-art.json",
    "id": "http://www.wikidata.org/entity/Q166937",
    "type": "HumanMadeObject",
    "identified_by": [
      {
        "type": "Name",
        "content": "De brieflezende vrouw",
        "language": [
          {
            "id": "http://vocab.getty.edu/aat/300388256",
            "type": "Language",
            "_label": "Dutch"
          }
        ]
      }
    ]
  },
  {
    "@context": "https://linked.art/ns/v1/linked-art.json",
    "id": "http://www.wikidata.org/entity/Q3567592",
    "type": "HumanMadeObject",
    "identified_by": [
      {
        "type": "Name",
        "content": "Whaam!",
        "language": [
          {
            "id": "http://vocab.getty.edu/aat/300388277",
            "type": "Language",
            "_label": "English"
          }
        ]
      }
    ]
  }
]
```
