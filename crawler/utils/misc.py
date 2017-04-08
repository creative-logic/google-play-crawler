from contextlib import contextmanager
from w3lib.url import add_or_replace_parameter


def url_params(url, **params):
    for k, v in params.items():
        url = add_or_replace_parameter(url, k, v)
    return url


def extract_text(sel, normalize=True):
    if sel:
        text_xpath = 'normalize-space(.)' if normalize else 'string(.)'
        return sel.xpath(text_xpath).extract_first()
    return ''


def filter_url_by_domain(url):
	# Set Yelp to sort reviews by newest first
	if url.find('yelp.com'):
		url = add_or_replace_parameter(url, 'sort_by', 'date_desc')
	
	return url


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass
