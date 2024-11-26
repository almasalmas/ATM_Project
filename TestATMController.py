import unittest
from BankAPI import BankAPI
from ATMController import ATMController

class TestATMController(unittest.TestCase):
    
  def setUp(self):
    self.bank_api = BankAPI()
    self.atm_controller = ATMController(self.bank_api)
    self.bank_api.register_account("123456", "1234", 1000, 5000)
    self.bank_api.register_account("654321", "1999", 100, 30000)
      
  def test_valid_pin(self):
    self.atm_controller.insert_card("123456")
    self.assertTrue(self.atm_controller.enter_pin("1234"))  

  def test_invalid_pin(self):
    self.atm_controller.insert_card("654321")
    self.assertFalse(self.atm_controller.enter_pin("0000")) 

  def test_check_balance(self):
    self.atm_controller.insert_card("123456")
    self.atm_controller.enter_pin("1234")
    self.atm_controller.select_account("Checking")
    self.assertEqual(self.atm_controller.check_balance(), 1000)

  def test_deposit(self):
    self.atm_controller.insert_card("654321")
    self.atm_controller.enter_pin("1999")
    self.atm_controller.select_account("Checking")
    self.atm_controller.deposit(500)
    self.assertEqual(self.atm_controller.check_balance(), 600)

  def test_withdraw(self):
    self.atm_controller.insert_card("123456")
    self.atm_controller.enter_pin("1234")
    self.atm_controller.select_account("Checking")
    self.atm_controller.withdraw(200)
    self.assertEqual(self.atm_controller.check_balance(), 800)

  def test_withdraw_insufficient_funds(self):
    self.atm_controller.insert_card("123456")
    self.atm_controller.enter_pin("1234")
    self.atm_controller.select_account("Checking")
    self.assertFalse(self.atm_controller.withdraw(2000))

if __name__ == "__main__":
    unittest.main()
