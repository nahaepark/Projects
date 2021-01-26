SELECT * FROM 

CREATE VIEW vw_Summary2
AS SELECT customer_no, lt_price, bp_price
FROM customer_information ci ,light_pr lp, bumper_pr bp
WHERE ci.car_code=(SELECT car_code FROM car)
AND lp.lt_code=(SELECT lt_code FROM car WHERE car_code=(SELECT car_code FROM customer_information WHERE customer_no= '7') ) AND 
bp.bp_code=(SELECT bp_code  FROM car WHERE car_code=(SELECT car_code FROM customer_information WHERE customer_no= '7'));


CREATE VIEW vw_S (customer_no,lt_price,bp_price)
AS SELECT ci.customer_no, lp.lt_price, bp.bp_price
FROM customer_information ci , car ,light_pr lp, bumper_pr bp
WHERE ci.car_code=car.car_code AND car.lt_code=lp.lt_code AND car.bp_code=bp.bp_code;

SELECT * FROM vw_S
order BY customer_no;

SELECT lt_price+bp_price AS total FROM vw_S WHERE customer_no='7';