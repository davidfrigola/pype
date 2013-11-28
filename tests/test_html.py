from pype.html import *


def init_ok_test():
    ## No valid (cause no invalid) config
    pass

def init_ko_test():
    ## No invalid config found
    pass

def parse_html_from_text_test():

    html_text = "<html><head><title>title</title></head><body><p class='pclass'> my text </p></html>"
    item = BaseItem(None)
    item.setValue(html_text)
    processor = HtmlProcessor({FROM_TEXT:True,"find":{"p":{"class":"pclass"}}})

    result = processor.process(item)
    print result
    assert len(result) == 1

