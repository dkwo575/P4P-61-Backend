# Function to update or add the event text by farm ID, building ID, and event date
def update_or_add_eventText(data, farm_id, building_id, event_date, new_text):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for event in building["events"]:
                        if event["date"] == event_date:
                            event["text"] = new_text
                            return True
                    # If event date not found, add a new event
                    building["events"].append({
                        "date": event_date,
                        "text": new_text
                    })
                    return True
            # If building ID not found, add a new building with the event
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [
                    {
                        "date": event_date,
                        "text": new_text
                    }
                ],
                "environment": [],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and event
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [
                    {
                        "date": event_date,
                        "text": new_text
                    }
                ],
                "environment": [],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure
