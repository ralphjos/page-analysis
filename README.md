Install Python 2.7, Pip, and Virtualenv based on your operating system: [Windows](http://docs.python-guide.org/en/latest/starting/install/win/), [OS X](http://docs.python-guide.org/en/latest/starting/install/osx/), or [Linux](http://docs.python-guide.org/en/latest/starting/install/linux/).

Also download MongoDB (I used version 3.2).  You will need to run it locally because the application uses a local database.  

Create a new virtual environment for the application:
```bash
virtualenv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```

Run the following command to download the Python libraries used:
```
pip install -r requirements.txt
```

Run MongoDB in the background before starting the application.

```
mongod
```

In lines 10 and 11 of ```main.py```, add the app ID and app key used for the Aylien client, then run the command below to run the application:

```
python main.py
```

Once you have everything running, you can try sending GET and POST requests to 127.0.0.1/extract with the following params:

```
url : a valid URL
callback (for POST only) : a callback URL where results of the extraction will get POST-ed to
