import BankAPI

class ATMController:
  def __init__(self, bank_API: BankAPI):
    self.bank_API = bank_API
    self.card_number = None
    self.is_authenticated = False

  def insert_card(self, card_number: str):
    self.card_number = card_number
    self.is_authenticated = False

  def enter_pin(self, pin: str) -> bool:
    if not self.card_number:
      raise Exception("No card inserted.")
    self.is_authenticated = self.bank_API.validate_pin(self.card_number, pin)
    return self.is_authenticated

  def select_account(self, account_type: str) -> bool:
    if not self.is_authenticated:
        raise Exception("Authentication required.")
    
    if account_type not in ["Checking", "Savings"]:
        raise Exception("Invalid account type selected.")
    
    self.selected_account = account_type
    balance = self.bank_API.get_balance(self.card_number, account_type)
    return balance is not None      

  def check_balance(self) -> int:
    if not self.is_authenticated:
      raise Exception("Authentication required.")
    if not self.selected_account:
      raise Exception("No account selected.")
    
    balance = self.bank_API.get_balance(self.card_number, self.selected_account)
    if balance is None:
      raise Exception("Invalid account type.")
    return balance

  def deposit(self, amount: int) -> bool:
    if not self.is_authenticated:
      raise Exception("Authentication required.")
    if not self.selected_account:
      raise Exception("No account selected.")
    
    return self.bank_API.deposit(self.card_number, self.selected_account, amount)

  def withdraw(self, amount: int) -> bool:
    if not self.is_authenticated:
      raise Exception("Authentication required.")
    if not self.selected_account:
      raise Exception("No account selected.")
    
    return self.bank_API.withdraw(self.card_number, self.selected_account, amount)

  def eject_card(self):
    self.card_number = None
    self.is_authenticated = False
    self.selected_account = None  