\# MyBank – Banking Management System



\## Project Overview

MyBank is a web-based Banking Management System developed using Python and Django. It provides users with a simple interface to manage their banking activities, perform money transfers, pay bills, and view transaction details.



\## Features



\- \*\*User Registration:\*\* New users can create an account.

\- \*\*User Login:\*\* Secure authentication for registered users.

\- \*\*Dashboard:\*\* View bank account details and balance.

\- \*\*Profile Management:\*\* View personal information.

\- \*\*Money Transfer:\*\* Transfer money between bank accounts.

\- \*\*Bill Payments:\*\* Make and manage bill payments.

\- \*\*Transaction History:\*\* View previous transactions.

\- \*\*Account Statement:\*\* Check transaction statements.

\- \*\*Complaint Management:\*\* Submit complaints and view complaint history.



\## Technologies Used



\- Python

\- Django

\- HTML

\- CSS

\- MySQL

\- Git and GitHub



\## Project Structure



```text

MyBank/

│

├── banking/

│   ├── migrations/

│   ├── static/

│   │   └── banking/

│   ├── templates/

│   │   └── banking/

│   ├── admin.py

│   ├── models.py

│   ├── urls.py

│   └── views.py

│

├── config/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

├── .gitignore

├── manage.py

└── README.md

```



\## Installation and Setup



1\. Clone the repository:



```bash

git clone https://github.com/gnaneshwaripathange/MyBank.git

```



2\. Navigate to the project folder:



```bash

cd MyBank

```



3\. Create a virtual environment:



```bash

python -m venv venv

```



4\. Activate the virtual environment (Windows):



```bash

venv\\Scripts\\activate

```



5\. Install the required packages:



```bash

pip install django python-dotenv mysql-connector-python

```



6\. Configure your database and environment variables in the project settings.



7\. Apply database migrations:



```bash

python manage.py migrate

```



8\. Start the development server:



```bash

python manage.py runserver

```



9\. Open your browser:



```text

http://127.0.0.1:8000/

```



\## Future Improvements



\- Add OTP-based authentication.

\- Improve security and validation.

\- Add downloadable transaction statements.

\- Improve the user interface.



\## Author



\*\*Gnaneshwari Pathange\*\*



GitHub: https://github.com/gnaneshwaripathange



\---



\*This project was developed as a learning project to understand Django web development and database integration.\*

