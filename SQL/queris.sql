SELECT customers.customerName,customers.addressLine1, sum(priceEach*quantityOrdered) as
revenue
FROM orders
LEFT JOIN customers ON orders.customerNumber = customers.customerNumber
LEFT JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
GROUP BY customers.customerName,customers.addressLine1
ORDER BY revenue DESC
LIMIT 5 ;



SELECT customers.customerName,SUM(payments.amount) AS Done,
sum(orderdetails.priceEach*orderdetails.quantityOrdered) AS
Must,SUM(orderdetails.priceEach*orderdetails.quantityOrdered)-SUM(payments.amount) as Dubt
FROM customers
JOIN payments ON customers.customerNumber=payments.customerNumber
JOIN orders on customers.customerNumber=orders.customerNumber
JOIN orderdetails ON orders.orderNumber=orderdetails.orderNumber
GROUP BY customers.customerName
ORDER BY customers.customerName;

