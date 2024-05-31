#################statement##################################

resource "confluent_flink_statement" "statement1" {
  statement  = "create table CustomerItinerary ( TRANSACTIONID bigint, CUSTOMERID bigint, FLIGHTNUMBER varchar, CONFIRMATIONNUMBER varchar, FROMAIRPORT varchar, TOAIRPORT varchar, DEPARTURETIME varchar, ARRIVALTIME varchar, FlightStatus varchar, BookingDate varchar, SeatNo varchar, BookingStatus varchar, BookingAmount bigint, PaymentStatus varchar, FIRSTNAME varchar, LASTNAME varchar, EMAIL varchar, PHONE varchar, GENDER varchar, ADDRESS varchar, MemberShipType varchar );"
  properties = {
    "sql.current-catalog"  = var.confluent_environment_display_name
    "sql.current-database" = var.confluent_kafka_cluster_display_name
  }

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_flink_statement" "statement2" {
  statement  = "insert into CustomerItinerary( TRANSACTIONID, CUSTOMERID, FLIGHTNUMBER, CONFIRMATIONNUMBER, FROMAIRPORT, TOAIRPORT, DEPARTURETIME, ARRIVALTIME, FlightStatus, BookingDate, SeatNo, BookingStatus, BookingAmount, PaymentStatus, FIRSTNAME, LASTNAME, EMAIL, PHONE, GENDER, ADDRESS, MemberShipType ) select TRANSACTIONID, FlightCustomerData.CUSTOMERID, FLIGHTNUMBER, CONFIRMATIONNUMBER, FROMAIRPORT, TOAIRPORT, DEPARTURETIME, ARRIVALTIME, FlightStatus, BookingDate, SeatNo, BookingStatus, BookingAmount, PaymentStatus, FIRSTNAME, LASTNAME, EMAIL, PHONE, GENDER, ADDRESS, MemberShipType from FlightCustomerData inner join FlightItinerariesData on FlightCustomerData.CUSTOMERID = FlightItinerariesData.CUSTOMERID;"
  properties = {
    "sql.current-catalog"  = var.confluent_environment_display_name
    "sql.current-database" = var.confluent_kafka_cluster_display_name
  }

  lifecycle {
    prevent_destroy = false
  }
  depends_on = [
    resource.confluent_flink_statement.statement1,
  ]
}

resource "confluent_flink_statement" "statement3" {
 statement  = "create table FlightData ( transaction_id bigint, customer_id bigint, flight_number varchar, confirmation_number varchar, source_code varchar, destination_code varchar, departure_time varchar, arrival_time varchar, gate bigint, flight_status varchar, booking_date varchar, seat_number varchar, booking_status varchar, booking_amount bigint, payment_status varchar, terminal bigint, first_name varchar, last_name varchar, email varchar, phone varchar, gender varchar, address varchar, membership_type varchar );"
  properties = {
    "sql.current-catalog"  = var.confluent_environment_display_name
    "sql.current-database" = var.confluent_kafka_cluster_display_name
  }

  lifecycle {
    prevent_destroy = false
  }
   depends_on = [
    resource.confluent_flink_statement.statement2,
  ]
}

resource "confluent_flink_statement" "statement4" {
  statement  = "insert into FlightData ( transaction_id, customer_id, flight_number, confirmation_number, source_code, destination_code, departure_time, arrival_time, gate, flight_status, booking_date, seat_number, booking_status, booking_amount, payment_status, terminal, first_name, last_name, email, phone, gender, address, membership_type ) select TRANSACTIONID as transaction_id, CUSTOMERID as customer_id, CustomerItinerary.FLIGHTNUMBER as flight_number, CONFIRMATIONNUMBER as confirmation_number, FROMAIRPORT as source_code, TOAIRPORT as destination_code, DEPARTURETIME as departure_time, ARRIVALTIME as arrival_time, FlightGateData.GATE as gate, FlightStatus as flight_status, BookingDate as booking_date, SeatNo as seat_number, BookingStatus as booking_status, BookingAmount as booking_amount, PaymentStatus as payment_status, FlightGateData.TERMINAL as terminal, FIRSTNAME as first_name, LASTNAME as last_name, EMAIL as email, PHONE as phone, GENDER as gender, ADDRESS as address, MemberShipType as membership_type from CustomerItinerary inner join FlightGateData on CustomerItinerary.FLIGHTNUMBER = FlightGateData.FLIGHTNUMBER;"
  properties = {
    "sql.current-catalog"  = var.confluent_environment_display_name
    "sql.current-database" = var.confluent_kafka_cluster_display_name
  }

  lifecycle {
    prevent_destroy = false
  }
   depends_on = [
    resource.confluent_flink_statement.statement3,
  ]
}