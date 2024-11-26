import unittest
from BankAPI import BankAPI
from ATMController import ATMController

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
    with self.assertRaises(Exception):
      self.atm_controller.select_account("InvalidAccount")

if __name__ == "__main__":
  unittest.main()
