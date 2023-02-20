from beanie.operators import RegEx,And,Or,In,GTE,LTE, GT,LT
from server.models.device import Device



async def filters(category,condition,color,brand,location,min_price,max_price):
    
    category_pattern = f'^{category}$' if category != None else rf'[a-zA-Z0-9_]'
    condition_pattern =f'^{condition}$' if condition != None else rf'[a-zA-Z0-9_]'
    color_pattern =f'^{color}$' if color != None else rf'[a-zA-Z0-9_]'
    brand_pattern =f'^{brand}$' if brand != None else rf'[a-zA-Z0-9_]'
    location_pattern =f'^{location}$' if location != None else rf'[a-zA-Z0-9_]'
    minimum_price = min_price if min_price != None else 0
    maximum_price = max_price if max_price != None else 0
   
    if maximum_price == 0 and minimum_price == 0:
        result = await Device.find(And((RegEx(Device.category, category_pattern,"i")),(RegEx(Device.first_condition, condition_pattern,"i")),
                                       (RegEx(Device.color, color_pattern,"i")),(RegEx(Device.brand, brand_pattern, "i")),
                                       (RegEx(Device.location, location_pattern,"i")))).to_list()

    if maximum_price != 0 and minimum_price == 0:
        result = await Device.find(And((RegEx(Device.category, category_pattern,"i")),(RegEx(Device.first_condition, condition_pattern,"i")),
                                       (RegEx(Device.color, color_pattern,"i")),(RegEx(Device.brand, brand_pattern, "i")),
                                       (RegEx(Device.location, location_pattern,"i")),
                                       (LTE(Device.discount_price,int(maximum_price))))).to_list()

    if minimum_price != 0 and maximum_price == 0:
        result = await Device.find(And((RegEx(Device.category, category_pattern,"i")),(RegEx(Device.first_condition, condition_pattern,"i")),
                                       (RegEx(Device.color, color_pattern,"i")),(RegEx(Device.brand, brand_pattern, "i")),
                                       (RegEx(Device.location, location_pattern,"i")),(GTE(Device.discount_price,int(minimum_price))))).to_list()

    if minimum_price != 0 and maximum_price != 0:
        result = []
        data_obj = await Device.find(And((RegEx(Device.category, category_pattern,"i")),(RegEx(Device.first_condition, condition_pattern,"i")),
                                       (RegEx(Device.color, color_pattern,"i")),(RegEx(Device.brand, brand_pattern, "i")),
                                       (RegEx(Device.location, location_pattern,"i")))).to_list()
        for  data in data_obj:
            if data.discount_price in range(int(minimum_price),int(maximum_price)+1):
                result.append(data)
    return result
