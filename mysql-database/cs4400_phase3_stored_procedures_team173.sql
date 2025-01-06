
-- CS4400: Introduction to Database Systems (Fall 2024)
-- Project Phase III: Stored Procedures SHELL [v3] Thursday, Nov 7, 2024
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use business_supply;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin

If ip_username is NULL then leave sp_main; end if;
If ip_first_name is NULL then leave sp_main; end if;
If ip_last_name is NULL then leave sp_main; end if;
If ip_birthdate is NULL then leave sp_main; end if;
If ip_address is NULL then leave sp_main; end if;
    -- ensure new owner has a unique username
    if ip_username in (select username from users) then leave sp_main; 	end if;
    
    insert into users (username, first_name, last_name, address, birthdate) 
    values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    
    insert into business_owners (username) 
    values (ip_username);
end //
delimiter ;

-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated driver or
worker roles.  A new employee must have a unique username and a unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin
	If ip_username is NULL then leave sp_main; end if;
	If ip_first_name is NULL then leave sp_main; end if;
	If ip_last_name is NULL then leave sp_main; end if;
	If ip_birthdate is NULL then leave sp_main; end if;
	If ip_address is NULL then leave sp_main; end if;
	If ip_taxID is NULL then leave sp_main; end if;
	If ip_hired is NULL then leave sp_main; end if;
	If ip_employee_experience is NULL then leave sp_main; end if;
	If ip_salary is NULL then leave sp_main; end if;
    -- ensure new owner has a unique username
    -- ensure new employee has a unique tax identifier
   if ip_username in (select username from users) then leave sp_main; 	end if;
   if ip_taxID in (select taxID from employees) then leave sp_main; 	end if;
   insert into users (username, first_name, last_name, address, birthdate) 
   values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
   
   insert into employees (username, taxID, hired, experience, salary) 
   values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary);
end //
delimiter ;

-- [3] add_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the driver role to an existing employee.  The
employee/new driver must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_driver_role;
delimiter //
create procedure add_driver_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_license_type varchar(40), in ip_driver_experience integer)
sp_main: begin
	If ip_username is NULL then leave sp_main; end if;
If ip_licenseID is NULL then leave sp_main; end if;
If ip_license_type is NULL then leave sp_main; end if;
If ip_driver_experience is NULL then leave sp_main; end if;
    -- ensure employee exists and is not a worker
    -- ensure new driver has a unique license identifier
    if ip_username not in (select username from users) then leave sp_main; 	end if;
    if ip_username in (select username from workers) then leave sp_main; 	end if;
	if ip_licenseID in (select licenseID from drivers) then leave sp_main; 	end if;
    insert into drivers (username, licenseID, license_type, successful_trips) 
    values (ip_username,ip_licenseID, ip_license_type, ip_driver_experience);
end //
delimiter ;

-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin
	If ip_username is NULL then leave sp_main; end if;
    -- ensure employee exists and is not a driver
    if ip_username not in (select username from users) then leave sp_main; 	end if;
	if ip_username in (select username from drivers) then leave sp_main; 	end if;
	insert into workers (username) 
 	values (ip_username);
end //
delimiter ;

-- [5] add_product()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new product.  A new product must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_product;
delimiter //
create procedure add_product (in ip_barcode varchar(40), in ip_name varchar(100),
	in ip_weight integer)
sp_main: begin
	If ip_barcode is NULL then leave sp_main; end if;
	If ip_name is NULL then leave sp_main; end if;
	If ip_weight is NULL then leave sp_main; end if;
	-- ensure new product doesn't already exist
     if ip_barcode in (select barcode from products) then leave sp_main; 	end if;
     insert into products (barcode, iname, weight) 
     values (ip_barcode, ip_name, ip_weight);
end //
delimiter ;

-- [6] add_van()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new van.  A new van must be assigned 
to a valid delivery service and must have a unique tag.  Also, it must be driven
by a valid driver initially (i.e., driver works for the same service). And the van's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_van;
delimiter //
create procedure add_van (in ip_id varchar(40), in ip_tag integer, in ip_fuel integer,
	in ip_capacity integer, in ip_sales integer, in ip_driven_by varchar(40))
sp_main: begin
	
	DECLARE van_exists INT DEFAULT 0;
    DECLARE service_exists INT DEFAULT 0;
    DECLARE driver_valid INT DEFAULT 0;
    
    If ip_id is NULL then leave sp_main; end if;
	If ip_tag is NULL then leave sp_main; end if;
	If ip_fuel is NULL then leave sp_main; end if;
	If ip_capacity is NULL then leave sp_main; end if;
	If ip_sales is NULL then leave sp_main; end if;

    SELECT COUNT(*) INTO van_exists FROM vans WHERE tag = ip_tag;
    IF van_exists > 0 THEN LEAVE sp_main; 
    END IF;

    SELECT COUNT(*) INTO service_exists FROM delivery_services WHERE id = ip_id;
    IF service_exists = 0 THEN LEAVE sp_main; 
    END IF;

    SELECT COUNT(*) INTO driver_valid FROM drivers WHERE username = ip_driven_by;
    IF driver_valid = 0 THEN LEAVE sp_main; 
    END IF;

    INSERT INTO vans (tag, fuel, capacity, sales, driven_by, id, located_at)
    VALUES (ip_tag, ip_fuel, ip_capacity, ip_sales, ip_driven_by, ip_id, 
            (SELECT home_base FROM delivery_services WHERE id = ip_id));
end //
delimiter ;

-- [7] add_business()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new business.  A new business must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_business;
delimiter //
create procedure add_business (in ip_long_name varchar(40), in ip_rating integer,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
	-- ensure new business doesn't already exist
    -- ensure that the location is valid
    -- ensure that the rating is valid (i.e., between 1 and 5 inclusively)
    declare business_exists int default 0;
    declare location_exists int default 0;
    If ip_long_name is NULL then leave sp_main; end if;
    If ip_rating is NULL then leave sp_main; end if;
    If ip_spent is NULL then leave sp_main; end if;
    If ip_location is NULL then leave sp_main; end if;


   
    select count(*) into business_exists from businesses where long_name = ip_long_name;
	if business_exists > 0 then leave sp_main; end if;
    
    select count(*) into location_exists from locations where label = ip_location;
	if location_exists = 0 then leave sp_main; end if;
    
    if ip_rating < 1 or ip_rating > 5 then
    leave sp_main; end if;
    
    insert into businesses (long_name, rating, spent, location)
    values(ip_long_name, ip_rating, ip_spent, ip_location);
end //
delimiter ;

-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
	-- ensure new delivery service doesn't already exist
    -- ensure that the home base location is valid
    -- ensure that the manager is valid
    
    declare service_exists int default 0;
	declare homebase_exists int default 0;
	declare manager_exists int default 0;
     If ip_id is NULL then leave sp_main; end if;
    If ip_long_name is NULL then leave sp_main; end if;
    If ip_home_base is NULL then leave sp_main; end if;

    
    select count(*) into service_exists from delivery_services where id = ip_id;
	if service_exists > 0 then leave sp_main; end if;
    
    select count(*) into homebase_exists from locations where label = ip_home_base;
	if homebase_exists = 0 then leave sp_main; end if;
    
    
    if ip_manager is not NULL then
        select count(*) into manager_exists from workers where username = ip_manager;
        if manager_exists = 0 then leave sp_main; end if;
    end if;
    
	-- select count(*) into manager_exists from workers where username = ip_manager;
	-- if manager_exists = 0 then leave sp_main; end if;
    
    insert into delivery_services (id, long_name, home_base, manager) 
    values (ip_id, ip_long_name, ip_home_base, ip_manager);
    
end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid van
destination.  A new location must have a unique combination of coordinates. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord integer,
	in ip_y_coord integer, in ip_space integer)
sp_main: begin
	-- ensure new location doesn't already exist
    -- ensure that the coordinate combination is distinct
    
	declare label_exists int default 0;
	declare coordinates_exists int default 0;
   If ip_x_coord is NULL then leave sp_main; end if;
   If ip_y_coord is NULL then leave sp_main; end if;
   If ip_label is NULL then leave sp_main; end if;

	
    
    select count(*) into label_exists from locations where label = ip_label;
	if label_exists > 0 then leave sp_main; end if;
    
    select count(*) into coordinates_exists from locations where x_coord = ip_x_coord and y_coord = ip_y_coord;
	if coordinates_exists > 0 then leave sp_main; end if;
    
	
    
    insert into locations (label, x_coord, y_coord, space) 
    values (ip_label, ip_x_coord, ip_y_coord, ip_space);
end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a business owner to provide funds
to a business. The owner and business must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_amount integer, in ip_long_name varchar(40), in ip_fund_date date)
sp_main: begin
	-- ensure the owner and business are valid
    declare owner_exists int default 0;
    declare business_exists int default 0;
   If ip_owner is NULL then leave sp_main; end if;
   If ip_fund_date is NULL then leave sp_main; end if;
   If ip_long_name is NULL then leave sp_main; end if;

    
	select count(*) into owner_exists from business_owners where username = ip_owner;
	if owner_exists = 0 then leave sp_main; end if;
   
    select count(*) into business_exists from businesses where long_name = ip_long_name;
	if business_exists = 0 then leave sp_main; end if;

    insert into fund(username, invested, invested_date, business)
    values(ip_owner, ip_amount, ip_fund_date, ip_long_name);
end //
delimiter ;

-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires a worker to work for a delivery service.
If a worker is actively serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter //
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee hasn't already been hired by that service
	-- ensure that the employee and delivery service are valid
    -- ensure that the employee isn't a manager for another service
    
    declare employee_exists int default 0;
    declare service_exists int default 0;
	declare is_manager int default 0;
    declare already_hired int default 0;
      If ip_username is NULL then leave sp_main; end if;
    If ip_id is NULL then leave sp_main; end if;

    
	select count(*) into employee_exists from employees where username = ip_username;
	if employee_exists = 0 then leave sp_main; end if;
   
    select count(*) into service_exists from delivery_services where id = ip_id;
	if service_exists = 0 then leave sp_main; end if;
    
    select count(*) into already_hired from work_for where username = ip_username and id = ip_id;
	if already_hired > 0 then leave sp_main; end if;
   
    select count(*) into is_manager from delivery_services where manager = ip_username and id != ip_id;
	if is_manager > 0 then leave sp_main; end if;

    insert into work_for(username, id)
    values(ip_username, ip_id);
end //
delimiter ;

-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires a worker who is currently working for a delivery
service.  The only restriction is that the employee must not be serving as a manager 
for the service. Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	
    -- null checks
    if ip_username is null or ip_id is null then 
        leave sp_main; 
    end if;
    
    -- ensure that the employee is currently working for the service
    if not exists (select 1 from work_for where username = ip_username and id = ip_id) then 
        leave sp_main; 
    end if;

    -- ensure that the employee isn't an active manager
    if (select manager from delivery_services where id = ip_id) = ip_username then
        leave sp_main;
    end if;
    
    -- ensure the service has more than one employee
    if (select count(*) from work_for where id = ip_id) < 2 then
        leave sp_main;
    end if;
    
    delete from work_for where username = ip_username and id = ip_id;
    
    
    
<<<<<<< HEAD
    
    
	-- declare is_manager int default 0;
--     declare is_working int default 0;
--    If ip_username is NULL then leave sp_main; end if;
--     If ip_id is NULL then leave sp_main; end if;

--     
-- 	
--     
--     select count(*) into is_working from work_for where username = ip_username and id = ip_id;
-- 	if is_working = 0 then leave sp_main; end if;
--    
--     select count(*) into is_manager from delivery_services where manager = ip_username and id != ip_id;
-- 	if is_manager > 0 then leave sp_main; end if;

--     delete from work_for where username = ip_username and id = ip_id; 
    
=======
>>>>>>> a1649d76c192cfc9892326af16b099c4db22fd4c
end //
delimiter ;

-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints a worker who is currently hired by a delivery
service as the new manager for that service.  The only restrictions is that
the worker must not be working for any other delivery service. Otherwise, the appointment 
to manager is permitted.  The current manager is simply replaced. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    -- ensure that the employee isn't working for any other services
    
    declare working_elsewhere int default 0;
    declare is_working int default 0;
    If ip_id is NULL then leave sp_main; end if;
    If ip_username is NULL then leave sp_main; end if;


    select count(*) into is_working from work_for where username = ip_username and id = ip_id;
	if is_working = 0 then leave sp_main; end if;
   
    select count(*) into working_elsewhere from work_for where username = ip_username and id != ip_id;
	if working_elsewhere > 0 then leave sp_main; end if;

    update delivery_services
    set manager = ip_username where id = ip_id;
end //
delimiter ;
-- [14] takeover_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid driver to take control of a van owned by 
the same delivery service. The current controller of the van is simply relieved 
of those duties. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_van;
delimiter //
create procedure takeover_van (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin
    DECLARE is_valid_driver INT DEFAULT 0;
    DECLARE van_belongs_to_service INT DEFAULT 0;
    DECLARE driver_assigned_elsewhere INT DEFAULT 0;

    If ip_id is NULL then leave sp_main; end if;
    If ip_username is NULL then leave sp_main; end if;
    If ip_tag is NULL then leave sp_main; end if;
    SELECT COUNT(*) INTO is_valid_driver FROM drivers WHERE username = ip_username;

    IF is_valid_driver = 0 THEN
        LEAVE sp_main;
    END IF;

    SELECT COUNT(*) INTO driver_assigned_elsewhere FROM vans WHERE driven_by = ip_username AND id != ip_id;

    IF driver_assigned_elsewhere > 0 THEN
        LEAVE sp_main; 
    END IF;

    SELECT COUNT(*) INTO van_belongs_to_service FROM vans WHERE tag = ip_tag AND id = ip_id;

    IF van_belongs_to_service = 0 THEN
        LEAVE sp_main; 
    END IF;

    UPDATE vans SET driven_by = ip_username WHERE tag = ip_tag AND id = ip_id;
end //
delimiter ;

-- [15] load_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific product to a van's payload so that we can sell them for some
specific price to other businesses.  The van can only be loaded if it's located
at its delivery service's home base, and the van must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the product already loaded onto the van as applicable.  And if the product
already exists on the van, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_van;
delimiter //
create procedure load_van (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin
    DECLARE van_capacity INT DEFAULT 0;
    DECLARE current_payload INT DEFAULT 0;
    DECLARE product_exists INT DEFAULT 0;
    DECLARE is_at_home_base INT DEFAULT 0;
    DECLARE home_base_location VARCHAR(40);
    DECLARE van_location VARCHAR(40);
    DECLARE new_payload INT DEFAULT 0;
    
    If ip_id is NULL then leave sp_main; end if;
    If ip_barcode is NULL then leave sp_main; end if;
    If ip_tag is NULL then leave sp_main; end if;
    If ip_price is NULL then leave sp_main; end if;

    IF ip_more_packages <= 0 THEN
        LEAVE sp_main;
    END IF;
    SELECT COUNT(*) INTO is_at_home_base FROM vans v JOIN delivery_services ds ON v.id = ds.id WHERE v.tag = ip_tag AND v.id = ip_id;

    IF is_at_home_base = 0 THEN
        LEAVE sp_main;
    END IF;

    SELECT COUNT(*) INTO product_exists FROM products WHERE barcode = ip_barcode;

    IF product_exists = 0 THEN
        LEAVE sp_main;
    END IF;

    SELECT ds.home_base INTO home_base_location FROM delivery_services ds JOIN vans v ON ds.id = v.id WHERE v.id = ip_id AND v.tag = ip_tag;

    SELECT located_at INTO van_location FROM vans WHERE id = ip_id AND tag = ip_tag; 
    
    IF van_location != home_base_location THEN
        LEAVE sp_main;
    END IF;

    SELECT v.capacity, IFNULL(SUM(c.quantity), 0)INTO van_capacity, current_payload FROM vans v LEFT JOIN contain c ON v.id = c.id AND v.tag = c.tag WHERE v.id = ip_id AND v.tag = ip_tag GROUP BY v.capacity;

    SET new_payload = current_payload + ip_more_packages;

    IF new_payload > van_capacity THEN
        LEAVE sp_main;
    END IF;

    INSERT INTO contain (id, tag, barcode, quantity, price) VALUES (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price) ON DUPLICATE KEY UPDATE quantity = quantity + ip_more_packages;

END //
DELIMITER ;

--  CALL load_van('lcc', 1, '16_WEF6', 1, 20);
-- CALL load_van('mbm', 1, 'hm_5E7L23M', 5, 29);



-- [16] refuel_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a van. The van can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_van;
delimiter //
create procedure refuel_van (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin

    -- null checks
    if ip_id is null or ip_tag is null or ip_more_fuel is null then
        leave sp_main;
    end if;

    -- ensure that the specified van exists and belongs to the given service
    if not exists (select 1 from vans where id = ip_id and tag = ip_tag) then
        leave sp_main;
    end if;

    -- ensure that the van is currently located at the service's home base
    if (select located_at from vans where id = ip_id and tag = ip_tag) 
       <> (select home_base from delivery_services where id = ip_id) then
        leave sp_main;
    end if;

    -- refuel
    update vans set fuel = fuel + ip_more_fuel
    where id = ip_id and tag = ip_tag;

   --  DECLARE current_fuel INT DEFAULT 0;
--     DECLARE van_location VARCHAR(40);
--     DECLARE home_base_location VARCHAR(40);
--     
--     If ip_id is NULL then leave sp_main; end if;
-- 	If ip_tag is NULL then leave sp_main; end if;

--     IF ip_more_fuel <= 0 THEN
--         LEAVE sp_main;
--     END IF;

--     SELECT fuel, located_at INTO current_fuel, van_location FROM vans WHERE id = ip_id AND tag = ip_tag LIMIT 1;

--     IF current_fuel IS NULL OR van_location IS NULL THEN 
--         LEAVE sp_main; 
--     END IF;

--     SELECT home_base INTO home_base_location FROM delivery_services WHERE id = ip_id;
--     IF van_location != home_base_location THEN 
--         LEAVE sp_main; 
--     END IF;

--     UPDATE vans SET fuel = fuel + ip_more_fuel WHERE id = ip_id AND tag = ip_tag;

end //
delimiter ;

-- [17] drive_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single van to a new
location (i.e., destination). This will also update the respective driver's 
experience and van's fuel. The main constraints on the van(s) being able to 
move to a new  location are fuel and space.  A van can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a van can only move to a destination if there's enough
space remaining at the destination. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
    declare d_x, d_y, a_x, a_y double;
    declare computed_fuel int;

    if ip_departure = ip_arrival then
        return 0;
    end if;

    -- Retrieve coordinates for both departure and arrival locations
    select x_coord, y_coord into d_x, d_y
    from locations
    where label = ip_departure;

    select x_coord, y_coord into a_x, a_y
    from locations
    where label = ip_arrival;

    -- Compute the required fuel based on distance
    set computed_fuel = 1 + truncate(sqrt(power(a_x - d_x, 2) + power(a_y - d_y, 2)), 0);
    return computed_fuel;
-- 	if (ip_departure = ip_arrival) then return 0;
--     else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
-- 		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
--         (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
-- 	end if;
end //
delimiter ;

drop procedure if exists drive_van;
delimiter //
create procedure drive_van (in ip_id varchar(40), in ip_tag integer, in ip_destination varchar(40))
sp_main: begin
    -- Variables to store necessary details
    declare current_location varchar(40);
    declare base_location varchar(40);
    declare current_fuel int;
    declare fuel_needed_to_target int;
    declare fuel_needed_back_home int;
    declare total_fuel_needed int;
    declare spot_available int;
    declare assigned_driver varchar(40);

    -- Basic input validation
    if ip_id is null or ip_tag is null or ip_destination is null then
        leave sp_main;
    end if;

    -- Confirm that the target location is known
    if (select count(*) from locations where label = ip_destination) = 0 then
        leave sp_main;
    end if;

    -- Retrieve the van’s current status and the manager’s home base
    select home_base into base_location from delivery_services where id = ip_id;
    select located_at, fuel, driven_by into current_location, current_fuel, assigned_driver
    from vans
    where id = ip_id and tag = ip_tag;

    -- Ensure the van actually exists for the given service
    if current_location is null or assigned_driver is null then
        leave sp_main;
    end if;

    -- If the van is already at the requested destination, no trip is needed
    if current_location = ip_destination then
        leave sp_main;
    end if;

    -- Calculate fuel requirements: to destination and then back to home base
    set fuel_needed_to_target = fuel_required(current_location, ip_destination);
    set fuel_needed_back_home = fuel_required(ip_destination, base_location);
    set total_fuel_needed = fuel_needed_to_target + fuel_needed_back_home;

    -- Check if the van has enough fuel for the round trip portion
    if current_fuel < total_fuel_needed then
        leave sp_main;
    end if;

    -- Ensure the destination has room for an additional van
    select space into spot_available from locations where label = ip_destination;
    if spot_available is not null and spot_available < 1 then
        leave sp_main;
    end if;

    -- Update the van’s location and fuel levels after traveling
    update vans
    set located_at = ip_destination,
        fuel = fuel - fuel_needed_to_target
    where id = ip_id and tag = ip_tag;

    -- The driver has successfully completed a trip
    update drivers
    set successful_trips = successful_trips + 1
    where username = assigned_driver;
    



    -- ensure that the destination is a valid location
    -- ensure that the van isn't already at the location
    -- ensure that the van has enough fuel to reach the destination and (then) home base
    -- ensure that the van has enough space at the destination for the trip
<<<<<<< HEAD
    


    
 --    
--     declare curr_loc varchar (40);
--     declare home_base varchar (40);
--     declare destination_exists int default 0;
-- 	declare v_fuel int default 0;
-- 	declare req_fuel_to_destination int default 0;
--     declare driven_by_driver varchar(40);
--     declare req_fuel_to_home int default 0;
--     declare total_fuel_req int default 0;
--     declare available_space int default 0;
--     
--     If ip_id is NULL then leave sp_main; end if;
-- 	If ip_tag is NULL then leave sp_main; end if;
--     
-- 	select count(*) into destination_exists from locations where label = ip_destination;
-- 	if destination_exists = 0 then leave sp_main; end if;
--     
--     
--     select located_at, fuel, driven_by into curr_loc, v_fuel, driven_by_driver from vans
--     where id = ip_id and tag = ip_tag;
-- 	if curr_loc = ip_destination then leave sp_main; end if;
--     
--     select home_base into home_base from delivery_services where id = ip_id;
--     
--     set req_fuel_to_destination = fuel_required(curr_loc, ip_destination);
--     set req_fuel_to_home = fuel_required(ip_destination, home_base);
-- 	set total_fuel_req = req_fuel_to_destination + req_fuel_to_home;
--     
--     if v_fuel < total_fuel_req then leave sp_main; end if;
--     
--     select space into available_space from locations where label = ip_destination;
--     
--     if available_space is not null and available_space < 1 then leave sp_main; end if;
--     
--     update vans 
--     set located_at = ip_destination, fuel = fuel - req_fuel_to_destination
--     where id = ip_id and tag = ip_tag;
--     
--     update drivers
--     set successful_trips = successful_trips + 1 
--     where username = driven_by_driver;
    
=======

>>>>>>> a1649d76c192cfc9892326af16b099c4db22fd4c
end //
delimiter ;

-- [18] purchase_product()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a business to purchase products from a van
at its current location.  The van must have the desired quantity of the product
being purchased.  And the business must have enough money to purchase the
products.  If the transaction is otherwise valid, then the van and business
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_product;
delimiter //
create procedure purchase_product (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
sp_main: begin

	-- ensure that the business is valid
    -- ensure that the van is valid and exists at the business's location
	-- ensure that the van has enough of the requested product
	-- update the monies spent and gained for the van and business
	-- update the van's payload
    -- ensure all quantities in the payload table are greater than zero
    
	declare prod_price integer;
    declare prod_quantity integer;
	declare business_funds integer;
    declare business_spent_total integer;
    declare van_total_sales integer;
	declare total_transaction_cost integer;
	declare van_location varchar(40);
    
    If ip_long_name is NULL then leave sp_main; end if;
	If ip_id is NULL then leave sp_main; end if;
	If ip_tag is NULL then leave sp_main; end if;
	If ip_barcode is NULL then leave sp_main; end if;
	If ip_quantity is NULL then leave sp_main; end if;

	
    if ip_long_name not in (select long_name from businesses) then leave sp_main; end if;
    

    if (ip_id, ip_tag) not in (select id, tag from vans) then leave sp_main; end if;
    select located_at into van_location from vans where id = ip_id and tag = ip_tag;
    if van_location not in (select location from businesses where long_name = ip_long_name) 
    then leave sp_main; end if;
    

    select price, quantity into prod_price, prod_quantity from contain
	where (id, tag) = (ip_id, ip_tag) and barcode = ip_barcode;

	if prod_quantity is null or prod_quantity < ip_quantity then leave sp_main; end if;
    

    update contain set quantity = prod_quantity - ip_quantity
	where id = ip_id and tag = ip_tag and barcode = ip_barcode;
    

    
    set total_transaction_cost = (prod_price * ip_quantity);
    
	select spent into business_spent_total from businesses where long_name = ip_long_name;
    update businesses set spent = (business_spent_total + total_transaction_cost) where long_name = ip_long_name;
    
    select sales into van_total_sales from vans where id = ip_id and tag = ip_tag;
	update vans set sales = van_total_sales + total_transaction_cost where (id, tag) = (ip_id, ip_tag);
    
   
    delete from contain where quantity <= 0;

end //
delimiter ;

-- [19] remove_product()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a product from the system.  The removal can
occur if, and only if, the product is not being carried by any vans. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_product;
delimiter //
create procedure remove_product (in ip_barcode varchar(40))
sp_main: begin



	-- ensure that the product exists
    -- ensure that the product is not being carried by any vans
    declare product_exists int default 0;
    declare product_carried int default 0;
    If ip_barcode is NULL then leave sp_main; end if;
    
    select count(*) into product_exists from products where barcode = ip_barcode;
    if product_exists = 0 then leave sp_main; end if;
    
    select count(*) into product_carried from contain where barcode = ip_barcode;
    if product_carried >0 then leave sp_main; end if;
    
    delete from products where barcode = ip_barcode;
end //
delimiter ;

-- [20] remove_van()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a van from the system.  The removal can
occur if, and only if, the van is not carrying any products.*/
-- -----------------------------------------------------------------------------
drop procedure if exists remove_van;
delimiter //
create procedure remove_van (in ip_id varchar(40), in ip_tag integer)
sp_main: begin


    -- ensure that the van exists
    -- ensure that the van is not carrying any products
    
    declare van_exists int default 0;
    declare van_carrying_products int default 0;

    If ip_id is NULL then leave sp_main; 
    end if;

     If ip_tag is NULL then leave sp_main; 
     end if;


    select count(*) into van_exists from vans where id = ip_id and tag = ip_tag;
    if van_exists = 0 then leave sp_main; end if;
    
    select count(*) into van_carrying_products from contain where id = ip_id and tag = ip_tag;
    if van_carrying_products > 0 then leave sp_main; end if;
    
    delete from vans where id = ip_id and tag = ip_tag;
end //
delimiter ;

-- [21] remove_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a driver from the system.  The removal can
occur if, and only if, the driver is not controlling any vans.  
The driver's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_driver_role;
delimiter //
create procedure remove_driver_role (in ip_username varchar(40))
sp_main: begin


    -- ensure that the driver exists
    -- ensure that the driver is not controlling any vans
    -- remove all remaining information
    
    declare driver_exists int default 0;
    declare driver_driving_vans int default 0;

    If ip_username is NULL then leave sp_main; end if;
    
    select count(*) into driver_exists from drivers where username = ip_username;
    if driver_exists = 0 then leave sp_main; end if;
    
    select count(*) into driver_driving_vans from vans where driven_by = ip_username;
    if driver_driving_vans > 0 then leave sp_main; end if;
    
    delete from drivers where username = ip_username;
    
    delete from employees where username = ip_username;
    delete from users where username = ip_username;
end //
delimiter ;

-- [22] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
businesses for which they provide funds and the number of different places where
those businesses are located.  It also includes the highest and lowest ratings
for each of those businesses, as well as the total amount of debt based on the
monies spent purchasing products by all of those businesses. And if an owner
doesn't fund any businesses then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as

select 
	o.username,
    u.first_name,
    u.last_name,
    u.address,
    coalesce(count(DISTINCT f.business), 0) as num_businesses,
    coalesce(count(DISTINCT b.location), 0) as num_places,
    coalesce(max(b.rating), 0) as highs,
    coalesce(min(b.rating), 0) as lows,
    coalesce(sum(b.spent), 0) as debt
from
	business_owners o join users u on o.username = u.username
	left join fund f on o.username = f.username
	left join businesses b on f.business = b.long_name
group by
    o.username, u.first_name, u.last_name, u.address, u.birthdate;
    
    
-- [23] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, salary, hiring date and
experience level, along with license identifer and driving experience (if applicable,
'n/a' if not), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------
create or replace view display_employee_view as
select 
	e.username,
    e.taxID,
    e.salary,
    e.hired as hiring_date,
    e.experience as experience_level,
    coalesce(d.licenseID, 'n/a') as license_identifier,
    coalesce(d.successful_trips, 'n/a') as driving_experience,
    case
		when ds.manager is not null and ds.manager = e.username then 'yes'
        else 'no'
	end as manager_status
from employees e
	left join drivers d on e.username = d.username
    left join delivery_services ds on e.username = ds.manager;

-- [24] display_driver_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a driver.
For each driver, it includes the username, licenseID and drivering experience, along
with the number of vans that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_driver_view as
select 
	d.username,
    d.licenseID,
    d.successful_trips,
    count(v.driven_by) as num_vans
from drivers d
	left join vans v on d.username = v.driven_by
	group by d.username, d.licenseID, d.successful_trips;

-- [25] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
name of the business or service at that location, the number of vans as well as 
the identifiers of the vans at the location (sorted by the tag), and both the 
total and remaining capacity at the location. */
-- -----------------------------------------------------------------------------
create or replace view display_location_view as
select 
    l.label,
    coalesce(b.long_name, s.long_name) as long_name,
    l.x_coord,
    l.y_coord,
    l.space,
    (select count(*) from vans where label = located_at) as num_vans,
    group_concat(v.id,v.tag) AS van_ids,
    (l.space- (select count(*) from vans where label = located_at)) as remaining_capacity
from 
    locations l left join businesses b on l.label = b.location
    left join delivery_services s on l.label = s.home_base
    join vans v on l.label = v.located_at
group by
    l.label, l.x_coord, l.y_coord, l.space, b.long_name, s.long_name;
    

-- [26] display_product_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the products.
For each product that is being carried by at least one van, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the product is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_product_view as
select 
    p.iname as product_name,
    v.located_at as location,
    sum(c.quantity) as amount_available,
    min(c.price) as low_price,
    max(c.price) as high_price
from products p
inner join contain c on p.barcode = c.barcode
inner join vans v on c.id = v.id and c.tag = v.tag
group by p.iname, v.located_at;

-- [27] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the vans.  It must also include the number
of unique products along with the total cost and weight of those products being
carried by the vans. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
with rev_table as (select id, SUM(sales) as revenue from vans v group by id)
select 
    s.id as id,
    s.long_name as long_name,
    s.home_base as home_base,
    s.manager,
    ifnull(revenue, 0) as revenue,
    ifnull(count(distinct c.barcode), 0) as products_carried,
    ifnull(sum(quantity * price), 0) as cost_carried,
    ifnull(sum(quantity * weight), 0) as weight_carried
from 
    delivery_services s left join vans v on s.id = v.id
    left join contain c on v.id = c.id and v.tag = c.tag
    left join products p on c.barcode = p.barcode
    left join rev_table r on s.id = r.id
group by 
    s.id, s.long_name, s.home_base, s.manager;
-- CALL load_van('mbm', 1, 'hm_5E7L23M', 5, 29);
-- CALL load_van('lcc', 1, 'pt_16WEF6M', 1, 20);
