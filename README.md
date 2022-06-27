# Beta Licensing Software

This project is a web based project management application which allows a non redundant and safe storage of licenses on an a cloud based storage system ( DBMS ). The project allows large scale companies maintaining / issuing licenses and even private organizations maintaining validity of said people to store, edit and maintain information for the same. The website allows users to login to check the status of their license where as registered license providers can login and issue new licenses, change the status of the license and even delete a license. It is designed to be used online via the website, and does not require any additional programs / prerequisite applications to be installed. Users must be registered on the platform by providing their email address and a username. This project uses strong encryption for both authentication as well as the storage of licenses to prevent leaks and to ensure security from attackers.

*Setup a virtual environment within the project folder*

- Setup virtual environment for the project with the simple python inbuilt command `python -m venv virt` [ This creates a virtual environment within our project folder ]

- Activate virtual environment by running this inbuilt command `source virt/scripts/activate` [ This activates the virtual environment for the project ]

- Install required dependancy by running a simple pip command `pip install -r requirements.txt` [ The requirements.txt file has been included in the repository for easy installation of required dependancy. Simply running this command will complete all dependancy installation within the virtual environment ]

- Setup flask environment by running these two commands `export FLASK_ENV=development` and `export FLASK_APP=main.py` [ This will set the environment for our flask application to execute ]

- Finally run the project on your localhost by running `flask run` [ This executes the project and the website will be online on localhost. ]
