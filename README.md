# Flask-Capital-Time

To use the api you need to have the correct access token. This token is the same as the one used in class.

To get the time of a city you need to use the following endpoint:

```
http://ip-address:5001/time?city=CityName
```

For example, running this code locally and to get the time of London you need to use the following endpoint with the correct access token:

```
http://127.0.0.1:5001/time?city=London
```

To test the api on GCP you need to use this endpoint with the correct access token:

```
http://34.28.174.149:5001/time?city=London
```

Run client.py to test the api.

```
python client.py
```
