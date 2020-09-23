import datetime
import pathlib
import logging

import requests
from bs4 import BeautifulSoup as bs

import ods_ezodf
import python_miscelaneous.configuration as configuration

logger = logging.getLogger(__name__)


def fetch_investment_update(config):
    current_values = {"date": datetime.date.today()}
    login_url = config.get("investment_website").get("login_page_url")
    login_post_url = config.get("investment_website").get("login_url")
    username = config.get("investment_website").get("username")
    password = config.get("investment_website").get("password")

    # Log into the website
    # Using example https://linuxhint.com/logging_into_websites_python/
    with requests.Session() as session:
        # Get the login page
        login_page_res = session.get(login_url, verify=False)
        # Get the _RequestVerificationToken hidden field value
        login_page_content = bs(login_page_res.content, "html.parser")
        token = login_page_content.find("input", {"name": "_RequestVerificationToken"})

        login_data = {'Login': username,
                      'Password': password,
                      'RememberLogin': False,
                      '_RequestVerificationToken': token}
        res = session.post(login_post_url, data=login_data, headers=dict(referer=login_url))
        if res.status_code != 200:
            logger.warning('Cannot login to the website {}. Getting status code {} with reason {}'.format(
                login_post_url, res.status_code, res.reason))
            return
        home_page = bs(res.content, "html.parser")
        # Get the summary page
        portfolio_url = config["investment_website"]["portfolio_url"]
        res = session.get(portfolio_url)
        portfolio_content = bs(res.content, "html.parser")

        accounts_config = config.get('accounts')
        for account_name in accounts_config.keys():
            value_location = accounts_config[account_name]['website_location']
            account_id = accounts_config[account_name]['account']
            account_anchor = portfolio_content.find('a', string=account_id)
            if value_location == 'portfolio_url':
                # Get the value from the portfolio summary page
                # Find the row with the account in the first column
                row = account_anchor.findParent('tr')

                value = 10000.00
            else:
                # Get the details page the account that contains the required value
                # Find the row with the account in the first column
                # Get the value from the page
                value = 1111.11
            current_values[account_name] = value

    return current_values


if __name__ == '__main__':
    config = configuration.get_configuration('investment_tracking',
                                             pathlib.Path('~/investment_tracking'),
                                             configuration.CONFIGURATION_TYPE_JSON)
    current_values = fetch_investment_update(config)
    import pprint
    pprint.pprint(current_values)
    # if current_values:
    #     ods_ezodf.save_investment_update(config, current_values)
