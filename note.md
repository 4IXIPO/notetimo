data structures, we need to connect em in a strings before we do it
then we can send em to internet
manipulating strings takes lot time so we use data structures so it will b eeasier
serializing, deserialising we use thcp ip mostly
when we use de tools we can see how the network connections
1 refresh take 6-7 requests
every request is different thcp/ip connection

================================

http 
client and server
request     response

client requests, server responds
server also can be a client

================================

request look like:

-request line      \
                   request message header
-request headers   /
---------------------------------------------->
-a blank line separates header and body
-request message body

================================
request mostly looks like binary code
/you can google first 5-7 numbers to know what binary decoder u need for this code/

http client library
server library

methods: Get, Post, Put, Delete, Options etc.

Status codes: 
2xx - success
3xx - redirect
4xx - client error
5xx - server error

/status code is coming from the server/

headers must go together with first line
headers end and body start
message is in body
empty new line means that body starts

browsers can do like 20 different connections with 1 computer
64k connections is max right now

Header and body

