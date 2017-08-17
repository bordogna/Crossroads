from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

cfg = dict(user='bill', password='gojets', host='localhost', database='comicbooks', raise_on_warnings=True)

class SearchResults:
    def __init__(self, searchterm, numresults):
        self.term = searchterm
        self.num = numresults
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def query(self):
        try:
            api = Finding(appid="BillBodo-Crossroa-PRD-38dfd86bc-b5af559e", config_file=None)
            response = api.execute('findCompletedItems',
                                   {'keywords': self.term,
                                    'categoryId' : ['63'],
                                    'paginationInput': {
                                        'entriesPerPage': self.num,
                                        'pageNumber': '1'
                                    },
                                    })
            if int(response.reply.paginationOutput.totalEntries) > 0:
                for i in response.reply.searchResult.item:
                    print (i.sellingStatus.currentPrice.value)
                    self.add_result(i)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
        return(self.results)

