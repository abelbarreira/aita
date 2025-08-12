# API Analysis

This is a short document gathering information about the different APIs is possible to use to get access to the Flights and Hotels information.

For the moment, let's start with Flights info.

## RapidAPI - Flights

- [Booking.com](https://rapidapi.com/DataCrawler/api/booking-com15)
  - Free:
    - 50 / m
    - 1000 request per hour
  - Pro: 9$ / m
    - 35,000 /m
    - +0.0015
  - [GET Search Flights](https://rapidapi.com/DataCrawler/api/booking-com15/playground/apiendpoint_5b86beca-5c23-45ea-9682-4c5fa4075454)
    - 11 Params: fromID, toID, departDate, returnDate, stops...
  - [GET Get Min Price](https://rapidapi.com/DataCrawler/api/booking-com15/playground/apiendpoint_5bd85d7f-ceac-479a-adbe-fedf008679e9)
    - 6 Params: fromID, toID, departDate, returnDate, cabinClass, currency_code
  - [GET Get Flight Details](https://rapidapi.com/DataCrawler/api/booking-com15/playground/apiendpoint_c78629cf-8b49-4acd-9eee-29e59706e976)
    - 2 Params: token, currency_code
- [Booking.com](https://rapidapi.com/ntd119/api/booking-com18)
  - Free:
    - 530 / m
    - 1000 request per hour
  - Pro: 15$ / m
    - 40,500 /m
    - Hard Limit
- [Google Flights](https://rapidapi.com/DataCrawler/api/google-flights2)
  - Free
    - 150 / m
    - 1000 request per hour
  - Pro: 13$
    - 40.000 / m
- [Google Flights](https://rapidapi.com/things4u-api4upro/api/google-flights4)
  - Free
    - 100 / m
    - 1000 request per hour
  - Pro: 15$
    - 35.000 / m
    - +0.0009
  - [GET flights/search-roundtrip](https://rapidapi.com/things4u-api4upro/api/google-flights4/playground/apiendpoint_95117ab9-4028-4b77-902e-0484a47c18be)
    - 22 Params
