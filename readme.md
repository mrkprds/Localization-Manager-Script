Localization Manager Script
===================

Originally a fork of [BdR76's](https://github.com/BdR76) repo, [Manage Translation](https://github.com/BdR76/Manage-translations)

It deviated enough to a point that it was way too different from the original project but I'd still like to credit him for the idea for it.

This project is a script that when run, will generate some localization file for iOS and Android based on a spreadsheet in Google Sheets. A Google Sheet would be set up by the user which would be the basis of the list of localizable strings.

The advantage of this is that a translator and developers on multiple platforms can share one source of truth for the list of their localizable strings and can easily be shared with others as the spreadsheet would come from Google Sheets.

The project is still in progress and generates a translation file for iOS using their new .xcstrings format. (Android implementation is in the works.)

It contains a Python script that authenticates with the Google Sheets and Google Drive APIs, it also uses AppScript, gSpread, and pandas for navigating around and parsing spreadsheets. 


How to use
----------
TODO

Sheet content
-------------
TODO

Export preview
--------------
TODO
