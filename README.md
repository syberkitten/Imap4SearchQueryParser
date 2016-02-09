# ImapSearchQueryParser

This code is more for a GIST then whole repository,
so future plans inclue normazliation according to demand :)
### Usage:
Simply executing the module will run afew query tests
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


