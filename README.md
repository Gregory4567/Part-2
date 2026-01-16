# Part-2

This workflow automation script processes fake Netflix user data. It reads the netflix_users.csv file, checks for data completeness and validity, and creates a new csv file which includes valid users engagement statuses and the number of days since they last logged in.The engagement status is based on whether a user's hours watched in the last month are above a certain threshold that aligns with their subscription plan.

Dataset used: netflix_users.csv

Columns<br>
User_ID – Unique identifier for each user<br>
Name – Randomly generated name<br>
Age – Age of the user (13 to 80)<br>
Country – User’s country (randomly chosen from 10 options)<br>
Subscription_Type – Type of Netflix plan (Basic, Standard, Premium)<br>
Watch_Time_Hours – Total hours watched in the last month<br>
Favorite_Genre – User’s preferred genre<br>
Last_Login – Last recorded login date<br>
