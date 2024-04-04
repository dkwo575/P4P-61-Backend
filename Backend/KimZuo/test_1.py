import json
import os

database_directory = os.getcwd() + "\database\\farm_data.json"

# Load the data from the JSON file
with open(database_directory, "r") as infile:
    loaded_data = json.load(infile)

# Manipulate the loaded data as needed
# For example, let's change the farm name of the first farm to "Updated Farm 1"
loaded_data[0]["farmName"] = "Updated Farm 1"

# Add a new event to the first building of the first farm
loaded_data[0]["buildings"][0]["events"].append({"date": "2023-07-20", "text": "Added new event"})

# Write the modified data back to the JSON file
with open("farm_data.json", "w") as outfile:
    json.dump(loaded_data, outfile, indent=4)

print("Data successfully loaded, modified, and stored back in 'farm_data.json' file.")
