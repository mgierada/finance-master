import os
from dotenv import load_dotenv

load_dotenv()

COLUMNS = {
    "#Data operacji": "date",
    "#Opis operacji": "description",
    "#Rachunek": "account",
    "#Kategoria": "category",
    "#Kwota": "raw_amount",
}

CSV_HEADER = (
    "#Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;#Saldo po operacji;"
)

COLUMNS_TO_BE_DROPPED = ["raw_amount", "Unnamed: 6"]

ZUS = "ZAKŁAD UBEZPIECZEŃ SPOŁECZNYCH"
VAT_7 = "URZĄD SKARBOWY, VAT-7"
VAT_PPE = "URZĄD SKARBOWY, PPE"

CONST_EXPENSES = [ZUS, VAT_7, VAT_PPE]
CONST_EXPENSES_REGEX = "|".join(CONST_EXPENSES)
UNWANTED_FIELDS_TAX_RESPONSE = ["index"]

BASED_SALARY = int(os.environ.get("BASED_SALARY", 1))
MONTHLY_HOUR_MEAN = int(os.environ.get("MONTHLY_HOUR_MEAN", 1))
ZUS_MONTHLY_EXPENSES = float(os.environ.get("ZUS_MONTHLY_EXPENSES", 1))
BONUS_EXPENSE = float(os.environ.get("BONUS_EXPENSE", 1))
BONUS_INCOME = float(os.environ.get("BONUS_INCOME", 1))
