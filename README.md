# Pass
Traditional point of sale software doesn't allow for custom institutional ID cards to be used as a payment method. But with Pass, you can easily parse employee and/or student ID cards and deduct directly from their outlined meal plans. This is especially useful for dining halls and cafeterias in both educational institutions and corporate offices.

![Front Page](https://user-images.githubusercontent.com/76973785/129935684-60411ea9-f541-423b-a83a-89597de794f8.png) ![Profile Page](https://user-images.githubusercontent.com/76973785/129937255-365ed5c3-287e-43b7-8dac-c84d4296d055.png)

## Quick Start
Connect your card reader, open Notepad, and scan a card. If the card starts with a `%` or `;`, your card is compatible with this software. Take note of any pattern that emerges from your cards. For example, Discover credit cards start with `%B6`, and are 16 digits long. Then, modify the `jquery.cardswipe.js` file so that the appropriate parser and parameters can be used. Additional instructions to set up the parser can be found in the `jquery.cardswipe.js` file.

Once you have successfully set up the parser, input the users' names, meal plan information, and ID number to the database by clicking "View Database" -> "Add User." You can also add the profile pics to the `static/pics` directory in JPEG or PNG format. Note that you must save the file as the respective user's ID number. 

*The default configuration resets the meal plan balance of all users on Sunday at 12:00AM. If you would like to disable this functionality, simply comment out the scheduler in `main.py`.

## License
Swipe away! Pass is free to use by anyone as detailed by the MIT License.
