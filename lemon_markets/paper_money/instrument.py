from lemon_markets.helpers.api_object import ApiObject
from lemon_markets.helpers.requests import ApiRequest
from lemon_markets.account import Account
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL


class Instrument(ApiObject):

    class Values(ApiObject.Values):
        isin: str = None
        wkn: str = None
        name: str = None
        title: str = None
        symbol: str = None
        type: str = None
        currency: str = None
        tradable: bool = None
        trading_venues: list = None

    def __init__(self, data: dict):
        self._update_values(data)

    @property
    def isin(self):
        return self.Values.isin

    @property
    def wkn(self):
        return self.Values.wkn

    @property
    def name(self):
        return self.Values.name

    @property
    def title(self):
        return self.Values.title

    @property
    def symbol(self):
        return self.Values.symbol

    @property
    def type(self):
        return self.Values.type

    @property
    def currency(self):
        return self.Values.currency

    @property
    def tradable(self):
        return self.Values.tradable

    @property
    def all(self):
        return self.Values.__dict__


class ListInstruments(ApiObject):
    _url = DEFAULT_PAPER_REST_API_URL + "instruments/"
    _account: Account
    instruments: [Instrument] = []

    class BodyVariables(ApiObject.BodyVariables):
        tradable: bool
        search: str
        currency: str
        type: str
        limit: int
        offset: int

    def __init__(self, account: Account, tradable: bool = None, search: str = None, currency: str = None,
                 type: str = None, limit: int = None, offset: int = None):
        self._account = account
        self.BodyVariables.tradable = tradable
        self.BodyVariables.search = search
        self.BodyVariables.currency = currency
        self.BodyVariables.type = type
        self.BodyVariables.limit = limit
        self.BodyVariables.offset = offset

        body = self._build_body()
        #BUG: Request dont react accorting to body parms!!!
        request = ApiRequest(url=self._url, method="GET", body=body, headers=self._account.authorization)
        print(request.response) #debug purpose
        results = request.response["results"]
        for instrument in results:
            self.instruments.append(Instrument(instrument)) #BUG: Overwrites all previeues Elements with the new Element