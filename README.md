# Trafilea Challenge

This is a Flask-based web application developed as part of the Trafilea challenge. The application allows users to manage their shopping carts and products.


### Installation

```bash
git clone https://github.com/GermanGomez182/trafilea_challenge.git
cd trafilea_challenge
docker build -t trafilea-challenge .
docker run -p 5000:5000 trafilea-challenge
The app will also be accessible at http://localhost:5000.
```


## Endpoints

- **POST /carts**: Create a new cart.
- **GET /carts/:cart_id**: Get cart details.
- **POST /carts/:cart_id/add_product**: Add a product to a cart.
- **POST /products**: Create a new product.
- **GET /products/:product_id**: Get product details.
- **POST /carts/:cart_id/orders**: Create an order from a cart.