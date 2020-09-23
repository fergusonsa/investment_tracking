# investment_tracking

A simple script to get investment values by webscraping from investment firm website after login, and updates an OpenDocument (.ods) spreadsheet with the details. 

Website and account details are stored in a json file, ~/investment_tracking/investment_tracking.json, that is not part of the repository and looks like this : 

{
    "investment_website": {
        "username": "my_username",
        "password": "qwerty1234",
        "login_page_url": "https://client.investmentcompany.com/"
    },
    "accounts": {
        "RRSP": {
            "name": "RRSP",
            "account": "100-ABFD-0",
            "column": "B",
            "website_location": "portfolio_url"
            },
        "TFSA":  {
            "name": "TFSA",
            "account": "100-ABSF-0",
            "column": "C",
            "website_location": "portfolio_url"
            },
        "Cash ACCOUNT":  {
            "name": "Cash",
            "account": "100-DEFG-0",
            "column": "D",
            "website_location": "portfolio_url"
            },
        "Bond 1":  {
            "name": "Bond 1",
            "account": "100-ABCD-0",
            "corporate_bond_name": "BOND COMPANY GIC 2.4% 09DEC20R",
            "column": "O",
            "website_location": "custom"
            }
    },
    "spreadsheet": {
        "path" : "C:\\python\\investment_tracking\\InvestmentTracking_test.ods",
        "sheet_name": "2020",
        "date_column": "A",
        "total_column": "H"
    }    
}


NOTE that the ezods module cannot recalculate formulas, so after opening the spreadsheet, you must select the sheet and press F9 to recalculate any formulas.
