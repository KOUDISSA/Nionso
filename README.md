# Nionso API

Built with Django REST Framework

This project was developed as part of the Meta Backend Developer 
Professional Certificate program on Coursera.

It's a Restaurant Management REST API that allows customers to 
register and create an authentication token for performing 
different actions.

The API has an authorization system that recognizes if a user 
is a customer, a manager or a delivery-crew member.

The API utilizes **Djoser** for Authentication. It automatically 
creates generic endpoints for register, login, change password, 
etc. Available in the 
[Djoser documentation](https://djoser.readthedocs.io).

---

## Technologies

- Python 3
- Django
- Django REST Framework
- Djoser
- SQLITE 3

---

## Installation

```bash
git clone https://github.com/[username]/[repo]
cd [repo]
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

---

## Available Endpoints

### Menu Items

**`/api/menu-items/`**

An authenticated customer can view all menu items with 
search, filtering and ordering. A manager can add new 
menu items via POST request with title, price, category 
and featured status. Pagination is implemented.

**`/api/menu-items/<int:pk>`**

An authenticated customer can retrieve a single menu item. 
A manager can also update and delete it.

---

### User Groups

**`/api/groups/manager/users`**

A manager can view all managers and promote a customer 
to manager.

**`/api/groups/manager/users/<int:pk>`**

A manager can remove another manager from the list.

**`/api/groups/delivery-crew/users`**

Managers can view all delivery crew members and add 
a new one from existing customers.

**`/api/groups/delivery-crew/users/<int:pk>`**

Managers can remove a delivery crew member.

---

### Cart

**`/api/cart/menu-items`**

A customer can add menu items to the cart via POST 
request with item ID and quantity. GET request shows 
only the customer's own cart items with unit price 
and total price. Managers can view all customers' carts.


### Categories

**`/api/category`**

A manager can view and add new categories.

### Orders

**`/api/orders`**

A customer can create an order from their cart via a 
blank POST request. The view automatically retrieves 
cart items and converts them into order items linked 
to an order object containing the date, the user, 
the assigned delivery crew (None by default) and 
the total price. The cart is automatically cleared 
after the order is placed.

- **Customer** — can only view their own orders
- **Delivery crew** — can only view orders assigned to them
- **Manager** — can view all orders

**`/api/orders/<int:pk>`**

- **Customer** — can view a specific order if it belongs to them
- **Manager** — can assign a delivery crew member to an order 
  and delete orders
- **Delivery crew** — can update only the status field of orders 
  assigned to them

---

## Author

Exaucé KOUDISSA
GitHub : github.com/KOUDISSA
Email : delicatngongo@gmail.Com
