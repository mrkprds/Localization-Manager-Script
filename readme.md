Localization Manager Script
===================

Originally a fork of [BdR76's](https://github.com/BdR76) repo, [Manage Translation](https://github.com/BdR76/Manage-translations)

It deviated enough to a point that it was way too different from the original project but I'd still like to credit him for the idea for it.

This project is essentially a script when run, will generate it into the designated localization file on a user's Google Drive. A Google Spreadsheet would be set up by the user which it would base of the list of translation strings from. 

Advantage of this is that a translator and developers on multiple platform can share one source of truth for the list of their localizable strings and can easily be shared with others as the spreadsheet would coming from Google Sheets.

The project is still currently in progress and generates a translation file for iOS using their new .xcstrings format. (Android implementation is in the works.)

It contains a python script that authenticates with the Google Sheets and Google Drive APIs, it also uses AppScript, gSpread, and pandas for navigating around and parsing spreadsheet. 


How to use
----------
TODO

Sheet content
-------------
TODO

Export preview
--------------
TODO
