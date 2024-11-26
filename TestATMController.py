import unittest
from BankAPI import BankAPI
from ATMController import ATMController
from exceptions import AuthenticationError, AccountNotSelectedError, InvalidAccountError, InsufficientFundsError, ATMError


class TestATMController(unittest.TestCase):

  def setUp(self):
    self.bank_api = BankAPI()
    self.atm_controller = ATMController(self.bank_api)
    self.bank_api.register_account("123456", "1234", 1000, 5000)
    self.bank_api.register_account("654321", "1999", 100, 30000)

  def _insert_and_authenticate(self, card_number: str, pin: str):
    self.atm_controller.insert_card(card_number)
    self.assertTrue(self.atm_controller.enter_pin(pin))

  def _select_account_and_verify_balance(self, account_type: str, expected_balance: int):
    self.atm_controller.select_account(account_type)
    self.assertEqual(self.atm_controller.check_balance(), expected_balance)

  def test_valid_pin(self):
    self._insert_and_authenticate("123456", "1234")
    self.assertTrue(self.atm_controller.is_authenticated)

  def test_invalid_pin(self):
    self._insert_and_authenticate("654321", "1999")
    self.assertFalse(self.atm_controller.enter_pin("0000"))

  def test_check_balance(self):
    self._insert_and_authenticate("123456", "1234")
    self._select_account_and_verify_balance("Checking", 1000)

  def test_deposit_increases_balance(self):
    self._insert_and_authenticate("654321", "1999")
    self.atm_controller.select_account("Checking")
    self.atm_controller.deposit(500)
    self._select_account_and_verify_balance("Checking", 600)

  def test_withdraw_decreases_balance(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self.atm_controller.withdraw(200)
    self._select_account_and_verify_balance("Checking", 800)

  def test_withdraw_insufficient_funds(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self.assertFalse(self.atm_controller.withdraw(2000))

  def test_select_invalid_account(self):
    self._insert_and_authenticate("123456", "1234")
    with self.assertRaises(InvalidAccountError):
      self.atm_controller.select_account("InvalidAccount")

  def test_deposit_invalid_amount(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self.assertFalse(self.atm_controller.deposit(0)) 
    self.assertFalse(self.atm_controller.deposit(-100))

  def test_withdraw_invalid_amount(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self.assertFalse(self.atm_controller.withdraw(0))
    self.assertFalse(self.atm_controller.withdraw(-100)) 

  def test_account_not_selected(self):
    self._insert_and_authenticate("123456", "1234")
    with self.assertRaises(AccountNotSelectedError):
      self.atm_controller.check_balance()

  def test_invalid_card_number(self):
    self.atm_controller.insert_card("000000")
    self.assertFalse(self.atm_controller.enter_pin("0000"))

  def test_card_ejection_after_operations(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.eject_card()
    self.assertIsNone(self.atm_controller.card_number)
    self.assertFalse(self.atm_controller.is_authenticated)
    self.assertIsNone(self.atm_controller.selected_account)

  def test_multiple_deposits_and_withdrawals(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")

    self.assertEqual(self.atm_controller.check_balance(), 1000)

    self.atm_controller.deposit(500)
    self.assertEqual(self.atm_controller.check_balance(), 1500)

    self.atm_controller.withdraw(300)
    self.assertEqual(self.atm_controller.check_balance(), 1200)

    self.atm_controller.withdraw(1200)
    self.assertEqual(self.atm_controller.check_balance(), 0)

  def test_balance_after_multiple_sessions(self):
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self.atm_controller.deposit(100)
    self._select_account_and_verify_balance("Checking", 1100)

    self.atm_controller.eject_card()
    self._insert_and_authenticate("123456", "1234")
    self.atm_controller.select_account("Checking")
    self._select_account_and_verify_balance("Checking", 1100)

  def test_register_duplicate_account(self):
    with self.assertRaises(InvalidAccountError):
      self.bank_api.register_account("123456", "1234", 500, 3000)

  def test_invalid_withdraw_after_account_selection(self):
    self._insert_and_authenticate("654321", "1999")
    self.atm_controller.select_account("Checking")
    self.assertFalse(self.atm_controller.withdraw(150))  # Insufficient funds (only 100 available)

if __name__ == "__main__":
  unittest.main()
