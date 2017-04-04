CREATE VIEW foreign_data.course_complete AS
SELECT
co.*,

tc.source__title,
tc.source__location,

tc.driver__first_name,
tc.driver__last_name,
tc.driver__username,

tc.request_datetime,
tc.requested_arrival_datetime,
tc.arrival_datetime,
tc.assign_datetime,
tc.seen_datetime,
tc.accept_datetime,
tc.cancel_datetime,

tc.trip_type,
tc.state,

cf.price
     
FROM
foreign_data.tracking_course co
LEFT JOIN foreign_data.trip_complete tc ON co.trip_id = tc.id
LEFT JOIN foreign_data.accounting_coursefinancials cf ON cf.course_id = co.id;


