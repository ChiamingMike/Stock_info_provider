

class Errors(Exception):

    def __init__(self):
        pass


class BasicInfoError(Errors):

    def __init__(self, msg):
        self.msg = msg
        return None


class FundamentalInfoError(Errors):

    def __init__(self, msg):
        self.msg = msg
        return None


class FinancialReportsError(Errors):

    def __init__(self, msg):
        self.msg = msg
        return None


class AverageDataError(Errors):

    def __init__(self, msg):
        self.msg = msg
        return None
