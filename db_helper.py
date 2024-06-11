import mysql.connector
global conn

conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql@2023",
            database="pandeyji_eatery"
        )

def get_order_status(order_id: int):
   
        # Create cursor
        cursor = conn.cursor()
        
        # Execute SQL query to fetch status for the given order_id
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
       
       #Execute the query
        cursor.execute(query, (order_id,))
        
        # Fetch the status
        result = cursor.fetchone()

        #Close the cursor and connection
        cursor.close()
        # conn.close()
        
        if result is not None:
            return result[0]
        else:
            return None  

def get_next_order_id():
    cursor = conn.cursor()

    #Executing the SQL Query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    
    #Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()   
            
    #Returning the next available order_id 

    if result is None:
        return 1
    else:
        return result + 1

    

def insert_order_item(food_item,quantity,order_id):
  try: 
      cursor = conn.cursor()

      cursor.callproc('insert_order_item', (food_item,quantity,order_id))

    #committing the changes
      conn.commit()
    
    # Closing the cursor
      cursor.close()   

      print("Order item inserted successfully")

      return 1

  except mysql.connector.Error as err:
    print(f"Error inserting order item: {err}")

    # Rollback changes if necessary
    conn.rollback()

    return -1

  except Exception as e:
    print(f"An error occurred: {e}")
    # Rollback changes if necessary
    conn.rollback()

    return -1



def get_total_order_price(order_id):
    cursor = conn.cursor()
    #Executing the SQL qury to get the total order price
    query = f"SELECT get_total_order_price({order_id})" 
    cursor.execute(query)

    #Fetching the result
    result = cursor.fetchone()[0]

    #Closing the cursor
    cursor.close()

    return result

def insert_order_tracking(order_id,status):
    cursor = conn.cursor()

    # Inserting the record into order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s,%s)"
    cursor.execute(insert_query, (order_id, status))

    #Commiting the changes
    conn.commit()

    # Closing the cursor
    cursor.close()

            
              
       