from exceptions import AuthenticationError, AccountNotSelectedError, InvalidAccountError, InsufficientFundsError, ATMError

class BankAPI:
  def __init__(self):
    self.accounts = {}

  def validate_pin(self, card_number: str, pin: str) -> bool:
    account = self.accounts.get(card_number)
    if account and account["pin"] == pin:
      return True
    return False

  def get_balance(self, card_number: str, account_type: str) -> int:
    account = self.accounts.get(card_number)
    if account:
      balance = account["balances"].get(account_type)
      if balance is not None:
        return balance
      else:
        raise InvalidAccountError(f"Invalid account type: {account_type}.")
    raise InvalidAccountError(f"Account with card number {card_number} not found.")

  def deposit(self, card_number: str, account_type: str, amount: int) -> bool:
    account = self.accounts.get(card_number)
    if not account:
      raise InvalidAccountError(f"Account with card number {card_number} not found.")
    if account_type not in account["balances"]:
      raise InvalidAccountError(f"Invalid account type: {account_type}.")
    if amount <= 0:
      raise ATMError("Deposit amount must be positive.")
    
    account["balances"][account_type] += amount
    return True

  def withdraw(self, card_number: str, account_type: str, amount: int) -> bool:
    account = self.accounts.get(card_number)
    if not account:
      raise InvalidAccountError(f"Account with card number {card_number} not found.")
    if account_type not in account["balances"]:
      raise InvalidAccountError(f"Invalid account type: {account_type}.")
    if account["balances"][account_type] < amount:
      raise InsufficientFundsError("Insufficient funds.")
    if amount <= 0:
      raise ATMError("Withdrawal amount must be positive.")
    
    account["balances"][account_type] -= amount
    return True

  def register_account(self, card_number: str, pin: str, checking_balance: int, savings_balance: int):
    if card_number in self.accounts:
      raise InvalidAccountError("Account with this card number already exists.")
    
    self.accounts[card_number] = {
      "pin": pin,
      "balances": {
        "Checking": checking_balance,
        "Savings": savings_balance,
      }
    }
    return True
