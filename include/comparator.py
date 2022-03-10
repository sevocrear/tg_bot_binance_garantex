def compare_lower_cup(gar_price, bin_price):
    return round(((gar_price/bin_price)-1.002)*100,3)

def compare_higher_cup(gar_price, bin_price):
    return round(((gar_price/bin_price)-1.0015)*100,3)