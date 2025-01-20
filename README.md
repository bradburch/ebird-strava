# eBird-Strava

This is a fun little project to update any coresponding Strava activity with the birds seen in an eBird checklist. 

## Setup

You will need [Docker](https://www.docker.com/) installed. 

You will need to create a `config.ini` with the following: 
```
[ebird]
ebird_api_token = 
ebird_profile_id = 

[strava]
strava_refresh_token = 
strava_access_token = 
strava_client_id = 
strava_client_secret = 
```

You can request an ebird API token here: https://ebird.org/data/download

You can request a Strava API token here: https://developers.strava.com/docs/


Your ebird profile id can be found as the item directly after `/profile/` in your profile URL. Please note that your profile must be public. 

Example: https://ebird.org/profile/**MzkyNjAwNA**

## Running

To run, choose a docker image name and build a docker image with `docker build -t <DOCKER-IMAGE-NAME> .`

Run the docker image with `docker run <DOCKER-IMAGE-NAME>`

You should see a successful message with the birds you saw and the Strava activity that was updated. 