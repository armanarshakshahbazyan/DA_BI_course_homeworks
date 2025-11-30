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



SELECT products.productCode,products.productName,SUM((orderdetails.priceEach -
products.buyPrice) * orderdetails.quantityOrdered) AS totalProfit
FROM orderdetails
JOIN products ON orderdetails.productCode = products.productCode
GROUP BY products.productCode, products.productName
ORDER BY totalProfit DESC
)
-- name_surname as (

-- select customers.customerNumber,employees.firstName + employees.lastName as anunazg

-- from customers

-- left join employees on employees.employeeNumber = customers.salesRepEmployeeNumber
-- left join orders on orders.customerNumber = customers.customerNumber
-- )

select order_info.orderDate,status,products.productName,customerName,city,revenue ,
profit.totalProfit, customers.salesRepEmployeeNumber
from order_info
left join products on products.productCode = order_info.productCode
left join customers on customers.customerNumber = order_info.customerNumber
left join profit on profit.productName = products.productName

-- left join name_surname on name_surname.customerNumber = orders.customerNumber
;



with order_info AS (
select customerNumber,productCode,orderDate,orderdetails.orderNumber,status,priceEach,
sum(priceEach*quantityOrdered) AS revenue
from orderdetails
left join orders on orderdetails.orderNumber=orders.orderNumber
Group by customerNumber,productCode, orderdetails.orderNumber,priceEach,status
),

profit as (
SELECT products.productCode,products.productName,SUM((orderdetails.priceEach -
products.buyPrice) * orderdetails.quantityOrdered) AS totalProfit
FROM orderdetails
JOIN products ON orderdetails.productCode = products.productCode
GROUP BY products.productCode, products.productName
ORDER BY totalProfit DESC
)
-- name_surname as (

-- select customers.customerNumber,employees.firstName + employees.lastName as anunazg

-- from customers

-- left join employees on employees.employeeNumber = customers.salesRepEmployeeNumber
-- left join orders on orders.customerNumber = customers.customerNumber
-- )

select order_info.orderDate,status,products.productName,customerName,city,revenue ,
profit.totalProfit,
CONCAT(employees.firstName, &#39; &#39;, employees.lastName) AS SalesRepName
from order_info
left join products on products.productCode = order_info.productCode
left join customers on customers.customerNumber = order_info.customerNumber
left join profit on profit.productName = products.productName
LEFT JOIN employees ON employees.employeeNumber = customers.salesRepEmployeeNumber;
-- left join name_surname on name_surname.customerNumber = orders.customerNumber
;