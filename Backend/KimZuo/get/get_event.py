# Function to update or add the event text by farm ID, building ID, and event date
def get_eventText(data, farm_id, building_id, event_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for event in building["events"]:
                        if event["date"] == event_date:
                            text = event["text"]
                            return text
                    # If event date not found, return error
                    raise ValueError("Event Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")

