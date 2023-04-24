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
