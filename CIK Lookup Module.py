import requests

class SecEdgar:
    def __init__(self, fileurl): # runs automatically when you create a SecEdgar object
        self.fileurl = fileurl # stores the URL so other methods can use it
        self.name_dict = {} # empty dict: will hold title (from CIK data)
        self.ticker_dict = {} # empty dict: will hold ticker (from CIK data)
        # __init__ is Python's reserved name for "run this automatically when the object is created."
        # self refers to the specific instance of the class.
        # analogy: imagine the SecEdgar class is a cookie cutter, and each SecEdgar object you create is an individual cookie:
        # full analogy mapped out:
        #   cookie cutter = SecEdgar class (the blueprint)
        #   cookie = se (the object, the living thing in memory)
        #   recipe step = __init__ (what happens when you bake it)
        #   raw ingredients = the JSON file from SEC (external data you fetch)
        #   finished ingredients, organized = self.name_dict and self.ticker_dict (what you do with that raw data)
        #   asking the cookie something = se.name_to_cik("APPLE INC.")

        headers = {'user-agent': 'MLT MM muhsinmohamed2005@gmail.com'} # ID card we show the SEC (line 9)
        r = requests.get(self.fileurl, headers=headers) # actually fetches the JSON file

        self.filejson = r.json() # converts raw response into Python-readable JSON

        self.cik_json_to_dict() # immediately calls the method below to populate the dicts

    def cik_json_to_dict(self): # parses the JSON and fills both dictionaries
        self.name_dict = {}
        self.ticker_dict = {}
        # redundant with __init__, but resets them cleanly (intentional defensive programming)
        # If someone calls cik_json_to_dict() a second time (w/o calling the whole SecEdgar class), those lines wipe the old dictionaries clean before repopulating.
        # Without them, you'd be adding to existing data rather than replacing it, which could cause duplicates or stale entries.

        for key, value in self.filejson.items():
            self.name_dict[value['title']] = (value['cik_str'], value['title'], value['ticker'])
            self.ticker_dict[value['ticker']] = (value['cik_str'], value['title'], value['ticker'])
            # before the loop — self.filejson (raw SEC format): {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, "1": {...}}
            # to find Apple you'd have to guess the key is "0" — useless.
            # after the loop — self.name_dict (your format): {"APPLE INC.": (320193, "APPLE INC.", "AAPL"), "MICROSOFT CORP": (...), ...}
            # now you can look up any company instantly by name.
            # (same logic for self.ticker_dict).

    def name_to_cik(self, company_name):
        return self.name_dict.get(company_name)
        # company_name is just whatever string you pass in as the search term.
        # The method then uses .get() to look for that string as a key in self.name_dict, which is 'title' (synonymous with company_name).

    def ticker_to_cik(self, ticker):
        return self.ticker_dict.get(ticker)
        # (same logic as the 'name_to_cik' method).

se = SecEdgar('https://www.sec.gov/files/company_tickers.json') # creates an actual SecEdgar object using the SEC's EDGAR database (company_tickers URL)
name_lookup = se.name_to_cik("Apple Inc.")
ticker_lookup = se.ticker_to_cik("AAPL")
print(name_lookup)
print(ticker_lookup)
# signed: MM - 06/13