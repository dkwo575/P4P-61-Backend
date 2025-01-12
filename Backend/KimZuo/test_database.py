import json
import os

database_directory = database_directory = os.path.join(os.getcwd(), "database", "farm_data.json")

# Original data from data.ts
data = [
    {
        "id": 0,
        "farmName": "Farm 1",
        "buildings": [
            {
                "id": 0,
                "buildingName": "Building 1",
                "events": [
                    {"date": "2023-07-10", "text": "Changed light level"},
                    {"date": "2023-07-15", "text": "Added fertilizer"}
                ],
                "environment": [
                    {"date": "2023-03-12", "temperature": 22.7, "fluorescents": 7041, "co2Concentration": 754,
                     "irrigation": 2.0},
                    {"date": "2023-03-13", "temperature": 22.6, "fluorescents": 6992, "co2Concentration": 754,
                     "irrigation": 2.1},
                    # More environment data...
                ],
                "data": [
                    {"date": "2023-03-12", "area": 613, "fruitlets": 0, "height": 192, "leaves": 5, "volume": 505,
                     "width": 46},
                    {"date": "2023-03-13", "area": 616, "fruitlets": 0, "height": 205, "leaves": 11, "volume": 495,
                     "width": 54},
                    # More data...
                ],
                "plots": [
                    {
                        "id": 0,
                        "plotName": "Plot A1",
                        # Plot A1 data...
                        "data": [
                            {
                                "date": "2023-03-12",
                                "area": 602,
                                "fruitlets": 0,
                                "height": 198,
                                "leaves": 5,
                                "volume": 520,
                                "width": 50,
                            }
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

print("Data successfully stored in 'farm_data.json' file.")
print(type(data[0]))
print(data[0])
