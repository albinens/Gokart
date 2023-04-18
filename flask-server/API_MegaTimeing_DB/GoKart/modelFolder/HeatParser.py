import json


class HeatParser():
    @classmethod
    def parse(cls, connection) -> list:
        heatData = connection.json()["data"]
        lapsData = connection.json()["laps"]
        racerList = cls.createRacerList(heatData)
        racerIds = cls.createRacerIds(heatData)
        lapTimeList = cls.createLapTimeList(lapsData, racerIds)
        cls.addLapTimesToRacerList(racerList, lapTimeList)
        return racerList

    @classmethod
    def createRacerIds(cls, data) -> list:
        racerIds = []
        activitysData = data["activitys"]
        for activity in activitysData:
            participantsData = activity["activity"]
            for participant in participantsData["participants"]:
                racerIds.append(participant["p"]["id"])
        return racerIds

    @classmethod
    def createRacerList(cls, data) -> list:
        racerList = []

        # finePrint(data)
        activitysData = data["activitys"]
        for activity in activitysData:

            participantsData = activity["activity"]
            date = participantsData["date"]
            for participant in participantsData["participants"]:
                racerDict = cls.createRacerDict(date, participant)
                racerList.append(racerDict)

        return racerList

    @classmethod
    def createLapTimeList(cls, lapsData, racerIds):
        lapTimeList = []
        activitys = lapsData["activitys"]

        for x in activitys:

            participants = x["activity"]["participants"]

            for participant in participants:

                laps = participant["p"]["laps"]
                if participant["p"]["id"] in racerIds:
                    for lap in laps:
                        lapTimeList.append(int(lap[2])/1000)

        # return lapsData
        # Hittade ett fel, den returnerade en variabel som användes i APIt för att hämta data.
        return lapTimeList

    @classmethod
    def addLapTimesToRacerList(cls, racerList, lapTimeList) -> None:
        i = -1  # I listan som innehåller alla varv, "initieras" en ny förare då varvtiden = "0.0" . Därav börjar vi med i som -1
        antalLaps = 0
        lastLap = 1

        for lapTime in lapTimeList:
            if lapTime == 0.0:
                if lastLap == 0.0 and lapTime == 0.0:
                    i -= 1
                i += 1
                lastLap = lapTime

            if lapTime != 0.0:
                racerList[i]["laptimes"].append(lapTime)
                lastLap = lapTime
                antalLaps += 1
        # HÄR ÄR RACERLIST KLAR.

    @classmethod
    def createRacerDict(cls, date, participant):
        racerDict = {'id': 0, 'nr': 0,
                     'name': "name", "laptimes": [], "date": 0}
        if participant["p"]["fname"] == None:
            racerDict["name"] = participant["p"]["nr"]

        else:
            # finePrint(participant["p"])
            racerDict["name"] = participant["p"]["fname"]

        racerDict["id"] = participant["p"]["id"]
        racerDict["nr"] = participant["p"]["nr"]
        racerDict["date"] = date

        return racerDict
