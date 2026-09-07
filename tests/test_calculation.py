from app.calculations import add, divide, sub, mul, BankAccount, insufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def account():
    return BankAccount(100)


@pytest.mark.parametrize("num1, num2, expected", [(2, 3, 5), (1, 1, 2), (0, 0, 0)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_sub():
    assert sub(5, 3) == 2


def test_mul():
    assert mul(2, 3) == 6


def test_divide():
    assert divide(10, 2) == 5


def test_bank_set_initial_amount(account):
    assert account.balance == 100


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdraw(account):
    account.withdraw(50)
    assert account.balance == 50


def test_bank_deposit(account):
    account.deposit(50)
    assert account.balance == 150


def test_bank_collect_interest(account):
    account.collect_interest()
    assert round(account.balance, 6) == 110


@pytest.mark.parametrize(
    "deposit, withdraw, expected",
    [(300, 0, 300), (100, 10, 90), (40, 2, 38), (1000, 1000, 0), (100, 20, 80)],
)
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(account):
    with pytest.raises(insufficientFunds):
        account.withdraw(200)
