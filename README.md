# Report

I have created a fully functional application protocol for exchanging files between a host and a client.

## Usage

**Server.py**
```
$ python server.py port

creates server at localhost port which client.py can make requests to.

eg:
$ python server.py 6000
```

**Client.py**
```
$ python client.py hostname port request (conditional)filename

will only work if server at hostname port exists

eg:
$ python server.py localhost 6000 list
$ python server.py localhost 6000 get cloud.txt
$ python server.py localhost 6000 put ground.txt
```

## Protocol

The protocol aims to be lightweight, simple, and flexible. 

For all data (apart from 1 byte codes), there is a length field before the data to know where the message starts and ends. I chose this over a start/end sequence so that data sent didn't need to avoid having the sequence, and it felt more efficient than checking for the sequence over and over.

