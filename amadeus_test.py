from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='c5OfvTrJnQAcRF40ATR2G0oPvdXkEkxv',
    client_secret='oVyXFiuu6BIkViyv'
)
def attempt():
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

        # Airport Nearest Relevant Airport (for London)
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
            hotelId = '90AE1201EC4A0F5AA3C28369FDFDBC6FA14B85FEA3DDBD22D1824DFEE4C11953'
        )

        # # This one breaks -----------------------------------
        # # Confirm the availability of a specific offer
        # response15 = amadeus.shopping.hotel_offer('D5BEE9D0D08B6678C2F5FAD910DC110BCDA187D21D4FCE68ED423426D0A246BB').get()

    except ResponseError as error:
        print(error)

def create_new():
    usr_city = input("Do you have a specific city (Y/N): ").upper()

    ## Select a City
    if (usr_city == "Y"):
        usr_city_specific = input("What is the city code: ").upper()
        response6 = amadeus.shopping.flight_offers.get(origin='MAD', destination='LON', departureDate='2019-08-01')

    else:
        # Here is a list of cities
        print("I cant help you then wtf\n")
        return 0

    ## Select a Airport
    usr_airport = input("Do you have a specific airport (Y/N): ").upper()
    if (usr_airport == "Y"):
        usr_airport_specific = input("What is the airport code: ").upper()
        airport_list

    ## Select a Hotel
    usr_hotel = input("Do you have a specific hotel (Y/N): ").upper()
    if (usr_hotel == "Y"):
        usr_hotel_specific = input("What is the hotel code: ").upper()
        hotel_info = amadeus.shopping.hotel_offers_by_hotel.get(
            hotelId = usr_hotel_specific
        )
        print("Here is the info on your hotel: \n")
        print(hotel_info)

    else:
        print("Here is a list of hotels for your target city: \n")
        hotel_list = amadeus.shopping.hotel_offers.get(
            cityCode = usr_city_specific
        )
        print(hotel_list.data[0]["hotel"]["name"])

def load_default():
    print("City: London\nAirport: \nHotel:HOTEL CAFE ROYAL")
    print("Flights from ___ to London")
    print("Hotel info: ")


def main():
    print("\n\nAmadeus_test demo initiated...\n")
    print("This is very basic so if you type random garbage itll break\n")
    print("Command List:\n\t'n': new vacation \n\t'l': load default vacation\n\t'a': check info on api")
    command = input("Please input a command: ").lower()
    exit = False
    while exit == False:
        if (command == "n"):
            create_new()
            exit = True
        elif (command == "l"):
            load_default()
            exit = True
        elif (command == "a"):
            attempt()
            exit = True
        else:
            print("Please try another command")
    print("\nDemo Over")
main()
