import requests


class ApiConnections():
    def __init__(self) -> None:  # type: ignore
        self.__connection = None

    def get_active_connection(self):  # -> requests.Response | None
        return self.__connection

    # Updates the active connection instance variable to list of dropin racers
    # Connection is based on which month of information is requested
    # Month must be from 1 to 12
    def connect_to_dropin(self, month: int) -> None:
        if month < 1 or month > 12:
            raise ValueError("Input must be from 1 to 12")
        else:
            self.__connection = requests.get(
                "https://megatiming.se/raas/server/portalfeed/publishedactivity.php?licens=164&history=true&year=2022&month="+str(month))

    # Updates the active connection instance variable to the dropin racer information
    # Connection is based on the id of the racer
    def connect_to_dropin_heat(self, dropInId: int) -> None:
        self.__connection = requests.get(
            "https://megatiming.se/raas/server/portalfeed/activitys.php?licens=164&id="+str(dropInId)+"&extra_path=laps_")

    def get_years(self):
        responseYear = requests.get(
            "https://megatiming.se/raas/server/portalfeed/publishedactivity.php?licens=164&history=true&year=0&month=0")
        years = []
        for year in responseYear.json()["publishedactivity"]:
            years.append(year["racedate"])
        return years

    def get_months(self):
        years = ApiConnections.get_years(self)
        responseMonth = requests.get(
            "https://megatiming.se/raas/server/portalfeed/publishedactivity.php?licens=164&history=true&year=2023&month=0")

        # print(json.dumps(responseMonth.json()["publishedactivity"],indent = 4, sort_keys = True))
        months = []
        for month in responseMonth.json()["publishedactivity"]:
            months.append(month["racedate"])

        return months

    def get_heatIDs(self, wantedMonths):
        # print(wantedMonths)
        apiIdDropIn = []  # Används för att få apilänken!
        for month in wantedMonths:
            print(month)
            responseDropIn = requests.get(
                "https://megatiming.se/raas/server/portalfeed/publishedactivity.php?licens=164&history=true&year=2023&month="+str(month))
            # print(json.dumps(responseDropIn.json()["publishedactivity"],indent = 4, sort_keys = True))

            for dropIn in responseDropIn.json()["publishedactivity"]:
                apiIdDropIn.append(dropIn["id"])
        return apiIdDropIn
