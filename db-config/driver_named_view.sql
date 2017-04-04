CREATE VIEW foreign_data.driver_named AS
SELECT

d.*,
u.first_name,
u.last_name,
u.username

FROM
foreign_data.auth_user u
INNER JOIN foreign_data.tracking_driver d ON d.user_id = u.id;
