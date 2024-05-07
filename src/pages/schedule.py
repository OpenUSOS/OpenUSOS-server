import os
import json
from datetime import datetime, timedelta

#nazwa przedmiotu, czas trwania, sala, prowadzacy, data
class Schedule():

    def __init__(self, caller):
        self.caller = caller

    def get_schedule(self, date_from, num_of_days):
        activities = []
        remaining_days = int (num_of_days)
        
        while remaining_days > 0:
            # Calculate the number of days to fetch in this call, maximum 7
            days_to_fetch = min(remaining_days, 7)
            
            # Fetch activities for the current batch of days
            batch_activities = self.caller.api.get('services/tt/student', start=date_from, days=days_to_fetch, fields="start_time|end_time|name|building_name|room_number")
            
            # Append the activities to the list
            for batch_activity in batch_activities:
                activity = {}
                activity["start_time"] = batch_activity["start_time"]
                activity["end_time"] = batch_activity["end_time"]
                activity["name"] = batch_activity["name"]
                #can be null:
                if 'building_name' in batch_activity:
                    activity["building_name"] = batch_activity["building_name"]
                else:
                    activity["building_name"] = "-"
                
                if 'room_number' in batch_activity:
                    activity["room_number"] = batch_activity["room_number"]
                else:
                    activity["room_number"] = "-"
                activities.append(activity)
            
            # Update remaining days and date_from for the next call
            remaining_days -= days_to_fetch
            date_from = (datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=days_to_fetch)).strftime("%Y-%m-%d")
        json_string = json.dumps(activities)
        return json_string



