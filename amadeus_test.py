from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='rE3dpAsJ6OAlUpa2Huh7t6QrJj2wvNSG',
    client_secret='JGonMzgZuO4J1yJU'
)

try:
    # Flight Inspiration Search
    response = amadeus.shopping.flight_destinations.get(origin='MAD')

    # This one breaks ------------------------------------
    # # Flight Cheapest Date Search
    # response1 = amadeus.shopping.flight_dates.get(
    #     origin='NYC',
    #     destination='MAD')

    # Flight Low-fare Search
    response2 = amadeus.shopping.flight_offers.get(
        origin='MAD',
        destination='NYC',
        departureDate='2019-08-01'
    )

    # Flight Checkin Links
    response3 = amadeus.reference_data.urls.checkin_links.get(
        airlineCode='BA')

    # Airline Code Lookup
    response4 = amadeus.reference_data.airlines.get(
        airlineCodes='U2'
    )

    # Airport and City Search (autocomplete)
    # Find all the cities and airports starting by 'LON'
    response5 = amadeus.reference_data.locations.get(
        keyword='LON',
        subType=Location.ANY
    )

    # Get a specific city or airport based on its id
    response6 = amadeus.reference_data.location('ALHR').get()

    Airport Nearest Relevant Airport (for London)
    response7 = amadeus.reference_data.locations.airports.get(
        longitude=0.1278,
        latitude=51.5074
    )

    # Flight Most Searched Destinations
    # Which were the most searched flight destinations from Madrid in August 2017?
    response8 = amadeus.travel.analytics.air_traffic.searched.get(
        originCityCode='MAD',
        marketCountryCode='ES',
        searchPeriod='2017-08'
    )

    # How many people in Spain searched for a trip from Madrid to New-York in September 2017?
    response9 = amadeus.travel.analytics.air_traffic.searched_by_destination.get(
        originCityCode='MAD',
        destinationCityCode='NYC',
        marketCountryCode='ES',
        searchPeriod='2017-08'
    )

    # Flight Most Booked Destinations
    response10 = amadeus.travel.analytics.air_traffic.booked.get(
        originCityCode='MAD',
        period='2017-08'
    )

    # Flight Most Traveled Destinations
    response11 = amadeus.travel.analytics.air_traffic.traveled.get(
        originCityCode='MAD',
        period='2017-01'
    )

    # Flight Busiest Travel Period
    response12 = amadeus.travel.analytics.air_traffic.busiest_period.get(
        cityCode='MAD',
        period='2017',
        direction='ARRIVING'
    )

    # Hotel Search
    # Get list of Hotels by city code
    response13 = amadeus.shopping.hotel_offers.get(
        cityCode = 'LON'
    )

    # Get list of offers for a specific hotel
    response14 = amadeus.shopping.hotel_offers_by_hotel.get(
        hotelId = 'IALONCHO'
    )

    # # This one breaks -----------------------------------
    # # Confirm the availability of a specific offer
    # response15 = amadeus.shopping.hotel_offer('D5BEE9D0D08B6678C2F5FAD910DC110BCDA187D21D4FCE68ED423426D0A246BB').get()



    # print("reponse: ")
    # print(response.data)
    # print("response1: ")
    # print(response1.body)
    # print(response1.result)
    # print(response.data)
    # print(response2.data)
    # print(response3.data)
    # print(response4.data)
    # print(response5.data)
    # print(response6.data)
    # print(response7.data)
    # print(response8.data)
    # print(response9.data)
    # print(response10.data)
    # print(response11.data)
    # print(response12.data)
    # print(response13.data)
    # print(response14.data)
    # print(response15.data)
except ResponseError as error:
    print(error)
