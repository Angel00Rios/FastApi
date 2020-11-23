SELECT distinct productos_de_venta.id_producto 
FROM venta 
INNER JOIN productos_de_venta
	ON productos_de_venta.id_venta = venta.id_venta
where  year(venta.fecha_de_venta) <= year(NOW()- INTERVAL 365 day)
group by venta.id_venta