# OSRM (Open Source Routing Machine) Client
## The problem:
You have dataset of 2mln rows of route data (point[x,y]) and you need calculate the time for all routes. No one famous api (Yandex api, 2Gis api) don't give free access to make so huge requests.

## Solution:
OSRM Client!

### Tips:
- 2 requests per second. I tried to raise more, but that is max speed.
- You may split input dataset to N equal parts and run the code on cloud machines just with change the `SOURCE_FILENAME` in `main.py`.
- F.e.: I have splitted the input dataset with 2mln points for 10 parts with `filemanager.py`, created 10 cloud servers and decreased the wait time from 10 days to 1 day :)