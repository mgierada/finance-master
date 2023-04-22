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
