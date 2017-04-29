import os
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import tortilla
from tortilla import Wrap
from tortilla.wrappers import Client
import pandas as pd

from datetime import datetime
from datetime import date
from datetime import timedelta
import pytz
from pytz import timezone

HELPSCOUT_API_URL = 'https://api.helpscout.net/v1/'

class HelpscoutClient():
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get('HELPSCOUT_API_KEY')

        self.api = HelpscoutWrap('https://api.helpscout.net/v1/', extension='json')
        self.api._parent.session.mount('https://api.helpscout.net', SkipEncodeAdapter())
        self.api.config.auth = auth=HTTPBasicAuth(api_key,'pass')

    def date_range_params(end_date=datetime.now(), days_range=56, include={}, timezone=timezone('US/Pacific'), days_interval=1):
        format_dt = lambda dt: datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")
        parse_dt = lambda dt: datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
        format_d = lambda dt: datetime.strftime(dt, "%Y-%m-%d")

        pst_end = timezone.localize(end_date.replace(hour=0, minute=0, second=0, microsecond=0))
        base = pst_end.astimezone(pytz.utc) + timedelta(1)
        date_params = [{
            "start" : format_dt(base - timedelta(days=x+days_interval)),
            "end" : format_dt(base - timedelta(days=x))
        } for x in range(0, days_range, days_interval)]

        params = [{**d, **include} for d in date_params]

        return params

class HelpscoutWrap(Wrap):
    def __call__(self, *parts, **options):
        self.config.update(**options)

        if len(parts) == 0:
            return self

        parent = self
        for part in parts:
            # check if a wrap is already created for the part
            try:
                # the next part in this loop will have this wrap as
                # its parent
                parent = parent.__dict__[part]
            except KeyError:
                # create a wrap for the part
                parent.__dict__[part] = HelpscoutWrap(part=part, parent=parent)
                parent = parent.__dict__[part]

        return parent

    def __getattr__(self, part):
        try:
            return self.__dict__[part]
        except KeyError:
            self.__dict__[part] = HelpscoutWrap(part=part, parent=self,
                                       debug=self.config.get('debug'))
            return self.__dict__[part]

    def get(self, *parts, **options):
        response = self.request('get', *parts, **options)
        if 'items' in response:
            return CollectionEnvelope(response)
        elif 'item' in response:
            return response.item
        else: #assume this is a report result, return as is
            return response

class SkipEncodeAdapter(requests.adapters.HTTPAdapter):
     def request_url(self, request, proxies):
        split = request.url.split('?') # Nasty hack, not always valid.
        if len(split) > 1:
            main, querystr = split
            querystr = urllib.parse.unquote(querystr)
            querystr = urllib.parse.quote(querystr, '/&:=')
            request.url = '?'.join([main, querystr])
        return super(SkipEncodeAdapter, self).request_url(request, proxies)


class CollectionEnvelope:
    def __init__(self, envelope):
        self.page = envelope['page']
        self.pages = envelope['pages']
        self.count = envelope['count']
        self.items = pd.DataFrame(envelope['items'])


def map_params(params_list, api_wrap):
    results = []
    for p in params_list:
        r = api_wrap(params=p)
        for k,v in p.items():
            r[k] = v
        results.append(r)

    #return results
    return pd.concat(results)

def apply(api_wrap, params_list):
    results = []
    for p in params_list:
        r = api_wrap(params=p)
        for k,v in p.items():
            r[k] = v
        results.append(r)

    #return results
    return pd.concat(results)
