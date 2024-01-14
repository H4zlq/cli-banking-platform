from enum import Enum


class TransactionType(Enum):
  DEPOSIT = "DEPOSIT"
  WITHDRAWAL = "WITHDRAWAL"
  TRANSFER = "TRANSFER"
