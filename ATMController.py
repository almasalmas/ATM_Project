import logging
from BankAPI import BankAPI
from exceptions import AuthenticationError, AccountNotSelectedError, InvalidAccountError, InsufficientFundsError

class ATMController:
  def __init__(self, bank_api: BankAPI):
    self.bank_api = bank_api
    self.card_number = None
    self.is_authenticated = False
    self.selected_account = None
    self._setup_logger()

  def _setup_logger(self):
    self.logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)

  def _check_authentication(self):
    if not self.is_authenticated:
      self.logger.error("Authentication required.")
      raise AuthenticationError("Authentication required.")

  def _check_account_selected(self):
    if not self.selected_account:
      self.logger.error("No account selected.")
      raise AccountNotSelectedError("No account selected.")

  def insert_card(self, card_number: str):
    self.card_number = card_number
    self.is_authenticated = False
    self.selected_account = None
    self.logger.info(f"Card {card_number} inserted.")

  def enter_pin(self, pin: str) -> bool:
    if not self.card_number:
      self.logger.error("No card inserted.")
      raise AuthenticationError("No card inserted.")
  
    self.is_authenticated = self.bank_api.validate_pin(self.card_number, pin)
    if self.is_authenticated:
      self.logger.info(f"PIN entered successfully for card {self.card_number}.")
    else:
      self.logger.error(f"Invalid PIN for card {self.card_number}.")
    return self.is_authenticated

  def select_account(self, account_type: str) -> bool:
    self._check_authentication()

    if account_type not in ["Checking", "Savings"]:
      self.logger.error(f"Invalid account type: {account_type}.")
      raise InvalidAccountError("Invalid account type selected.")
    
    self.selected_account = account_type
    balance = self.bank_api.get_balance(self.card_number, account_type)
    if balance is None:
      self.logger.error(f"Failed to retrieve balance for {account_type} account.")
      raise InvalidAccountError("Failed to retrieve account balance.")
    
    self.logger.info(f"Account selected: {account_type}.")
    return True

  def check_balance(self) -> int:
    self._check_authentication()
    self._check_account_selected()
    
    balance = self.bank_api.get_balance(self.card_number, self.selected_account)
    if balance is None:
      self.logger.error("Failed to retrieve balance.")
      raise InvalidAccountError("Invalid account type or balance unavailable.")
    
    self.logger.info(f"Balance checked for {self.selected_account}: {balance}.")
    return balance

  def deposit(self, amount: int) -> bool:
    self._check_authentication()
    self._check_account_selected()

    if amount <= 0:
      self.logger.error(f"Invalid deposit amount: {amount}. Must be positive.")
      return False
    
    success = self.bank_api.deposit(self.card_number, self.selected_account, amount)
    if success:
      self.logger.info(f"Deposited {amount} to {self.selected_account}.")
    else:
      self.logger.error(f"Failed to deposit {amount} to {self.selected_account}.")
    return success

  def withdraw(self, amount: int) -> bool:
    self._check_authentication()
    self._check_account_selected()

    if amount <= 0:
      self.logger.error(f"Invalid withdrawal amount: {amount}. Must be positive.")
      return False

    balance = self.bank_api.get_balance(self.card_number, self.selected_account)
    if balance is None or balance < amount:
      self.logger.error(f"Insufficient funds for withdrawal. Balance: {balance}, Withdrawal amount: {amount}.")
      return False
    
    success = self.bank_api.withdraw(self.card_number, self.selected_account, amount)
    if success:
        self.logger.info(f"Withdrew {amount} from {self.selected_account}.")
    else:
        self.logger.error(f"Failed to withdraw {amount} from {self.selected_account}.")
    return success

  def eject_card(self):
    self.card_number = None
    self.is_authenticated = False
    self.selected_account = None
    self.logger.info("Card ejected.")
