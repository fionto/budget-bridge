# The `datetime` module supplies classes for manipulating dates and times
# This line imports the datetime class from the datetime module. 
# The datetime class represents a specific date and time.
from datetime import datetime

date_string = "2025-12-21T13:05:33.120Z" # ISO 8601 format from wallet data

# Creating the date object using the class method .fromisoformat()
date_object = datetime.fromisoformat(date_string)

print(type(date_object)) # date_object is an instance of the datetime class

# extracting attributes
year = date_object.year
month = date_object.month
day = date_object.day

# checking types of the final variables
print(type(year))
print(type(month))
print(type(day)) 