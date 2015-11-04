
## HTTP get protocol implementation
Working HTTP get request implementation.
## HTTP get SERVER implementation

Created the TCP socket and bind it to HOST and PORT.
HOST being localhost and PORT being a free port number.
Now I wait for a connection. Whenever I get a HTTP request I parse that and send the required HTML file to the HTTP_RESPONSE instance to check whether the file exists or not and send the appropiate content and header data.
## HTTP get CLIENT implemetation
HTTP CLIENT:
The HTTP client takes three command line arguments apart from the Python file name. The format to compile and run the code is:

python client.py HOST PORT FILEPATH	

Here HOST is the IP address of the server from where the file given in the FILEPATH has to parsed for getting .html file links which we in turn have to download to out local machine. PORT is just the port number 80.

First I create a TCP connection to (HOST,PORT) and then send a GET request to the server requesting the file I want to download. Once I get the data from the file I pass the data to a function called extractfiles() which extracts a finite number of .html files from the html file data passed onto it. Once I have a list of all .html files I just send the list to a downloadfiles() function which downloads all the files for me i.e. create new files with the same content in my local machine.

## Installation
python 2.7 and a operating system with Berkeley Sockets distribution.
## Files
client.py =====>>> The client side code. 

server.py =====>>> The server side code.
## Usage
In order to run you just need to open two terminals and goto the directory of these files. There run both the files with appropriate command line arguments using python 2.7.

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits
Who else. Me. :D
