
# Divar crawler

This project is designed as an API with the goal of crawling phone numbers from the website "divar". It receives three parameters: `city` (the city to search posters in), `stext` (the search parameter), and `scount` (the number of posters to check for their phone numbers).

## Prerequisites

Before running the project, you need to follow these steps:

1. Download and install a ChromeDriver that matches your Chrome version and operating system.

2. Open the `chrome://version` link in your Chrome browser, find the **Profile Path**, and make a copy of it to a desired location on your system.

3. Set the `PROFILE_PATH` variable in `settings.py` (line 132) to the directory where you placed the copied version of your profile path.

4. Set the `FIRST_TIME_SETUP` variable in `settings.py` (line 130) to `True`. This will open a web browser and allow you to log in to 'divar' using your phone number and OTP. This process only needs to be done the first time you run the project. After successfully logging in, close the Selenium browser window and set the `FIRST_TIME_SETUP` variable to `False`.

## Setup

```
# do this once
python3 -m venv .venv

source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# do this once
pip install -r requirements.txt

# run migrations
python manage.py migrate

#run server
python manage.py runserver
```

## Usage

To use the API, send a POST request to the `/search` endpoint with the following JSON payload:

```json
{
 "city": "search city",
 "stext": "keyword to search",
 "scount": "number of posters to check for their phone numbers"
}
```
The successful response will be in the following format:
```json

{
  "success": "Crawled numbers: 7, button fails: 1, failed to crawl: 2"
}
```
-   `Crawled numbers`  indicates the count of successfully crawled phone numbers.
-   `button fails`  indicates the number of failures during clicking on the contact info button (this may happen a few times due to some reasons).
-   `failed to crawl`  indicates the number of posters whose phone numbers are hidden and could not be collected.

Please note that this project should be used only for legitimate business purposes and in compliance with applicable laws and regulations.

## Contributing
If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.
