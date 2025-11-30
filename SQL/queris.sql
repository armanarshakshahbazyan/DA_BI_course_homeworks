SELECT customers.customerName,customers.addressLine1, sum(priceEach*quantityOrdered) as
revenue
FROM orders
LEFT JOIN customers ON orders.customerNumber = customers.customerNumber
LEFT JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
GROUP BY customers.customerName,customers.addressLine1
ORDER BY revenue DESC
LIMIT 5 ;