# helpscout_api

A simple Python interface to [Helpscout API][helpscout-api].

## Requirements

Python 3.5+

For development: Docker

## Installation

You can use `pip` to install helpscout_api

```bash
pip install git+https://github.com/bufferapp/helpscout_api
```

If you prefer, you can clone it and run the setup.py file. Use the following
commands to install helpscout_api from Github:

```bash
git clone https://github.com/bufferapp/helpscout_api
cd helpscout_api
python setup.py install
```

## Basic Usage

To use helpscout_api, you need your Helpscout API key.

Log in to Helpscout, go to 'Your Profile' > 'API keys'

Click on 'Generate an API Key' or copy the value of an existing one.

If you set the following environment variable, that package will use that key to authenticate:

```
HELPSCOUT_API_KEY=key_value
```

To get access to an instance of the Helpscout api, use the connect method

```
from helpscout.
helpscout = client.connect()
```

```python
from helpscout_api import HelpscoutClient

helpscout = HelpscoutClient()
#or you can pass an explicit api key
helpscout = HelpscoutClient(api_key='your-api-key')
```

Now you can start calling the Helpscout API :D

Find the docs here: http://developer.helpscout.net/help-desk-api/

The client is implemented in tortilla, so you should be able to convert the endpoint url to a Python call pretty easily

```python
#https://api.helpscout.net/v1/mailboxes.json
envelope = api.mailboxes.get()
```

## Api Results
The Helpscout API has different kinds of [result envelopes](http://developer.helpscout.net/help-desk-api/#response-envelopes).

Single item envelope calls will just return the item directly

```python
helpscout = HelpscoutClient()

mailbox = helpscout.api.mailboxes(1234).get()
print(mailbox.name)
```

Collections envelope calls will return a `CollectionEnvelope` object. The `items` property is a pandas dataframe

```python
helpscout = HelpscoutClient()
result = helpscout.api.mailboxes().get()

print(result.count)
print(result.page)
print(result.pages)

result.items.head() #pandas dataframe
```

Results are limited to 50 items per page. To get another page, use the `page` parameter

```python
helpscout = HelpscoutClient()
result = helpscout.api.mailboxes().get(params={'page':2})
```

Report api calls are returned as is:

```python
from helpscout_api import format_dt

start = format_dt(datetime(2017,1,1))
end = format_dt(datetime(2017,1,2))
params = {'start':start, 'end':end}
report = helpscout.api.reports.conversations().get(params=params)

print(report.busiestDay) #access report fields directly
```

## Development

The development environment uses Docker. To get it set up just run:

```bash
make build
make test #to run the unit tests
make dev #command line access to the bash env
```

[helpscout-api]:http://developer.helpscout.net/help-desk-api/
