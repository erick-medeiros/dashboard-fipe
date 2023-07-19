def brl_to_float(brl: str):
    brl = brl.replace("R$", "")
    translate = brl.maketrans({".": "", ",": "."})
    return float(brl.translate(translate))
