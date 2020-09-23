import datetime
import pathlib
import logging

import requests
from bs4 import BeautifulSoup as bs
import mechanicalsoup
import mechanize


import ods_ezodf
import python_miscelaneous.configuration as configuration

logger = logging.getLogger(__name__)


def fetch_investment_update(config):
    current_values = {"date": datetime.date.today()}
    login_url = config.get("investment_website").get("login_page_url")
    login_post_url = config.get("investment_website").get("login_url")
    username = config.get("investment_website").get("username")
    password = config.get("investment_website").get("password")

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )
    # Log into the website
    browser.open(login_url)
    browser.select_form('#login-form')
    browser["Login"] = username
    browser["Password"] = password
    resp = browser.submit_selected()
    if resp.status_code != 200:
        logger.warning('Cannot login to the website {}. Getting status code {} with reason {}'.format(
            login_url, resp.status_code, resp.reason))
        return
    home_page = browser.get_current_page()

    # Get the summary page
    portfolio_links = browser.links(link_text="My Portfolio")
    if not portfolio_links:
        logger.warning('Cannot find "My Portfolio" link!')
        return
    browser.follow_link(portfolio_links[0])
    portfolio_page = browser.get_current_page()
    portfolio_url = browser.get_url()
    meta = portfolio_page.find('meta', content=True)
    browser.get(meta)
    accounts_config = config.get('accounts')
    for account_name in accounts_config.keys():
        if browser.get_url() != portfolio_url:
            portfolio_link = browser.find_link('a', string="MY PORTFOLIO")
            browser.follow_link(portfolio_link)

        value_location = accounts_config[account_name]['website_location']
        account_id = accounts_config[account_name]['account']
        account_anchor = browser.find('a', string=account_id)
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
