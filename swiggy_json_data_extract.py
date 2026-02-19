
import json

def json_to_dictionary(file_path):
    with open(file_path, "r") as file:
        dict_data = json.load(file)
    return dict_data

def extract_data(dict_data):
    swiggy_base_url = "https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/"
    swiggy_data = []
    cards_list = dict_data["data"]["cards"]
    for cards_dict in cards_list:
        if cards_dict.get("card").get("card").get("gridElements"):
            items_list = cards_dict["card"]["card"]["gridElements"]["infoWithStyle"]["items"]
            for items_dict in items_list:
                product_dict = {}
                product_dict["Product Name"] = items_dict["displayName"]
                product_dict["Product ID"] = items_dict["productId"]
                product_dict["Product Price"] = float(items_dict["variations"][0]["price"]["offerPrice"]["units"])
                product_dict["Product quantity"] = str(items_dict["variations"][0]["quantityDescription"])
                product_dict["Product Image Url"] = [swiggy_base_url + url for url in items_dict["variations"][0]["imageIds"]]
                Discount = items_dict["variations"][0]["price"]["offerApplied"]["listingDescription"].split("%")
                for num in Discount:
                    if num.isdigit():
                        Discount = int(num)
                product_dict["Discount percentage"] = Discount
                product_dict["Product Mrp"] = float(items_dict["variations"][0]["price"]["mrp"]["units"])
                product_dict["is_available"] = items_dict["isAvail"]
                swiggy_data.append(product_dict)
    print(swiggy_data)
    return swiggy_data

def convert_dict_to_json_data(extract_list):
    path = "C:/Users/vishal.kushvanshi/PycharmProjects/swiggy_json_data/" + "Extract_data.json"
    with open(path,"w") as file:
        json.dump(extract_list,file, indent=4)



file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/swiggy_json_data/" + "keyword_serach_data.json"
# file_path = "C:/Users/vishal.kushvanshi/PycharmProjects/swiggy_json_data/" + "data-2026218105913.json"

print(file_path)
dict_data = json_to_dictionary(file_path)
extract_list = extract_data(dict_data)
convert_dict_to_json_data(extract_list)


