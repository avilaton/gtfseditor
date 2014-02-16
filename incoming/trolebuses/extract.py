GET trips 

SELECT * FROM stop_seq WHERE trip_id IN
(SELECT trip_id FROM trips WHERE route_id='TA' OR route_id='TB' OR route_id='TC')

GET STOPS

SELECT * FROM stops WHERE stop_id IN
	(SELECT DISTINCT stop_id FROM stop_seq 
	    WHERE trip_id IN
	        (SELECT trip_id FROM trips 
	            WHERE route_id='TA' OR route_id='TB' OR route_id='TC'
	        )
	)