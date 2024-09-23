from pymongo import MongoClient
from pymongo import errors
from bson.objectid import ObjectId
try:
    client = MongoClient("mongodb://localhost..../")
    db = client["MarketDB"]
    prod_collection = db["products"]
    order_collection = db["orders"]
except errors.ConnectionFaluire as e:
    print(f"Could not connect to MongoDB {e}")
    exit()


def add_product(name, price, created_at, expiry_date):
    prod_collection.insert_one({"name": name, "price":price, "created_at": created_at, "expiry_date":expiry_date})

def remove_product(product_id):
    prod_collection.delete_one({"_id": ObjectId(product_id)})

def update_product(product_id, new_name, new_price, new_created_at, new_expiry_date):
    prod_collection.update_one({"_id": ObjectId(product_id)}, {"$set": {"name": new_name, "price": new_price, "created_at": new_created_at, "expiry_date": new_expiry_date}})

def view_products():
    for product in prod_collection.find():
        print(f"{product['_id']}--> product: {product['name']}, price: {product['price']}, created_at: {product['created_at']}, expiry_date: {product['expiry_date']}")

def add_order(product_name, quantity, customer_name, status):
    order_collection.insert_one({"product_name": product_name, "quantity": quantity, "customer": customer_name, "status": status})

def remove_order(order_id):
    order_collection.delete_one({"_id": ObjectId(order_id)})

def update_order(order_id, new_product_name, new_quantity, new_customer_name, new_status):
    order_collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"product_name": new_product_name, "quantity": new_quantity, "customer": new_customer_name, "status": new_status}})

def view_orders():
    for order in order_collection.find():
        print(f"{order["_id"]}--> product_name: {order["product_name"]}, quantity: {order["quantity"]}, customer: {order['customer']} status: {order['status']}")

def main():
    while True:
        try:
            print("ENTER CHOICE FROM THE MENU")
            print("1. Product details")
            print("2. Place order")
            print("3. Exit")
            choice = int(input("Enter your choice: "))

            match(choice):

                case 1:
                    while(True):
                        print("ENTER THE CHOICE")
                        print("1. Add new product")
                        print("2. Remove product")
                        print("3. Update product details")
                        print("4. View products")
                        print("5. Exit")

                        ch = int(input("Enter your choice: "))
                        match(ch):

                            case 1:
                                name = input("Enter the name of product: ")
                                price = int(input("Enter the price of product: "))
                                created_at = input("Enter manufacturing date: ")
                                expiry_date = input("Enter expiry date: ")
                                add_product(name, price, created_at, expiry_date)
                            
                            case 2:
                                prod_id = input("Enter product id to remove: ")
                                remove_product(prod_id)
                            
                            case 3:
                                prod_id = input("Enter product id to be updated: ")
                                new_name = input("Enter the new name of product: ")
                                new_price = int(input("Enter the new price fo product: "))
                                new_created_at = input("Enter new manufacturing date: ")
                                new_expiry_date = input("Enter new expiry date: ")
                                update_product(prod_id, new_name, new_price, new_created_at, new_expiry_date)
                            
                            case 4:
                                view_products()

                            case 5:
                                break

                            case _:
                                print("Invalid Choice..")

                case 2:

                    while(True):
                        print("ENTER CHOICE FROM THE MENU")
                        print("1. Add new ordre")
                        print("2. Remove order")
                        print("3. Update order details")
                        print("4. View orders")
                        print("5. Exit")
                        ch = int(input("Enter your choice"))
                        match(ch):

                            case 1:
                                product_name = input("Enter the product name: ")
                                quantity = int(input("Enter order quantity: "))
                                customer_name = input("Enter customer name: ")
                                status = input("Enter order status: ")
                                add_order(product_name, quantity, customer_name, status)

                            case 2:
                                order_id = input("Enter order id to remove: ")
                                remove_order(order_id)
                            
                            case 3:
                                order_id = input("Enter order id to update: ")
                                new_product_name = input("Enter the new product name: ")
                                new_quantity = int(input("Enter new order quantity: "))
                                new_customer_name = input("Enter new customer name: ")
                                new_status = input("Enter new order status: ")
                                
                                update_order(order_id, new_product_name, new_quantity, new_customer_name, new_status)
                            
                            case 4:
                                view_orders()
                                pass
                            
                            case 5:
                                break

                            case _:
                                print("Invalid choice..")
                
                case 3:
                    print("Exiting...")
                    break
        except ValueError:
            print("Invalid input, Please enter a number.")


if __name__ == "__main__":
    main()
