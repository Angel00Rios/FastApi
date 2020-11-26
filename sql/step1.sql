SELECT productos_de_venta.id_producto, productos.nombre, count(*) as ventas_totales
FROM venta
INNER JOIN productos_de_venta
	ON productos_de_venta.id_venta = venta.id_venta
inner join productos on productos_de_venta.id_producto = productos.codigo 
group by productos_de_venta.id_producto
order by ventas_totales desc