import datetime
import json

from collections import defaultdict


DATE_FORMAT = "%Y-%m-%d"


def get_birthdays_per_week(
        users_data: dict,
) -> dict:
    """This function will return dictionary with all users that have birthday in following week.

    Args:
        users_data: dict where key is user full name, and value is his birthday in following format "%Y-%m-%d".

    Returns:
        A dictionary where key is week day and value is list of user full names.
    """
    # Initial values and consts
    result = defaultdict(list)
    next_monday_date = (
        datetime.datetime.today().date() +
        datetime.timedelta(
            days=(7 - datetime.datetime.today().date().weekday()) % 7
        )
    )

    for user, birthday_str in users_data.items():
        birthday_date = (
            datetime.datetime.strptime(
                birthday_str,
                DATE_FORMAT
            ).date()
        )
        birthday_date = birthday_date.replace(year=next_monday_date.year)

        # Check if weekday is Sun or Sat
        if birthday_date.weekday() >= 5:
            birthday_date += datetime.timedelta(days=(7 - birthday_date.weekday()) % 7)

        # Advance by one year if birthday already passed
        if next_monday_date > birthday_date:
            birthday_date = birthday_date.replace(year=next_monday_date.year+1)

        # If birthday is within the week, add to result
        if (birthday_date - next_monday_date).days < 7:
            result[birthday_date.strftime("%A")].append(user)

    for week_day, users in result.items():
        print(f"{week_day}: {', '.join(users)}")

    return result


if __name__ == "__main__":
    # For demo, dummy data is stored under users.json file.
    with open("users.json", "r") as json_input:
        users_dict = json.load(json_input)

    users_bd = get_birthdays_per_week(users_data=users_dict)
