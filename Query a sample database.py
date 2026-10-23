import sqlite3

# 1. Create an in-memory sample database
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, customer_name TEXT)")
cur.execute("""CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_amount REAL)""")

# 2. Insert sample data
cur.executemany("INSERT INTO customers VALUES (?, ?)", [
    (1, "Alice"), (2, "Bob"), (3, "Charlie"), (4, "Diana"), (5, "Evan"), (6, "Fiona"),
])
cur.executemany("INSERT INTO orders (customer_id, order_amount) VALUES (?, ?)", [
    (1, 250), (1, 400), (2, 150), (2, 100), (3, 900),
    (4, 300), (4, 200), (4, 350), (5, 50), (6, 600),
])

# 3. Top customers by total spend
print("Top 5 customers by total spend")
cur.execute("""
    SELECT c.customer_id, c.customer_name,
           COUNT(o.order_id) AS total_orders,
           SUM(o.order_amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Orders: {row[2]}, Spent: {row[3]}")

# 4. Overall average order value
cur.execute("SELECT AVG(order_amount) FROM orders")
print("\nOverall average order value:", round(cur.fetchone()[0], 2))

# 5. Average order value per customer
print("\nAverage order value per customer")
cur.execute("""
    SELECT c.customer_name, ROUND(AVG(o.order_amount), 2) AS avg_order_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name
    ORDER BY avg_order_value DESC
""")
for name, avg in cur.fetchall():
    print(f"{name}: {avg}")

conn.close()