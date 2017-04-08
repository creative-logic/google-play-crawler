import collections
import json
import logging
import sys

import requests
import six
from retrying import retry


logger = logging.getLogger(__name__)


@retry(wait_exponential_multiplier=4000, stop_max_attempt_number=3)
def select_result(target, compare_targets, city_match=False):
    """Return the index in compare_targets for the item
    that best matches the given target.
    Return None if none matches.

    The spider input can also be given in place of target,
    for the common case of searching by business name and address.
    """
    if 'address' in target and 'business_name' in target:
        target = dict(name=target['business_name'], text=text_address(target))

    from reviews_crawler.settings import MATCH_SERVICE_URL
    if compare_targets:
        params = dict(
            target=target,
            compare_targets=compare_targets,
            winner=False,
        )
        if city_match:
            params['city_match'] = True
        logger.debug('Calling match service: %s' % json.dumps(params))
        try:
            resp = requests.post(MATCH_SERVICE_URL, json=params)
            resp.raise_for_status()
        except Exception as e:
            msg = 'Match service failed! URL: {} Error: {}'.format(MATCH_SERVICE_URL, e)
            logger.error(msg)
            exc_type, _, exc_tb = sys.exc_info()
            six.reraise(exc_type, exc_type(msg), exc_tb)
        result = resp.json()
        logger.debug('Match service result: %s' % resp.text)
        winner = result['winner']
        if not isinstance(winner, bool):
            return winner


def nested_dict_value(d, path):
    if isinstance(path, basestring):
        path = path.split('.')
    value = d
    for k in path:
        if not isinstance(value, collections.Mapping):
            raise TypeError('Could not get key {} from {} for {} and path {}'
                            .format(k, value, d, path))
        elif k in value:
            value = value[k]
        else:
            raise KeyError('Key {} could not be found for nested path {} in {}'
                           .format(k, path, d))
    return value


_DEFAULT_SEARCH_INPUT_FIELDS = (
    'business_name',
    'address.street',
    'address.city',
    'address.state',
    'address.zip',
)


def text_address(place, include_number=True, include_zip=True, include_street=True, filter_street=False):
    address = place['address'] or {}
    if include_number:
        house_number = address.get('house_number') or u''
        street_address = (house_number + u' ') if house_number else u''
    else:
        street_address = ''

    if include_street:
    	if include_number:
        	street_address += address.get('street') or u''
        else:
        	street_address += ' '.join(address.get('street').split()[1:]) if address.get('street') and len(address.get('street').split()) > 1 else address.get('street') or u''
        
        if filter_street:
        	street_address = filter_street_address(street_address)
    
    state_and_zip = address.get('state') or u''
    if include_zip:
        state_and_zip += (u' ' + (address.get('zip') or u''))

    address_components = filter(None, [
        street_address,
        address.get('city'),
        state_and_zip.strip(),
    ])
    return ', '.join(address_components)


def full_address(place, **kwargs):
    return u'{}, {}'.format(place['business_name'], text_address(place, **kwargs))


def create_search_query(place, normalize=None, fields=None):
    components = fields or _DEFAULT_SEARCH_INPUT_FIELDS
    search_components = [nested_dict_value(place, path) for path in components]
    if normalize:
        search_components = [normalize(s) for s in search_components]
    search_components = filter(None, search_components)
    return ', '.join(search_components)

def filter_street_address(street):
	from reviews_crawler.settings import ADDRESS_PARSE_URL
	
	acceptable_types = ['AddressNumber',
	'AddressNumberPrefix',
	'AddressNumberSuffix',
	'StreetName',
	'StreetNamePreDirectional',
	'StreetNamePreModifier',
	'StreetNamePreType',
	'StreetNamePostDirectional',
	'StreetNamePostModifier',
	'StreetNamePostType']
	
	params = dict(
	    address=street
	)
	
	try:
		logger.debug('Checking this street for search: %s' % street)
		# Only execute if specific characters found
		if('#' in street and (street.index('#') > (len(street) / 2)) or ('Sp. ' in street and street.index('Sp. ') > (len(street) / 2)) or ('Unit ' in street and street.index('Unit ') > (len(street) / 2))):
		    resp = requests.post(ADDRESS_PARSE_URL, json=params)
		    resp.raise_for_status()
		    result = resp.json()
		    if result and 'result' in result:
		    	_street = []
		    	for element in result['result']:
		    		if element[1] in acceptable_types:
		    			_street.append(element[0].replace(",","").replace("-",""))
		    	if len(_street) > 0:
		    		street = ' '.join(_street)
		logger.debug('Returned street is %s' % street)
	except Exception as e:
	    msg = 'Address parse service failed! URL: {} Error: {}'.format('http://localhost:5001', e)
	    logger.error(msg)
	
	return street;