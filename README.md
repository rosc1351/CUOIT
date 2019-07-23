# OIT Room Schedule Tool

## Abstract

OIT must check each room for issues periodically. This project develops an organized method of checking rooms, ensuring none get missed. This implementation hosts a web application using Express server in NodeJS. The application takes in daily bookings via excel file upload in addition to fetching live data via Google Sheets API whenever the 'getSheets' button is pressed. The application processes and presents the collected data in a table that is searchable and sortable. When a room is checked by submitting a response to google sheets, the room will automatically be removed from the list until it needs to be checked again.

![Website](/Present/OIT-Display.png)
