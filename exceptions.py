class ATMError(Exception):
    pass

class AuthenticationError(ATMError):
    pass

class AccountNotSelectedError(ATMError):
    pass

class InvalidAccountError(ATMError):
    pass

class InsufficientFundsError(ATMError):
    pass