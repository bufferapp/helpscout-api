import os
from datetime import datetime
from helpscout_api import format_dt
from helpscout_api.client import HelpscoutClient

def test_auth_with_env_var():
    #This test assumes you've got a env variable called HELPSCOUT_API_KEY set, that is a valid key
    helpscout = HelpscoutClient()
    helpscout.api.mailboxes().get() #should not raise an error

def test_auth_with_explicit_key():
    #This test assumes you've got a env variable called HELPSCOUT_API_KEY set, that is a valid key
    api_key = os.environ.pop('HELPSCOUT_API_KEY')
    helpscout = HelpscoutClient(api_key=api_key)
    helpscout.api.mailboxes().get() #should not raise an error
    os.environ['HELPSCOUT_API_KEY'] = api_key

def test_collection_result_call():
    helpscout = HelpscoutClient()
    result = helpscout.api.mailboxes().get() #should not raise an error

    assert result.count > 0
    assert result.page == 1
    assert result.pages > 0

    # The items property is a pandas dataframe
    assert len(result.items) > 0
    assert 'createdAt' in result.items.columns
    assert 'id' in result.items.columns
    assert 'name' in result.items.columns

def test_single_result_call():
    helpscout = HelpscoutClient()
    result = helpscout.api.mailboxes().get() #should not raise an error

    mailbox_id = result.items['id'][0]

    mailbox = helpscout.api.mailboxes(mailbox_id).get()

    assert mailbox.id == mailbox_id


def test_report_result():
    helpscout = HelpscoutClient()

    start = format_dt(datetime(2017,1,1))
    end = format_dt(datetime(2017,1,2))

    report = helpscout.api.reports.conversations().get(params={'start':start, 'end':end})

    assert 'busiestDay' in report
