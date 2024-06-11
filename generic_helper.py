import re


def  extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/",session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""    

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])




if __name__=="__main__":

    print(get_str_from_food_dict({"samosa":2, "chhole":5}))
    print(extract_session_id("projects/mira-chatbot-for-food-del-saga/agent/sessions/acb6e80a-f9a4-0cd0-b3f4-e343288ec66e/contexts/ongoing-order"))


def get_next_order_id():
    cursor = cnn.cursor()
    #Executing the sql query to get the next available order_id
    query = "SELECT max(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the connection
    cursor.close()

    #Returning the next availabl order_id
    if result is None:
        return 1
    else:
        return result + 1
