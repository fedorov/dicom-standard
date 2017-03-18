'''
Convenience functions for common relations in the DICOM HTML.
Many of these relations are obscure-looking nested accesses,
but they are consistent relations across the HTML source.
'''
from typing import List

from bs4.element import PageElement

def table_rows(table_div: PageElement) -> List[PageElement]:
    return table_div.find('tbody').find_all('tr')

def table_name(table_div: PageElement) -> str:
    return table_div.p.strong.get_text()

def table_id(table_div: PageElement) -> str:
    return table_div.a.get('id')

def table_description(table_div: PageElement) -> PageElement:
    return table_div.parent.find('p')
