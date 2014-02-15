CREATE TABLE IF NOT EXISTS agency (
	agency_url TEXT, 
	agency_name TEXT, 
	agency_id TEXT, 
	agency_timezone TEXT, 
	agency_lang TEXT, 
	agency_phone TEXT);
CREATE TABLE IF NOT EXISTS calendar (
	service_id TEXT, 
	start_date TEXT, 
	end_date TEXT, 
	monday INTEGER, 
	tuesday INTEGER, 
	wednesday INTEGER, 
	thursday INTEGER, 
	friday INTEGER, 
	saturday INTEGER, 
	sunday INTEGER
	);
CREATE TABLE IF NOT EXISTS calendar_dates (
	service_id TEXT,
	date TEXT DEFAULT (null) ,
	exception_type TEXT DEFAULT (null) 
	);
CREATE TABLE IF NOT EXISTS feed_info (
	feed_publisher_name TEXT, 
	feed_publisher_url TEXT, 
	feed_lang TEXT, 
	feed_start_date TEXT, 
	feed_end_date TEXT, 
	feed_version TEXT
	);
CREATE TABLE IF NOT EXISTS frequencies (
	trip_id TEXT,
	start_time TEXT,
	end_time TEXT,
	headway_secs INTEGER DEFAULT (null) ,
	exact_times INTEGER
	);
CREATE TABLE IF NOT EXISTS routes (
	route_id TEXT PRIMARY KEY NOT NULL ,
	agency_id TEXT,
	route_short_name TEXT,
	route_long_name TEXT,
	route_desc TEXT,
	route_type TEXT,
	route_color TEXT,
	route_text_color TEXT,
	active BOOL NOT NULL  DEFAULT 'true'
	);
CREATE TABLE IF NOT EXISTS services (
	route_id TEXT,
	service_id TEXT, 
	start_time TEXT,
	end_time TEXT,
	headway_secs INTEGER,
	PRIMARY KEY (
		route_id, 
		service_id, 
		start_time, 
		end_time
		)
	);
CREATE TABLE IF NOT EXISTS shapes (
	shape_id TEXT,
	shape_pt_lat REAL,
	shape_pt_lon REAL,
	shape_pt_sequence INTEGER,
	PRIMARY KEY (
		shape_id,
		shape_pt_sequence
		)
	);
CREATE TABLE IF NOT EXISTS stop_seq (
	trip_id TEXT,
	stop_id TEXT,
	stop_sequence INTEGER, 
	is_timepoint BOOL DEFAULT 'false', 
	shape_dist_traveled FLOAT
	);
CREATE TABLE IF NOT EXISTS stops (
	stop_id TEXT PRIMARY KEY,
	stop_code TEXT,
	stop_desc TEXT,
	stop_name TEXT,
	stop_lat REAL,
	stop_lon REAL, 
	stop_calle TEXT, 
	stop_numero TEXT, 
	stop_entre TEXT, 
	stop_esquina TEXT
	);
CREATE TABLE IF NOT EXISTS stops_removed (
	stop_id TEXT PRIMARY KEY,
	stop_code TEXT,
	stop_desc TEXT,
	stop_name TEXT,
	stop_lat REAL,
	stop_lon REAL, 
	stop_calle TEXT, 
	stop_numero TEXT, 
	stop_entre TEXT, 
	stop_esquina TEXT
	);
CREATE TABLE IF NOT EXISTS timepoints (
	trip_id TEXT, 
	key TEXT, 
	value TEXT
	);
CREATE TABLE IF NOT EXISTS trips (
	route_id TEXT,
	service_id TEXT,
	trip_id TEXT,
	trip_headsign TEXT,
	trip_short_name TEXT,
	direction_id TEXT,
	shape_id TEXT
	);