class BankAPI:
  def __init__(self):
    self.accounts = {}  

  def validate_pin(self, card_number: str, pin: str) -> bool:
    account = self.accounts.get(card_number)
    return account and account["pin"] == pin

  def get_balance(self, card_number: str, account_type: str) -> int:
    account = self.accounts.get(card_number)
    if account:
      balance = account["balances"].get(account_type)
      return balance
    return None

  def deposit(self, card_number: str, account_type: str, amount: int) -> bool:
    account = self.accounts.get(card_number)
    if account and account_type in account["balances"]:
      account["balances"][account_type] += amount
      return True
    return False

  def withdraw(self, card_number: str, account_type: str, amount: int) -> bool:
    account = self.accounts.get(card_number)
    if account and account_type in account["balances"] and account["balances"][account_type] >= amount:
      account["balances"][account_type] -= amount
      return True
    return False

  def register_account(self, card_number: str, pin: str, checking_balance: int, savings_balance: int):
    if card_number in self.accounts:
      raise Exception("Account with this card number already exists.")
    self.accounts[card_number] = {
      "pin": pin,
      "balances": {
        "Checking": checking_balance,
        "Savings": savings_balance,
      }
    }
    return True