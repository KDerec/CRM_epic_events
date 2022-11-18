<div id="top"></div>


<!-- PROJECT LOGO -->
<br/>
<div align="center">
  <a href="https://github.com/KDerec/CRM_epic_events/blob/master/images/logo.png">
    <img src="images/logo.png" alt="Logo" width="160" height="80">
  </a>

<h3 align="center">Develop a secure CRM with Django & Django REST</h3>

  <p align="center">
    This student project is the #9 of my training (<i>IN PROGRESS...</i>).<br>You can follow the previous one <a href="https://github.com/KDerec/Python_Testing">here</a>.
  </p>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
### 🌱 Developped skills
* Develop the architecture of a relational database with domain-driven design approach.
* Implement a secure database with Django ORM and PostgreSQL.
### 📖 Scenario
I work as a software developer at **Epic Events**, an event management and consulting company that caters to the needs of startups wanting to throw "epic parties" 🎉.  
Internally, most of my work consists of managing the company's **outdated customer relationship management** (CRM) software, which tracks all clients and events.

🌄 One morning, I get an email from my manager:  
"The vendor we were using for our CRM has been **hacked** ! What's worse, the integrity of some of Epic Events' **customer information** has been **compromised**, which is a serious problem for the company, as many customers are considering other providers ⚠."  

<u>Solution:</u> **Develop a secure CRM system in-house** and I'm responsible for the first version.
### 🚧 🚀 Project goal & deliverable
Design an **entity-relationship diagram** (ERD) with domain-driven design (DDD) approach and develop the corresponding **Django application** with a **PostgreSQL** database.

The Django application must provide a set of secure API endpoints using the **Django REST framework** to allow **CRUD** operations (create, read, update and delete) applied to the various **CRM objects**.  

✍🏻 Create a **simple front-end interface** using the Django administration site, which will allow authorized users to manage the application, access all models and check the database configuration.  

For security:
* Prevent SQL injection. 
* Guarantee authentication.
* Security misconfigurations.
* Logging and monitoring.  

**Test** the application's **API** endpoints with **Postman**.

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With
* [Python 3.9](https://www.python.org/)
* [Django 4.1](https://www.djangoproject.com/)
* [Django REST 3.14](https://www.django-rest-framework.org/)
* [PostgreSQL 15](https://www.postgresql.org/)
* [Postman](https://www.postman.com/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation
1. <a href="#python-installation">Install Python</a> ;
2. Clone the project in desired directory ;
   ```sh
   git clone https://github.com/KDerec/CRM_epic_events.git
   ```
3. Change directory to project folder ;
   ```sh
   cd path/to/CRM_epic_events
   ```
4. Create a virtual environnement *(More detail to [Creating a virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment))* ;
    * For Windows :
      ```sh
      python -m venv env
      ```
    * For Linux :
      ```sh
      python3 -m venv env
      ```
5. Activate the virtual environment ;
    * For Windows :
      ```sh
      .\env\Scripts\activate
      ```
    * For Linux :
      ```sh
      source env/bin/activate
      ```
6. Install package of requirements.txt ;
   ```sh
   pip install -r requirements.txt
   ```
7. 


<p align="right">(<a href="#top">back to top</a>)</p>


#### Python installation
1. Install Python. If you are using Linux or macOS, it should be available on your system already. If you are a Windows user, you can get an installer from the Python homepage and follow the instructions to install it:
   - Go to [python.org](https://www.python.org/)
   - Under the Download section, click the link for Python "3.xxx".
   - At the bottom of the page, click the Windows Installer link to download the installer file.
   - When it has downloaded, run it.
   - On the first installer page, make sure you check the "Add Python 3.xxx to PATH" checkbox.
   - Click Install, then click Close when the installation has finished.

2. Open your command prompt (Windows) / terminal (macOS/ Linux). To check if Python is installed, enter the following command (this should return a version number.):
   ``` sh
   python -V
   # If the above fails, try:
   python3 -V
   # Or, if the "py" command is available, try:
   py -V
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact
Kévin Dérécusson 👇🏻  
Email : kevin.derecusson@outlook.fr  
LinkedIn : https://www.linkedin.com/in/kevin-derecusson/  

<p align="right">(<a href="#top">back to top</a>)</p>


<i>This student project is the #9 of my training.<br>You can follow the previous one <a href="https://github.com/KDerec/Python_Testing">here</a>.</i>
