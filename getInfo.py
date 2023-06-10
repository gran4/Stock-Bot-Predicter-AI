import urllib.request
from bs4 import BeautifulSoup
import ssl

from typing import Optional, List
from datetime import datetime
import json

company_symbols = ["APPL"]


def get_earnings_history(company_ticker: str, context: Optional[ssl.SSLContext] = None) -> List[List[str]]:
    """
    Gets earning history of a company as a list.

    Args:
        company_ticker str: company to get info of
        context Optional[ssl certificate]: ssl certificate to use

    Warning:
        IF YOU GET ERROR:
            urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1002)>
        Go to Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file. :D
        NOTE: ON macOS go to Macintosh HD > Applications > Python3.6(or whatever version of python you're using) > double click on "Install Certificates.command" file. :D

    Warning:
        YOU are probibly looking to use get_corrected_earnings_history not this

    Returns:
        List: of [Date, Actual EPS, Estimated EPS]
    """
    url = f"https://finance.yahoo.com/quote/{company_ticker}/history?p={company_ticker}"

    # Send a GET request to the URL with certificate verification
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, context=context)
    html_content = response.read().decode('utf-8')

    # Create a Beautiful Soup object for parsing
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table containing earnings history
    table = soup.find('table', {'data-test': 'historical-prices'})
    rows = table.find_all('tr')

    earnings_history = []
    for row in rows[1:]:
        columns = row.find_all('td')
        if len(columns) == 7:
            date = columns[0].text
            actual_eps = columns[4].text
            estimated_eps = columns[6].text
            #list so info can be added
            earnings_history.append([date, actual_eps, estimated_eps])

    return earnings_history


def date_time_since_ref(date_string: str, reference_date: datetime) -> int:
    """
    Returns the number of days between the given date and the reference date.

    Args:
        date_string str: date to use
        reference_date datetime: date to compare with

    Returns:
        int: The number of days between the given date and the reference date.
    """
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_string, "%b %d, %Y")

    # Calculate the number of days between the date and the reference date
    delta = date_object - reference_date
    days_since_ref = delta.days

    return days_since_ref


if __name__ == '__main__':
    start_date = '2010-01-01'
    end_date = '2023-05-16'

    date_object = datetime.strptime(start_date, "%Y-%m-%d")
    # Convert the datetime object back to a string in the desired format
    converted_date = date_object.strftime("%b %d, %Y")
    reference_date = datetime.strptime(converted_date, "%b %d, %Y")


    # Example usage
    for company_ticker in company_symbols:
        earnings_history = get_earnings_history(company_ticker)
        for earnings in earnings_history:
            date, actual_eps, estimated_eps = earnings
            time_since = date_time_since_ref(date, reference_date) 

            reference_date = datetime.strptime(date, "%b %d, %Y")
            earnings.append(time_since)

        with open(f"{company_ticker}/info.json", "w") as json_file:
            print(earnings_history, company_ticker)
            json.dump(earnings_history, json_file)

