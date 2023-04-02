from abc import ABCMeta, abstractmethod


class Query(metaclass=ABCMeta):

    @abstractmethod
    def make_query(self):
        pass


class QueryDecorator(Query):
    def __init__(self, field, query: Query):
        self.field = field
        self.query = query
    
    def make_query(self):
        pass


class ConcreteQuery(Query):
    def __init__(self, field, term):
        self.field = field
        self.term = term
    
    def make_query(self, type_):
        body = {
            type_:{
                self.field: {
                    "query":self.term 
                }
            }
        }
        return body


class StandardAnalyzer(QueryDecorator):
    def make_query(self, type_):
        body = self.query.make_query(type_)
        body[type_][self.field]["analyzer"] = "standard"
        return body


class AndOperator(QueryDecorator):
    def make_query(self, type_):
        body = self.query.make_query(type_)
        body[type_][self.field]["operator"] = "and"
        return body


field = "name"
query = ConcreteQuery(field, "John")
query = StandardAnalyzer(field, query)
query = AndOperator(field, query)
print(query.make_query("match"))