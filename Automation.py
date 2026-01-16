from datetime import datetime, date
import csv

def load_netflix_data(filename):
    users_list = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users_list.append(row)
        print(f"Successfully loaded data of {len(users_list)} users.")
        return users_list
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    
def enrich_netflix_data(data):
    """
    Processes user data to calculate days since last login,
    and assigns an engagment status based on subscription plan and hours watched in the last month.
    Prints a dictionary containing the Users IDs with invalid data and a description.
    Returns a list of enriched user dictionaries showing User ID, engagment status and days inactive.
    """
    if not data:
        return []

    invalid_users = {}
    #today = datetime.now().date()
    #I am using the date below as the 'current date' as the fake data I'm using does not have logins after this date.
    today = date(2025, 3, 25)
    enriched_users = []

    MANDATORY_FIELDS = ["User_ID", "Subscription_Type", "Watch_Time_Hours", "Last_Login"]
    PLAN_THRESHOLDS = {"Premium": 100, "Standard": 50, "Basic": 25}

    for user in data:
        #Check all mandatory fields are present
        user_id = user.get("User_ID") or "UnknownID"
        missing_fields = [field for field in MANDATORY_FIELDS if not user.get(field)]
        if missing_fields:
            invalid_users[user_id] = f"Missing: {', '.join(missing_fields)}"
            continue

        #Check that subscription plan is valid and present within the plan thresholds dictionary
        threshold = PLAN_THRESHOLDS.get(user["Subscription_Type"], 0)
        if threshold == 0:
            invalid_users[user_id] = "Invalid Subscription type"
            continue

        #Assign an engagment status to the user, and calculate days since login.
        try:
            watch_time = float(user["Watch_Time_Hours"])
            engagement_status = "Under-utilising" if watch_time < threshold else "Active"

            last_login_dt = datetime.strptime(user["Last_Login"], "%Y-%m-%d").date()
            days_since_login = (today - last_login_dt).days
        except ValueError:
            invalid_users[user_id] = "Invalid data format"
            continue
        
        enriched_users.append({
                "User_ID": user_id,
                "Engagement_Status": engagement_status,
                "Days_Inactive": days_since_login
            })
        
    print(f"{len(invalid_users)} User IDs with invalid data: {invalid_users}")

    return enriched_users

def export_to_csv(data, filename):
    if not data:
        print("No data to export.")
        return
    
    try:
        headers = data[0].keys()
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)  
        print(f"Successfully exported {len(data)} records to {filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")

users_data = load_netflix_data('netflix_users.csv')
results = enrich_netflix_data(users_data)
export_to_csv(results, "enriched_netflix_data.csv")

"""
This workflow could be extended using an AI API by using the AI to generate a Film or TV suggestion for users
who are deemed to be under-utilising their subscription and are at risk of cancelling.
The Age, Country, and Favourite Genre fields could be used in an AI tool to output an appropriate user-specific suggestion.
"""