SELECT DATE(venta.fecha_de_venta) AS Fecha,
       productos_de_venta.id_producto AS Producto,
       SUM(productos_de_venta.cantidad_comprada) AS Cantidad
FROM venta
INNER JOIN productos_de_venta
	ON productos_de_venta.id_venta = venta.id_venta
WHERE productos_de_venta.id_producto = '{}'
GROUP BY Fecha, Producto