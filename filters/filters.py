

def loadFilterPriceState(obj, borders):
    """
    #TODO: uncomment and repair
    dic = {}
    for border in borders:
        if border in obj.get_args:
            dic["price_" + border] = str("%.2f" % (obj.get_args[border]/100.0))
            return dic
    """
    return {"price_to":'0.00', "price_from":'0.00'}



def loadFilterState(obj, dic, name):
    get = []#obj.get_args[name] if name in obj.get_args else []
    r = []
    for group_name, group_item_list in dic.items():
        r.append({"name":group_name, "items":[ {'name':item, 'isFilterActive':(item in get)} for item in group_item_list]})
    return r