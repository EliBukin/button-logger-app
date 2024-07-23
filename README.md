# Medication Consumption Logger

**Current Version: 1.1.1**

A Flask-based web application designed to help users track their medication intake and receive timely reminders.

## Key Features:

1. **Medication Logging**: Users can log their medication consumption with a simple button press.

2. **Customizable Reminder System**: 
   - Set two daily medication times
   - Configure up to three reminder intervals
   - Receive email reminders if medication is not logged on time

3. **Email Notifications**: 
   - Optional email confirmation when medication is logged
   - Configurable email settings for sender and recipient

4. **User-Friendly Interface**:
   - Responsive design for both desktop and mobile devices
   - Easy-to-use buttons and switches for quick interactions
   - Tabbed interface for separating time and email configurations

5. **Logging History**: View the last 5 medication log entries directly on the main page

6. **Flexible Configuration**:
   - Toggle email functionality on/off
   - Customize reminder intervals and medication times
   - Update email settings through the web interface

7. **Security**: 
   - Configurations stored in a JSON file
   - Passwords and sensitive information handled securely

8. **Background Processing**: 
   - Utilizes threading for sending reminders without blocking the main application

This application is perfect for individuals who need assistance in maintaining a consistent medication schedule. It combines ease of use with powerful customization options to adapt to various user needs.

## Tech Stack:
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Email: SMTP with SSL
- Configuration: JSON
- Logging: Python's built-in logging module

## Deployment:
Designed to be easily deployable in containerized environments, with configurations and logs persisted in a dedicated data directory.

## Version History:
- 1.1.1: added email notifications and configurable config file from the UI
- 0.2.1: improved UI and functionality
- 0.1.1: Initial release with core functionality