# LABI-Logger
Logging module in Python for both Python projects and TD projects.

The Logger module is located in TD/Scripts/Logger

## How to use
#### In TouchDesigner

Add the three files in local/modules COMP. (see TD/LABI_Logger.toe)

in your Class/Extension:
```
from LABILogger import LABILogger

class YourExtension():
  def __init__(owner):
    self.logger = LABILogger(__name__, file='INFO')
```
#### In Python project

Copy the 'Logger' folder under 'TD/Scripts/' in your project.

In your main .py file (App.py):
```
sys.path.append('./Logger') #path to the Logger folder
from  Logger.LABILogger import LABILogger

loggername = __name__ if __name__ != "__main__" else 'DEFAULT-LOGGER-NAME'
LOGGER = LABILogger(loggername, file='INFO')
```
In a class:
```
class AClass(object):
  def __init__(self):
    self.logger = LABILogger(__name__, stream=None, file=None)
    self.logger.AddTimedFile('tracking', 'W-6', 27, 0, severity='INFO')
    self.logger.Log('Initialzing a class', 'INFO')
  
```
To use the same Logger inside different classes, see 'Python/Helpers/A_class.py' and 'B_class.py'.



#### Public Methods

>**Log(msg, severity)**

Logs the 'msg' at the specified severity



>**UpdateStreamSeverity(severity, label=None)**

Updates the severity of a Stream handler.

if the label is 'None' it will target the default Stream handler (created on __init__())



>**UpdateFileSeverity(severity, label=None)**

Updates the severity of a File handler.

if the label is 'None' it will target the default File handler (created on __init__())



>**ListHandlers()**

Returns a list of Handlers associated with that Logger



>**DeleteHandler(label)**

Deletes a handler using his label



>**AddStream( label, severity='DEBUG')**

Adds a Stream handler to this logger. (for printing in the console)

If not specified, the severity will be set to 'DEBUG'.



>**AddFile( label, severity='DEBUG')**

Adds a File handler to this logger.

If not specified, the severity will be set to 'DEBUG'.



>**AddTimedFile( label, when, interval, backupCount, severity='DEBUG')**

Adds a TimedRotatingFile handler.

For parameters, see : https://docs.python.org/3.7/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
