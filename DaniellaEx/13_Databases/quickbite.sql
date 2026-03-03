-- Query 1 Select all restaurants sorted by name alphabetically.
SELECT *
FROM restaurants r
ORDER BY r.name ASC;
-- Query 2 Select all menu items that cost more than ₪40, sorted by price descending.
SELECT *
FROM menu m
WHERE m.price > 40.00
ORDER BY m.price DESC;
-- Query 3 Find all restaurants whose name contains "burger" (case-insensitive).
SELECT *
FROM restaurants r
WHERE r.name LIKE '%burger%';
-- Query 4 Select all orders with status `delivered` or `cancelled`.
SELECT *
FROM orders o
WHERE o.status='delivered' OR o.status='cancelled';
-- Query 5 Find all menu items in the `Dessert` category, sorted by price ascending.
SELECT *
FROM menu m
WHERE m.category='Dessert'
ORDER BY m.price ASC;
-- Query 6  Select all customers who registered in 2024.
SELECT *
FROM customers c
WHERE c.registration_date BETWEEN '2024-1-1' AND '2024-12-31';
-- Query 7 Find all restaurants with a rating of 4.0 or higher that are active.
SELECT *
FROM restaurants r
WHERE r.rating >= 4 AND r.is_active=TRUE;
-- Query 8 Show all orders with the customer name and restaurant name.
SELECT o.id AS "order id",c.name AS "customer" ,r.name AS "restaurant"
FROM orders o
INNER JOIN customers c
ON o.customer_id=c.id
INNER JOIN restaurants r
on r.id=o.restaurant_id;

-- Query 9  For each restaurant,show how many menu items they have. Sort by count descending.
SELECT r.name AS "restaurant name ", count(m.id) AS "namber of items"
FROM restaurants r 
INNER JOIN menu m
ON r.id=m.restaurant_id 
GROUP BY r.name
ORDER BY 2 DESC;
-- Query 10 Show all reviews alongside the customer name and restaurant name.
SELECT rev.comment ,c.name AS customer_name , r.name AS restaurant_name
FROM review rev 
INNER JOIN customers c
ON rev.customer_id=c.id
INNER JOIN restaurants r
ON rev.restaurant_id =r.id;
-- Query 11 For each order, calculate the **total price** (sum of item price × quantity). 
-- Show the order ID, customer name, restaurant name, and total.
SELECT o.id AS "order id" ,c.name AS "customer name" ,r.name AS "restaurant name" ,sum(m.price * order_items.quantity) AS "total price"
FROM order_items
INNER JOIN orders o
ON o.id = order_items.order_id
INNER JOIN menu m
ON  order_items.menu_id=m.id
INNER JOIN  customers c 
ON o.customer_id = c.id
INNER JOIN restaurants r 
ON o.restaurant_id = r.id
GROUP BY o.id , c.name ,r.name;
-- Query 12 Find the **most expensive menu item** for each restaurant. Show restaurant name, item name, and price.
SELECT r.name AS "restaurant name" ,m.name AS "item name" ,  m.price AS "most expensive menu item"
FROM restaurants r
INNER JOIN menu m
ON m.restaurant_id=r.id 
WHERE m.price = (
                 SELECT MAX(m2.price) 
                 FROM menu m2 
                 WHERE m2.restaurant_id=r.id )
ORDER BY m.price DESC;
-- Query 13 Show the **number of orders per status** (how many pending, how many delivered, etc.)		
SELECT o.status ,count(*) AS "number of orders per status"
FROM orders o
GROUP BY o.status;
-- Query 14 List all customers who have **never placed an order**.
SELECT c.name 
FROM customers c 
LEFT JOIN orders o 
ON c.id = o.customer_id
WHERE o.customer_id is NULL ;
--  Query 15 For each restaurant, show the **average review rating**. 
-- Only include restaurants with **3 or more reviews**. Sort by average rating descending.
SELECT r.name AS "restaurant name" , AVG(review.rating) AS "average review rating",COUNT(*) AS "number of the reviews" 
FROM restaurants r
INNER JOIN review 
ON r.id = review.restaurant_id
GROUP BY r.name
HAVING COUNT(*)>=3;
-- Query 16 Find the **top 3 customers** by total amount spent across all their orders.
SELECT  c.name AS "customer name"  ,sum(m.price * order_items.quantity) AS "total price"
FROM order_items
INNER JOIN orders o
ON o.id = order_items.order_id
INNER JOIN menu m
ON  order_items.menu_id=m.id
INNER JOIN  customers c 
ON o.customer_id = c.id
GROUP BY c.name 
ORDER BY 2 DESC
LIMIT 3;
-- Query 17 Find customers who have ordered from **more than 3 different restaurants**
SELECT c.name AS "customer name" , COUNT(DISTINCT o.restaurant_id) AS " order from more than 3 different restaurants"
FROM orders o
INNER JOIN customers c
ON o.customer_id=c.id 
GROUP BY c.name
HAVING COUNT(o.restaurant_id)>3;
-- Query 18
-- Write a single query that shows a **"platform dashboard"**:
-- Total active restaurants
-- Total customers
-- Total delivered orders this month
-- Total revenue this month
-- Average order value this month
-- The cuisine type with the highest revenue this month
SELECT   "Total active restaurants" AS "description"  , COUNT(*) AS VALUE 
FROM restaurants r
WHERE r.is_active=TRUE 
UNION 
SELECT  "Total customers" ,COUNT(*)
FROM customers 
UNION 
SELECT "Total delivered orders this month" , COUNT(*)
FROM orders o 
WHERE o.status="delivered"
     AND MONTH(O.date_time)=MONTH(curdate())
     AND YEAR(O.date_time)=YEAR (curdate())
UNION
SELECT "Total revenue this month" , sum(m.price * order_items.quantity)
FROM order_items
INNER JOIN orders o
ON o.id = order_items.order_id
INNER JOIN menu m
ON  order_items.menu_id=m.id
WHERE o.status="delivered"
     AND MONTH(O.date_time)=MONTH(curdate())
     AND YEAR(O.date_time)=YEAR (curdate())
UNION
SELECT  "Average order value this month", ROUND(AVG( order_total),2)
FROM(
     SELECT O.id,SUM(m.price * order_items.quantity) as order_total
     FROM order_items
     INNER JOIN orders o
     ON o.id = order_items.order_id
     INNER JOIN menu m
     ON  order_items.menu_id=m.id
     WHERE o.status="delivered"
       AND MONTH(O.date_time)=MONTH(curdate())
       AND YEAR(O.date_time)=YEAR (curdate())
     GROUP BY o.id  
) AS t
UNION 
SELECT "The cuisine type with the highest revenue this month",
      (
        SELECT r.cuisine_type
        FROM order_items
	    INNER JOIN orders o
        ON o.id = order_items.order_id
        INNER JOIN menu m
        ON  order_items.menu_id=m.id
        INNER JOIN  customers c 
	    ON o.customer_id = c.id
        INNER JOIN restaurants r 
        ON o.restaurant_id = r.id
		WHERE o.status="delivered"
          AND MONTH(O.date_time)=MONTH(curdate())
          AND YEAR(O.date_time)=YEAR (curdate())
        GROUP BY r.cuisine_type 
        ORDER BY SUM(m.price * order_items.quantity) DESC 
        LIMIT 1
      );  
