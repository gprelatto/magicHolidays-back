# pz-management-api

## To Set it Up:

* 1 create virtual enviroment: virtualenv venv
* 2 Activate the enviroment: venv\Scripts\activate
* 3 install requirements.txt 
* 4 Migrate the database (only first time running) : python manage.py migrate
* 5 python manage.py createsuperuser --email admin@example.com --username admin
* 6 exec the server: python manage.py runserver


## Current Endpoints:

* "users": "http://127.0.0.1:8000/users/",
* "groups": "http://127.0.0.1:8000/groups/",
* "taxes": "http://127.0.0.1:8000/taxes/",
* "customers": "http://127.0.0.1:8000/customers/",
* "phones": "http://127.0.0.1:8000/phones/",
* "addresses": "http://127.0.0.1:8000/addresses/",
* "products": "http://127.0.0.1:8000/products/",
* "product_types": "http://127.0.0.1:8000/product_types/",
* "prices": "http://127.0.0.1:8000/prices/",
* "price_segments": "http://127.0.0.1:8000/price_segments/",
* "order_headers": "http://127.0.0.1:8000/order_headers/",
* "order_details": "http://127.0.0.1:8000/order_details/",
* "stock": "http://127.0.0.1:8000/stock/"

## Extra Endpoints:

* Under Prices:
	1. actual_price : Returns all the active prices for all the customers
	2. customer_actual_price/PK : Returns all the active prices for a customer (it needs the ID of the customer as a parameter)