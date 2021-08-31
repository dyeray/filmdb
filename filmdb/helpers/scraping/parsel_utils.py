from parsel import Selector


def get_node_text(selector: Selector, include_children: bool = False):
    query = '::text' if include_children else ':scope::text'
    return ''.join(selector.css(query).getall())
