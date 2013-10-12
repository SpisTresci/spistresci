

def loadFilterPriceState(obj, borders):
    dic = {}
    for border in borders:
        if border in obj.get_args:
            dic["price_" + border] = str("%.2f" % (obj.get_args[border]/100.0))
    return dic

def loadFilterState(obj, dic, name):
    get = []#obj.get_args[name] if name in obj.get_args else []
    r = []
    for group_name, group_item_list in dic.items():
        r.append({"name":group_name, "items":[ {'name':item, 'isFilterActive':(item in get)} for item in group_item_list]})
    return r