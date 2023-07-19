import datetime


def brl_to_float(brl: str):
    brl = brl.replace("R$", "")
    translate = brl.maketrans({".": "", ",": "."})
    return float(brl.translate(translate))


def br_date(date: str) -> datetime:
    date = date.split()

    year = int(date[2])
    month = 0

    match date[0]:
        case "janeiro":
            month = 1
        case "fevereiro":
            month = 2
        case "março":
            month = 3
        case "abril":
            month = 4
        case "maio":
            month = 5
        case "junho":
            month = 6
        case "julho":
            month = 7
        case "agosto":
            month = 8
        case "setembro":
            month = 9
        case "outubro":
            month = 10
        case "novembro":
            month = 11
        case "dezembro":
            month = 12

    if month == 0:
        print("Error month = 0")

    return datetime.datetime(year, month, 1)
