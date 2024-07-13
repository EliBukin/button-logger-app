Button Logger App - app version 1.0.3


This application is a button logger system with email reminders. Here's a high-level description of its purpose and operation:

Purpose:
1. To log button pushes at specific times
2. To send email reminders if the button is not pushed
3. To allow configuration of email settings and reminder times

Operation:

1. Button Logging:
   - Users can push a virtual button through a web interface.
   - Each button push is logged with a timestamp.
   - Optionally, an email confirmation can be sent for each button push.

2. Reminder System:
   - The app checks for button pushes at two configurable time slots each day.
   - If a button push is missed, the system sends a series of reminder emails at specified intervals.

3. Web Interface:
   - Provides a simple UI for pushing the button and viewing recent button pushes.
   - Allows users to configure email settings and reminder times.

4. Configuration:
   - Email settings: Sender email, recipient email, and password can be set.
   - Time settings: Two daily time slots for checking button pushes.
   - Reminder intervals: Three configurable intervals for sending reminder emails.

5. Logging:
   - Maintains a log file of button pushes.
   - Displays the last 5 button pushes on the web interface.

6. Background Processes:
   - Continuously checks the current time against configured time slots.
   - Triggers reminder emails based on configured intervals if a button push is missed.

This application could be useful in scenarios where regular actions need to be logged and tracked, with an automated reminder system in place. It's designed to be simple to use while offering flexibility in its configuration.
