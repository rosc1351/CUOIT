# OIT Room Schedule Tool

## Abstract

OIT must periodically check each room for issues and preventative maintenance. This project develops an algorithmic approach of checking rooms, ensuring none go unchecked for too long. This implementation hosts a web application using Express server in NodeJS running on an AWS EC2 linux compute unit. The application takes in daily bookings via excel file upload in addition to fetching live data via Google Sheets API whenever the 'getSheets' button is pressed. The application processes and presents the collected data in a table that is searchable and sortable. When a room is checked by submitting a response to google sheets, the room will automatically be removed from the list until it needs to be checked again.

![Website](/Present/OIT-Display.png)
