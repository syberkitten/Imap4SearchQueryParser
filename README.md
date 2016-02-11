# ImapSearchQueryParser

This code is more for a GIST then whole repository,
so future plans inclue normazliation according to demand :)

Implementing a pseudo Parse Tree algorythm economically and specifically designed
for parsing imap search query commands into dictionary entities that can be 
passed to different layers in your application, to handle the actual retrieving
of the mesasges.

The class therefore normalizes the search query commands into a filter list
made of flags and commands with arguments, supporting NOT and OR operators.

also to note, that OR by design can be used only once
in the command list, otherwise it would be merged with previous OR commands.

It is possible to change this paradigm, but for pragmatic reasons and concensus
the code can handle only one OR, and multiple NOT commands.


### Usage:
Simply executing the module will run a few query command tests
```py
python SearchParser.py
````
or in your own code

```py
from SearchParser import ImapSearchQueryParser
c = ImapSearchQueryParser()
res = c.parse(['SUBJECT','all about love','NOT','TO','johan@myemail.com','SINCE','1-Feb-1994','NOT','FROM','Smith','UID','1:*','OR','NOT','TEXT','Go To Hello'])

print c
=
{'not-to': 'johan@myemail.com', 'since': '1-Feb-1994', 'not-from': 'Smith', 'or': {'not-text': 'Go To Hello', 'uid': '1:*'}, 'subject': 'all about love'}


```

based on RFC3501:
https://tools.ietf.org/html/rfc3501#section-6.4.4


### IMAP4 SEARCH Query commands
- C: A282 SEARCH FLAGGED SINCE 1-Feb-1994 NOT FROM "Smith"
- S: * SEARCH 2 84 882
- S: A282 OK SEARCH completed
- C: A283 SEARCH TEXT "string not in mailbox"
- S: * SEARCH
- S: A283 OK SEARCH completed
- C: A284 SEARCH CHARSET UTF-8 TEXT {6}
- C: XXXXXX
- S: * SEARCH 43
- S: A284 OK SEARCH completed




### Todo's

Ideas welcome

License
----

MIT


