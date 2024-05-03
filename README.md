# Report

Name : Bellatrix Hodgson

Matriculation Number : 2770706H

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

For all data (apart from 1 byte codes), there is a length field before the data to know where the message starts and ends. I chose this over a start/end sequence so that data sent didn't need to avoid any sequences. Also, it felt more efficient than checking for the sequence over and over.

The protocol also sends minimal error codes in that it only sends confirmation if something could have gone wrong within the server or client, it does not consider the network as that is handled by TCP. For example, when doing a list request, the client will take the list it receives or does not receive as confirmation enough. However, as the client could have had an error while trying to display the list, so it sends a confirmation to the server after it has displayed. This way the server knows it can depend on the client having seen the list.

This also applies for put and get requests. Since the network is assumed reliable due to TCP, only the file receiving party sends confirmations. That way the server can rely on the client having files it sent it, and vice versa.

I decided to make the maximum file size that could be sent 136 GB because 40 bytes for a length integer seemed about right. I haven't tried, but the length integer is all tied to one constant called "MAX_FILE_LEN_SIZE_BYTES" in common_utilities, so it is probably easy to increase this limit. But the official size of it is 40 bytes.

The length integer for the filename is only 2 bytes long because in windows the maximum filename length is 255 characters. One utf-8 character can be up to 4 bytes. 4*255 = 1020. 1020 can't be represented by one byte, so two it is. The program lets the full 2^16 bytes be used instead of just 1020 as if a user is trying to have filenames that long, they probably know what they are doing.

### Exchanges

The exchanges differ between request types but the encoding is the same.

For request type there is 1 byte:
 - put = 0x00
 - get = 0x01
 - list = 0x02

For error codes there is 1 byte:
 - success = 0x00
 - overwrite failure = 0x01
 - generic failure = 0x02

#### List

First the list request is created and sent by the client:
 - request type (list)
   - 1 byte

That is received by the server, then the list is created and sent by the server:
 - list length
   - integer
   - 40 bytes
 - list
   - utf-8 string
   - between 0 and 2^40 bytes

That is then received by the client and a confirmation or error is sent:
 - error code
   - 1 byte

#### Get

First the get request is created and sent by the client:
 - request type (get)
   - 1 byte
 - filename length
   - integer
   - 2 bytes
 - filename
   - utf-8 string
   - between 0 and 2^16 bytes

That is received by the server, then the file is found and sent by the server:
 - file length
   - integer
   - 40 bytes
 - file
   - any binary encoding
   - between 0 and 2^40 bytes

That is then received by the client and a confirmation or error is sent:
 - error code
   - 1 byte

#### Put

First the put request is created and sent by the client:
 - request type (put)
   - 1 byte
 - filename length
   - integer
   - 2 bytes
 - filename
   - utf-8 string
   - between 0 and 2^16 bytes
 - file length
    - integer
    - 40 bytes
 - file
   - any binary encoding
   - between 0 and 2^40 bytes

That is then received by the server and a confirmation or error is sent:
 - error code
   - 1 byte
