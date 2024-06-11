
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

inprogress_order = {}

@app.post("/")
async def handle_request(request: Request):
    #Retreive the JSON data from the request
    payload = await request.json()

    #Extract the necessary information from thr payload
    #based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'order.add-context:ongoing-order':add_to_order,
        'order.remove-context:on-going':remove_from_order,
        'order.complete:Context_ongoing-order': complete_order,
        'track.order-context:ongoing-tracking':track_order
    }

    return intent_handler_dict[intent](parameters, session_id)


def add_to_order(parameters: dict,session_id:str):
    food_item = parameters["food-items"]
    quantities = parameters["number"]

    if len(food_item) != len(quantities):
        fulfillment_text = "Sorry I didn't understood! Can you specify the food items and Quantites"
    else:
        new_food_dict = dict(zip(food_item,quantities))

    if session_id in inprogress_order:
        current_food_dict = inprogress_order[session_id]
        current_food_dict.update(new_food_dict)
        inprogress_order[session_id] = current_food_dict
    else:
        inprogress_order[session_id] = new_food_dict


    print("*********************************")   
    print(inprogress_order) 

    order_str = generic_helper.get_str_from_food_dict(inprogress_order[session_id])
    fulfillment_text =  f"So far you have: {order_str}. Do you need naything else?"
     
    return JSONResponse(content={
            "fulfillmentText":  fulfillment_text
        })    



    if intent == 'track.order-context:ongoing-tracking':
       return track_order(parameters)



def track_order(parameters:dict, session_id:str):
        order_id = int(parameters['order_id'])
        order_status = db_helper.get_order_status(order_id)

        if order_status:
            fulfillment_text  = f"The order status for order id: {order_id} is: {order_status}"
        else:
            fulfillment_text  = f"No order found with order id: {order_id}"

        return JSONResponse(content={
            "fulfillmentText":  fulfillment_text
        })

        

def complete_order(parameters:dict,session_id:str):
    if session_id not in inprogress_order:
        fulfillment_text = "I'm having trouble finding your order. Sorry! Can you place a new order again!"    
    else:
        order = inprogress_order[session_id]    
        order_id = save_to_db(order) 

        if order_id == -1:
            fulfillment_text = "Sorry, We couldn't process your order due to a backend error." \
                          "Please place a new order again"
        else: 
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order."\
                f"Here is your order id #{order_id}."\
                f"Your order total is {order_total} which you can pay at the time of delivery!"                  

        del inprogress_order[session_id]

        return JSONResponse(content={
            "fulfillmentText":fulfillment_text
        })



def save_to_db(order: dict):

     next_order_id = db_helper.get_next_order_id()

     for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
        food_item,
        quantity,
        next_order_id
        )

        if rcode == -1:
            return -1

     db_helper.insert_order_tracking(next_order_id,"in progress")        
     return next_order_id       



def remove_from_order(parameters: dict, session_id:str):
    if session_id not in inprogress_order:
        return JSONResponse(content={
            "fulfillemtText":"I'm having trouble finding your order.Sorry! Kindly place new order."
        })  

    current_order = inprogress_order[session_id]
    food_item = parameters["food-items"]

    removed_items = []
    no_such_items = []

    for item in food_item:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]  

    if len(removed_items) > 0:
        fulfillment_text = f'Removed{",".join(removed_items)} from your order.'     

    if len(no_such_items) > 0:
        fulfillment_text = f'Your current order does not exist {",".join(no_such_items)}'  

    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)   
        fulfillment_text += f" Here, what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })   
