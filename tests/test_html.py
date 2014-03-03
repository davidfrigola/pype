from pype.model import BaseItem
from pype.html import HtmlProcessor, FROM_TEXT, RandomUserAgentHeaderProvider,\
    RANDOM_USER_AGENT_FILE, FixHeaderProvider, MultipleHeaderProvider,\
    HEADER_PROVIDERS_LIST, FIX_HEADER, DefaultUserAgentHeaderProvider,\
    USER_AGENT_HEADER


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


def parse_html_error_test():

    html_text = "<bad format></test>"
    item = BaseItem(None,html_text)

    processor = HtmlProcessor({FROM_TEXT:True,"find":{"p":{"class":"pclass"}}})

    result = processor.process(item)

    assert result == []

def randomuseragentheaderprovider_ok_test():

    provider = RandomUserAgentHeaderProvider({RANDOM_USER_AGENT_FILE:"./tests/resources/useragents.txt"})

    result = provider.getHeaders()

    assert result is not None

def fixheaderprovider_noconfig_test():

    provider = FixHeaderProvider(None)

    result = provider.getHeaders()

    assert len(result)==0

def multiheadersprovider_ok_test():

    provider = MultipleHeaderProvider({HEADER_PROVIDERS_LIST:[FixHeaderProvider({FIX_HEADER:{"h1":"vh1"}}),
                                                            FixHeaderProvider({FIX_HEADER:{"h2":"vh2"}})]})

    result = provider.getHeaders()

    assert result is not None
    assert len(result) == 2

def multiheadersprovider_nolist_test():

    provider = MultipleHeaderProvider(None)

    result = provider.getHeaders()

    assert len(result) == 0

def defaultuseragentheaderprovider_ok_test():

    provider = DefaultUserAgentHeaderProvider(None)

    result = provider.getHeaders()

    assert len(result)==1
    assert "User-Agent" in result

    provider = DefaultUserAgentHeaderProvider({USER_AGENT_HEADER:"testuseragent"})

    result = provider.getHeaders()

    assert len(result)==1
    assert result["User-Agent"] == "testuseragent"