from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

class Searcher:
    def __init__(self, searchterm):
        self.term = searchterm
#        self.sold = sold  # use this later?
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def query(self):
        try:
            api = Finding(appid="BillBodo-Crossroa-PRD-38dfd86bc-b5af559e", config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': self.term})
            if int(response.reply.paginationOutput.totalEntries) > 0:
                for i in response.reply.searchResult.item:
                    print i.sellingStatus.currentPrice.value
                    self.add_result(i)
            print(response.dict())
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
        return(self.results)



