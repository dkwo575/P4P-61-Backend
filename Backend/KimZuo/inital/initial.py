import json
import os


def inital_farm(database_directory):
    # Database structure from data.ts (Frontend)
    data = [
        {
            "id": 0,
            "farmName": "",
            "buildings": [
                {
                    "id": 0,
                    "buildingName": "",
                    "events": [
                        # {"date": "2023-07-10", "text": "Changed light level"},
                        # {"date": "2023-07-15", "text": "Added fertilizer"}
                    ],
                    "environment": [
                        # {"date": "2023-03-12", "temperature": 22.7, "fluorescents": 7041, "co2Concentration": 754,
                        #  "irrigation": 2.0},
                        # {"date": "2023-03-13", "temperature": 22.6, "fluorescents": 6992, "co2Concentration": 754,
                        #  "irrigation": 2.1},
                        # # More environment data...
                    ],
                    "data": [
                        # {"date": "2023-03-12", "area": 613, "fruitlets": 0, "height": 192, "leaves": 5, "volume": 505,
                        #  "width": 46},
                        # {"date": "2023-03-13", "area": 616, "fruitlets": 0, "height": 205, "leaves": 6, "volume": 495,
                        #  "width": 54},
                        # # More data...
                    ],
                    "plots": [
                        {
                            "id": 0,
                            "plotName": "",
                            "data": [
                                # {
                                #     "date": "2023-03-12",
                                #     "area": 602,
                                #     "fruitlets": 0,
                                #     "height": 198,
                                #     "leaves": 5,
                                #     "volume": 520,
                                #     "width": 50,
                                # }
                            ]
                        },
                        # More plots...
                    ]
                },
                # More buildings...
            ]
        },
        # More farms...
    ]

    # Write data to a text file in JSON format
    with open(database_directory, "w") as outfile:
        json.dump(data, outfile, indent=4)

    print("Data successfully stored in %s file." % database_directory)
