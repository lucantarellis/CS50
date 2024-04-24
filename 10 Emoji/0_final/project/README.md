# Project title: Local Store
## Video demo: https://youtu.be/i5SaZbELVl4

## Table of Contents
+ [Introduction](#introduction)
+ [Features](#features)
+ [Endpoints](#endpoints)
+ [HTML files and design choices](#html-files-and-design-choices)
+ [Styles](#Styles)
+ [SQLite tables](#sqlite-tables)
+ [Learnings](#learnings)

## Introduction
The Local Store app is a Flask-based web application that facilitates a direct connection between local producers and customers. It enables users to browse and purchase artisanal products from local farmers. This README outlines the key features and design choices that contribute to the app's functionality.

## Features
**User Authentication:**
+ The app supports user registration and login using password hashing and the `werkzeug.security` library. Password hashes are stored in the database for security.

**Store Selection:**
+ Users can explore various local stores, view products, and place orders.

**Order Processing:**
+ The app allows users to select products from local stores, calculates the order subtotal and total costs, and provides an order summary before processing the order.

**Session Management:**
+ The Flask-Session extension is employed to manage user sessions. Sessions are used to store temporary order data and user login information.

**Database Interaction:**
+ The app interacts with an SQLite database to manage and store user accounts, product details, store information, and order history.

**Dynamic content:**
+ The app dynamically generates and displays most of the content by calling the required database. Aditionally, each user has their own order history, so they can check out in which store and what products they bought in the past.

## Endpoints
The following endpoints handle different functionalities of the app:

### **`/:`**
+ **Fucntionality:** Renders the home page after user authentication.
+ **HTTP Method:** GET
+ **Requirements:** User must be authenticated.
+ **Explanation:** Landing page for authenticated users. It shows information about the steps required to complete an order and some next steps.

### **`/login:`**
+ **Fucntionality:** Manages user login and session creation.
+ **HTTP Method:** GET (for displaying login page) | POST (for validating user credentials)
+ **Explanation:** Users can submit their credentials (username and password) to log in. The app verifies the information against the database, creates a user session, and redirects the user to the home page upon successful authentication. In case the user inputs wrong or insufficient information, descriptive errors will raise.

### **`/logout:`**
+ **Fucntionality:** Ends the user session.
+ **Explanation:** Users can click the "Log Out" button to end their session and return to the login page.

### **`/register:`**
+ **Fucntionality:** Handles user registration and account creation.
+ **HTTP Method:** GET (for displaying the register page) | POST (for validating user information is correct, prevent duplicates and add the user data to the database)
+ **Explanation:** Users can create a new account by providing a username, password, and email. The app checks for valid input, hashes the password, stores the user's information in the database, and logs the user in automatically.

### **`/store:`**
+ **Fucntionality:** Allows users to select products and place orders.
+ **HTTP Method:** GET (for displaying store and products) | POST (for processing temporary orders)
+ **Requirements:** User must be authenticated.
+ **Explanation:** This endpoint presents the user with a list of products available in a specific store. Users can select products and quantities, and upon submission, the app processes the temporary order and calculates the order subtotal (in the checkout).

### **`/checkout:`**
+ **Fucntionality:** Processes orders and their details.
+ **HTTP Method:** POST
+ **Requirements:** User must be authenticated.
+ **Explanation:** After the user submits an order, this endpoint processes the order details, showing the products, quantities, and total cost. Finally, if the user clicks on "finish order", inserts the order details into the database.

### **`/local-stores:`**
+ **Fucntionality:** Displays a list of local stores.
+ **HTTP Method:** GET
+ **Requirements:** User must be authenticated.
+ **Explanation:** Users can explore and select from a list of available local stores, which leads to the store's products page.

### **`/orders:`**
+ **Fucntionality:** Shows order history for the logged-in user.
+ **HTTP Method:** GET (for displaying user's orders) | POST (for calling the database for all the order details and redirect the user to the requested order)
+ **Requirements:** User must be authenticated.
+ **Explanation:** This endpoint provides users with a history of their past orders, including order IDs, dates, and store names. Clicking on an order ID displays detailed order information.

### **`/wip:`**
+ **Fucntionality:** Renders a work-in-progress page.
+ **HTTP Method:** GET
+ **Explanation:** This endpoint displays a placeholder page indicating that a particular feature is currently under development.

## HTML files and design choices

### **`layout.html`**
Defines the app's general layout, including the navigation bar and footer. It is reused across various endpoints, enhancing consistency.
#### Design choices
+ A different layout(menuless) was created for login, registration and checkout pages in order to enhance user experience.

### **`login.html`** and **`register.html`**
This files presents users with a straightforward login form (login.html) and an option to create an account if they don't have one (register.html).

### **`index.html`**
Serves as the app's landing page, offering an introduction and call to action for users to explore local stores.

### **`local-stores.html`**
Dynamically lists local stores and their offerings. Each store card includes a link to browse products.
#### Design choices
+ Store information is dynamically fetched from the database, enabling flexibility and scalability.

### **`store.html`**
Shows users the available products from a selected store, allowing them to adjust quantities before checkout.
#### Design choices
+ JavaScript functionality enables real-time updates of the total price as users adjust quantities.

### **`checkout.html`**
Presents users with a summary of their order details so they can review them before finalizing their purchase. It dynamically populates the table with selected products, prices, quantities, and subtotals.
#### Design choices
+ Users can buy products from a single store per order. Future iterations may allow multiple orders from different stores.
+ The layout is menuless to eliminate distractions and facilitate focused order completion.
+ Payment processing occurs at the physical store.

### **`success.html`**
Confirms the successful placement of an order, providing the user with an order ID and store details.

### **`orders.html`**
Presents users with a list of their past orders, allowing them to navigate to order details.

### **`myorder.html`**
Displays a list of a user's past orders, providing links to view detailed information for each order.

## Styles
I used a combination of some Bootstrap elements and a custom stylesheet to shape the visual presentation of the Local Store app. While Bootstrap provided a solid foundation for responsive design and UI components, I also took the opportunity to create unique design elements of my own.

## SQLite tables
The foundation of the Local Store app's functionality lies in a set of thoughtfully designed SQLite tables, each chosen to cater to specific needs and ensure efficient data handling.

### Users
To safeguard user information and facilitate secure access, the "users" table stores user credentials and optional contact details, with password security enhanced through hash implementation.

```SQL
CREATE TABLE
  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT
  );
```

### Stores and products
The initial approach involved a single table encompassing both stores and products. However, as the back-end development progressed, a strategic shift led to the separation of "stores" and "products" tables. Meanwhile, the choice of using integer values (cents) instead of floating-point numbers for prices ensures precision and minimizes potential complexities related to floating-point accuracy in SQLite.

```SQL
CREATE TABLE
  stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    img TEXT
  );

CREATE TABLE
  products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    store_id INT NOT NULL,
    product TEXT,
    cents INT,
    FOREIGN KEY (store_id) REFERENCES stores (id)
  );
```
### Orders
Structuring the "orders" system was a significant challenge. I defined a strategic solution by utilizing a dual-table arrangement. The "order_line" table adeptly manages product quantities tied to an order, while the principal "orders" table efficiently logs essential order details.

```SQL
CREATE TABLE
  order_line (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
  );
```

```SQL
CREATE TABLE
  orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT NOT NULL,
    store_id INT NOT NULL,
    DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
  );
```

## Learnings
Throughout the process of developing the Local Store app, several valuable lessons were learned that contributed to both technical and design aspects. These learnings have provided a deeper understanding on how to create an user-friendly, online platform for connecting local producers and customers.

### Dynamic Content: Flexibility and Scalability
One of the most significant learnings was the power of dynamic content generation. By leveraging the Flask framework and integrating it with a relational database, the Local Store app achieved flexibility and scalability. This allowed me to dynamically generate and display content such as local stores, product listings, order histories, and more. Dynamic content greatly simplified the process of updating and expanding the app's offerings, enabling future integration of new local producers and products.

### User-Centered Design: Focus on Clarity and Efficiency
Design choices played an important role in enhancing the user experience. By prioritizing clarity and efficiency, I aimed to provide users with a streamlined journey from browsing products to placing orders. The decision to use a menuless layout during the checkout process was guided by the intention to minimize distractions and prioritize the completion of the order.

### Data Management and User Sessions
The Local Store app highlights the importance of effective data management and user session handling. Storing order details and user information in session variables proved crucial for maintaining continuity and coherence throughout the user's interaction with the app. This approach facilitated the seamless transition between different pages and ensured that user-specific data, such as order histories, could be easily retrieved and displayed.

### Continuous Learning and Iteration
The journey of developing the Local Store app proved that software development is an iterative process. As the project progressed, new concepts, tools, and techniques were discovered and applied. For instance, incorporating JavaScript to enable real-time updates of order totals in the "store" page.

In conclusion, the Local Store app development journey was marked by continuous learning and adaptation. The project highlighted the importance of dynamic content, user-centered design, effective data management, and the iterative nature of software development. These learnings have not only contributed to the app's functionality but also enriched my understanding of building user-friendly and efficient web applications.

There's only one more thing left to say:
# Thanks to all the CS50x staff! You are the best.