# gudlift-registration

1. Why
    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - Clone the repository:  
    <code>
    git clone https://github.com/GrolschSec/gudlft.git
    </code>
    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask --app server.py run</code> or <code>python -m flask --app server.py run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    - Each issues from the [original project](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues) have been corrected independently you can find them all on each bug/* branches.
    - The project include severals unit test and integration test but also some performance test that you can run just by typing <code>pytest</code>
    - You can see the testing coverage of the project using <code>coverage run -m pytest</code> and then generate a report using <code>coverage report</code> or <code>coverage html</code> to generate an html report.
    - The project also include perfomance tests using locust to run them you have to run server first as explained in the installation process then run <code>locust -f tests/performance/locustfile.py --headless -u 6 -r 1 --host http://localhost:5000/</code> to run it in headless mode or you can run <code>locust -f tests/performance/locustfile.py</code> without options and then connect from your navigator localhost port 8089 as this [link](http://localhost:8089/) and then configure and run you test from there.

