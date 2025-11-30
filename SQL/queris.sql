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


SELECT products.productCode , products.productName , SUM(orderdetails.quantityOrdered) AS
QUANTITY
from products
LEFT JOIN orderdetails on products.productCode = orderdetails.productCode
WHERE orderdetails.quantityOrdered IS NOT NULL
GROUP BY products.productCode , products.productName
ORDER BY QUANTITY ASC
LIMIT 5;


SELECT orders.orderDate,SUM(orderdetails.priceEach*orderdetails.quantityOrdered) AS Total
FROM orderdetails
LEFT JOIN orders on orderdetails.orderNumber=orders.orderNumber
GROUP BY orders.orderDate;


WITH all_order AS (
SELECT orderdetails.orderNumber,SUM(orderdetails.quantityOrdered*orderdetails.priceEach) as coast
FROM orderdetails
GROUP BY orderdetails.orderNumber
)
SELECT DISTINCT employees.employeeNumber,employees.lastName,employees.firstName
FROM employees
LEFT JOIN customers on customers.salesRepEmployeeNumber=employees.employeeNumber
LEFT JOIN orders on orders.customerNumber=customers.customerNumber
LEFT JOIN all_order on all_order.orderNumber=orders.orderNumber
WHERE all_order.coast &gt; (SELECT AVG(coast) FROM all_order);