'''
Serialise a `.csv` file to Linked Art JSON-LD.
'''


import argparse
import csv
import json
import requests
from lxml import etree
from pathlib import Path
from pyld import jsonld
from pyld.jsonld import set_document_loader
from rdflib import ConjunctiveGraph


class Document(object):
    '''
    Create a tree with XPath expressions which can be serialised to Linked Art JSON-LD.
    '''

    def __init__(self, root):
        self.root = etree.Element(root)

    def __repr__(self):
        return etree.tostring(self.root, pretty_print=True).decode('utf-8')

    def build_xpath(self, node, path):
        '''
        Create elements specified by path.
        See <https://stackoverflow.com/a/5664332>
        '''
        components = path.split('/')
        if components[0] == node.tag:
            components.pop(0)
        while components:
            # take in account positional  indexes in the form /path/para[3] or /path/para[location()=3]
            if '[' in components[0]:
                component, trail = components[0].split('[', 1)
                target_index = int(trail.split('=')[-1].strip(']'))
            else:
                component = components[0]
                target_index = 0
            components.pop(0)
            found_index = -1
            for child in node.getchildren():
                if child.tag == component:
                    found_index += 1
                    if found_index == target_index:
                        node = child
                        break
            else:
                for i in range(target_index - found_index):
                    new_node = etree.Element(component)
                    node.append(new_node)
                node = new_node

    def update(self, exp, value):
        '''
        Create a path of elements and set a value.
        '''
        # Create elements.
        self.build_xpath(self.root, exp)
        # Increment position index keys.
        new = list()
        for char in str(exp):
            try:
                i = int(char)
                i += 1
                new.append(str(i))
            except:
                new.append(char)
        exp = ''.join(new)
        # Set value.
        element = self.root.xpath(exp)[0]
        element.text = value

    def serialise(self):
        '''
        Create a Linked Art JSON-LD object.
        '''
        # RDF-ise with template
        here = Path(__file__).parent
        xslt = etree.parse(f'{here}/rdf.xslt')
        template = etree.XSLT(xslt)
        rdf_xml = template(self.root)
        # Parse RDF.
        graph = ConjunctiveGraph()
        graph.parse(data=rdf_xml, format='xml')
        # Serialise to expanded JSON-LD.
        js_str = graph.serialize(format='json-ld').decode('utf-8')
        js = json.loads(js_str)
        for i in js:
            i['@context'] = 'https://linked.art/ns/v1/linked-art.json'
        # Frame and compact the JSON-LD.
        frame = {'@id': self.record, '@embed': '@always'}
        framed = jsonld.frame(js, frame)
        compacted = jsonld.compact(framed, 'https://linked.art/ns/v1/linked-art.json')
        return compacted


def load_document_and_cache(*args):
    doc = {
        'contextUrl': None,
        'documentUrl': None,
        'document': context
    }
    return doc


# Cache the Linked Art context JSON.
response = requests.get('https://linked.art/ns/v1/linked-art.json')
context = response.json()
set_document_loader(load_document_and_cache)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    objects = list()
    # Iterate CSV rows, creating a Linked Art document for each.
    rows = csv.reader(args.file)
    headers = next(rows)
    # Require `type`
    if 'type' and 'id' not in headers:
        raise Exception('Data must have `id` and `type` columns.')
    for row in rows:
        # Initialise document with base object class.
        for exp, value in zip(headers, row):
            if exp == 'type':
                doc = Document(value)
                break
        # Extend base object with data.
        for exp, value in zip(headers, row):
            if exp == 'type':
                continue
            doc.update(exp, value)
            if exp == 'id':
                doc.record = value
        linked_art_json = doc.serialise()
        objects.append(linked_art_json)

    # Serialise everything to string.
    print(json.dumps(objects, indent=2, ensure_ascii=False))
