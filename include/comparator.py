def compare_lower_cup(gar_price, bin_price):
    if gar_price != -1 and bin_price != -1:
        return round(((gar_price/bin_price)-1.002)*100,3)
    else:
        return None
def compare_higher_cup(gar_price, bin_price):
    if gar_price != -1 and bin_price != -1:
        return round(((gar_price/bin_price)-1.0015)*100,3)
    else:
        return None