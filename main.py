import datetime
import pathlib
import logging

from bs4 import BeautifulSoup
import mechanize


import ods_ezodf
import python_miscelaneous.configuration as configuration

logger = logging.getLogger(__name__)


def fetch_investment_update(config):
    current_values = {"date": datetime.date.today()}
    login_url = config.get("investment_website").get("login_page_url")

    browser = mechanize.Browser()
    browser.set_handle_refresh(True)
    # Log into the website
    browser.open(login_url)
    browser.select_form(action="/en-CA/Users/Login")
    browser["Login"] = config.get("investment_website").get("username")
    browser["Password"] = config.get("investment_website").get("password")
    resp = browser.submit()
    if resp.code != 200:
        logger.warning('Cannot login to the website {}. Getting status code {} with reason {}'.format(
            login_url, resp.status_code, resp.reason))
        return

    # Get the summary page
    portfolio_link = browser.find_link(text="My Portfolio")
    if not portfolio_link:
        logger.warning('Cannot find "My Portfolio" link!')
        return
    browser.follow_link(portfolio_link)
    portfolio_url = browser.geturl()
    portfolio_soup = BeautifulSoup(browser.response().read(), features="lxml")
    accounts_config = config.get('accounts')
    for account_name in accounts_config.keys():
        if browser.geturl() != portfolio_url:
            portfolio_link = browser.find_link(text="My Portfolio")
            browser.follow_link(portfolio_link)

        value_location = accounts_config[account_name]['website_location']
        account_id = accounts_config[account_name]['account']
        if value_location == 'portfolio_url':
            # Get the value from the portfolio summary page
            account_link = portfolio_soup.find('a', text=account_id)
            # Find the row with the account in the first column
            account_row = account_link.findParent('tr')
            value_contents = account_row.findAll('td')[6].contents[0]
            value = float(value_contents.strip().replace(',',''))
        else:
            # Get the details page the account that contains the required value
            bond_name = accounts_config[account_name]['corporate_bond_name']
            account_anchor = browser.find_link(text=account_id)
            browser.follow_link(account_anchor)
            account_soup = BeautifulSoup(browser.response().read(), features="lxml")
            # Get the value from the page
            cell_element = account_soup.find('td', text=bond_name)
            cell_row = cell_element.findParent('tr')
            value_contents = cell_row.findAll('td')[8].contents[0]
            value = float(value_contents.strip().replace(',',''))

        current_values[account_name] = value

    return current_values


if __name__ == '__main__':
    config = configuration.get_configuration('investment_tracking',
                                             pathlib.Path('~/investment_tracking'),
                                             configuration.CONFIGURATION_TYPE_JSON)
    current_values = fetch_investment_update(config)
    if current_values:
        ods_ezodf.save_investment_update(config, current_values)
