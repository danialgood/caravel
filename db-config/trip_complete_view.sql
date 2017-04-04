CREATE VIEW foreign_data.trip_complete AS
SELECT
t.*,
c.title source__title,
c.location source__location,


d.first_name driver__first_name,
d.last_name driver__last_name,
d.username driver__username,

tf.price

FROM
foreign_data.tracking_client c, foreign_data.tracking_trip t
LEFT JOIN foreign_data.driver_named d ON t.driver_id = d.id
LEFT JOIN foreign_data.accounting_tripfinancials tf ON tf.trip_id = t.id
WHERE t.source_id = c.id;
