# ATM Controller System

## Description
This project simulates the controller logic for an ATM machine. It handles card insertion, PIN validation, account selection, balance checks, deposits, and withdrawals. The bank API is mocked for testing purposes and is flexible for future integration with real banking systems.

## Requirements
- Python 3.x
- unittest (for testing)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/almasalmas/ATM_Project.git

2. Testing (Run)
To run the unit tests, use the following command:

  ```bash
    python -m unittest TestATMController.py
  ```  

3. Code Structure
```bash
/atm-controller
├── BankAPI.py        # Contains logic for interacting with a bank (mocked)
├── ATMController.py  # Contains logic for ATM operations (controller)
├── exceptions.py     # Custom exceptions for error handling
├── TestATMController.py       # Unit tests for ATMController
└── README.md         # Project documentation
```

Future Work/Improvements
- Integrate with a real bank system for validating PIN and processing transactions.
- Add user interface for interacting with the ATM system.
- Implement additional security features (e.g., account lock after multiple failed PIN attempts).
