# Overview
In order to gather data from the SmartFin, you must configure a way for the
Smartfin to upload data to a Google Spreadsheet.  You will need the following:
- Particle Console Access
- Google Spreadsheet
- Google Developer Console Access

# Configuration Instructions

Roughly, follow the steps in this guide: https://www.hackster.io/gusgonnet/pushing-data-to-google-docs-02f9c4

1.  Create a Google Sheet with the following columns:
    - `published_at`, corresponds to `PARTICLE_PUBLISHED_AT`
    - `event`, corresponds to `PARTICLE_EVENT_NAME`
    - `data`, corresponds to `PARTICLE_EVENT_VALUE`
    - `coreid`, corresponds to `PARTICLE_DEVICE_ID`
2.  From Google Sheets, click on `Tools` > `Script editor`
3.  Copy the code from `Code.gs` in this repository into the `Code.gs` file in the
    script editor.
4.  Click the `Save` icon to save `Code.gs`.
5.  Set the dropdown icon to execute the `setup` function.
6.  Click on the `Run` button to run the `setup` function.  This should show 
    `Running function setup` and then put up a dialog `Authorization Required`.
7.  Click `Review permissions`.
8.  Select the Google Account to authorize and click `Allow`.
9.  In the left bar, select the `Trigger` menu using the alarm clock icon.
10. Click the blue `Add Trigger` button.
11. Set function to `doPost`, deployment to `Head`, event source to `From spreadsheet`, event type to `On form submit`, and failure notification settings to `Notify me immediately`.
12. Follow the prompts to authorize the application.
13. Click on the blue `Deploy` button, then select `New deployment` from the 
    drop-down.
14. Under `Select type`, select `Web app` and `Library`.
15. Enter an appropriate description.
16. Set `Execute as` as yourself.
17. Set `Who has access` to `Anyone`.
18. Click `Deploy`.
19. Copy the web app URL.
20. Log in to your Particle Console (http://console.particle.io)
21. Click on `New Integration`
22. Select `Webhook`
23. Set `Event Name` to `Sfin-` to trigger on any event starting with `Sfin-`.
24. Set `URL` to the URL copied in step 15.
25. Set `Request Type` to `POST`.
26. Set `Request Format` to `Web Form`.
27. Set `Device` to `Any`.
28. Set `Status` to `Enabled`.
29. Click `Create Webhook`.
30. Data should now be able to flow from the Smartfins to the google sheet.
