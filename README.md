# Linked Art CSV

Utility for generating [Linked Art](https://linked.art/) documents from `.csv` files with headers specifying data patterns as paths.

## Dependencies

```bash
pip install lxml requests rdflib rdflib-jsonld pyld loguru
```

## Quickstart

Add a row of headings to a `.csv` file where [Linked Art patterns](https://linked.art/model/index.html) are expressed as XPath-like paths. Each subsequent row of the file represents an entity. Paths may be identified with a zero-indexed integer – for example, data in the column `identified_by[1]/Identifier/content` will be written to the second occurence of the property.

```bash
python linked_art_csv.py example.csv
```

## Example

| type            | id                                       | identified_by/Name/content | identified_by/Name/language/Language/id  | identified_by/Name/language/Language/_label | subject_of/DigitalObject/access_point/DigitalObject/id             | subject_of/DigitalObject/classified_as/Type/id | subject_of/DigitalObject/classified_as/Type/_label | subject_of/DigitalObject/format |
|-----------------|------------------------------------------|----------------------------|------------------------------------------|---------------------------------------------|--------------------------------------------------------------------|------------------------------------------------|----------------------------------------------------|---------------------------------|
| HumanMadeObject | http://www.wikidata.org/entity/Q166937   | Brieflezende vrouw         | http://vocab.getty.edu/aat/300388256     | Dutch                                       | https://www.rijksmuseum.nl/nl/collectie/SK-C-251                   | http://vocab.getty.edu/aat/300264578           | Web page                                           | text/html                       |
| HumanMadeObject | http://www.wikidata.org/entity/Q3567592  | Whaam!                     | http://vocab.getty.edu/aat/300388277     | English                                     | https://www.tate.org.uk/art/artworks/lichtenstein-whaam-t00897     | http://vocab.getty.edu/aat/300264578           | Web page                                           | text/html                       |
| HumanMadeObject | http://www.wikidata.org/entity/Q16903550 | Winged Figure              | http://vocab.getty.edu/aat/300388277     | English                                     | https://barbarahepworth.org.uk/commissions/list/winged-figure.html | http://vocab.getty.edu/aat/300264578           | Web page                                           | text/html                       |

```yaml
[
  {
    "@context": "https://linked.art/ns/v1/linked-art.json",
    "id": "https://www.wikidata.org/wiki/Q3567592",
    "type": "HumanMadeObject",
    "subject_of": [
      {
        "type": "DigitalObject",
        "format": "text/html",
        "classified_as": [
          {
            "id": "http://vocab.getty.edu/aat/300264578",
            "type": "Type",
            "_label": "Web page"
          }
        ],
        "access_point": [
          {
            "id": "https://www.tate.org.uk/art/artworks/lichtenstein-whaam-t00897",
            "type": "DigitalObject"
          }
        ]
      }
    ],
    "identified_by": [
      {
        "type": "Name",
        "content": "Whaam!",
        "language": [
          {
            "type": "Language",
            "_label": "English"
          }
        ]
      }
    ]
  },
  {
    "@context": "https://linked.art/ns/v1/linked-art.json",
    "id": "http://www.wikidata.org/entity/Q16903550",
    "type": "HumanMadeObject",
    "subject_of": [
      {
        "type": "DigitalObject",
        "format": "text/html",
        "classified_as": [
          {
            "id": "http://vocab.getty.edu/aat/300264578",
            "type": "Type",
            "_label": "Web page"
          }
        ],
        "access_point": [
          {
            "id": "https://barbarahepworth.org.uk/commissions/list/winged-figure.html",
            "type": "DigitalObject"
          }
        ]
      }
    ],
    "identified_by": [
      {
        "type": "Name",
        "content": "Winged Figure",
        "language": [
          {
            "type": "Language",
            "_label": "English"
          }
        ]
      }
    ]
  },
  {
    "@context": "https://linked.art/ns/v1/linked-art.json",
    "id": "http://www.wikidata.org/entity/Q166937",
    "type": "HumanMadeObject",
    "subject_of": [
      {
        "type": "DigitalObject",
        "format": "text/html",
        "classified_as": [
          {
            "id": "http://vocab.getty.edu/aat/300264578",
            "type": "Type",
            "_label": "Web page"
          }
        ],
        "access_point": [
          {
            "id": "https://www.rijksmuseum.nl/nl/collectie/SK-C-251",
            "type": "DigitalObject"
          }
        ]
      }
    ],
    "identified_by": [
      {
        "type": "Name",
        "content": "Brieflezende vrouw",
        "language": [
          {
            "type": "Language",
            "_label": "Dutch"
          }
        ]
      }
    ]
  }
]
```
