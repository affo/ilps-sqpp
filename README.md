Get [pip](https://pip.pypa.io/en/stable/installing/) and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and run:

```
$ git clone https://github.com/affo/ilps-sqpp.git ilps
$ cd ilps
$ sudo pip install -r requirements.txt
$ python placement.py
```

You can edit the file `placement.py` to change the values of

```
NETWORK_SIZE = 50
MAX_LATENCY = 5
MAX_NODE_CAPACITY = 8
```

on the top.
