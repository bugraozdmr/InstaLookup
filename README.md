<p align=center>
  <br>
  <a href="https://github.com/bugraozdmr/Arsen/blob/main/Arsen/images/sample-2.png" target="_blank"><img src="https://raw.githubusercontent.com/bugraozdmr/Arsen/main/Arsen/images/sample-2.png"/></a>
  <br>
  <span>Search instagram users without logging in</span>
  <br>
</p>




## Installation

```console
# clone the repo
$ git clone https://github.com/bugraozdmr/InstaLookup.git

# change the working directory to Arsen
$ cd InstaLookup

# install packages
$ pip install -r requirememts.txt

```

## Usage

```console
$ python InstaLookup.py -h
Usage: InstaLookup.py -f <user agents file> -u <usernames file> -o <output file> -p <proxy_list>

Options:
  -h, --help            show this help message and exit
  -u USERNAMES_FILE, --usernames=USERNAMES_FILE
                        Specify the file path for usernames
  -a USER_AGENTS, --agents=USER_AGENTS
                        Specify the file path for user agents
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        Specify the output file name (optional)
  -p PROXY_LIST, --proxies=PROXY_LIST
                        Specify the proxy list file name (optional)
```

Basic search for user:
```
python InstaLookup.py -u resources/users.txt -a resources/useragents.txt
```
Advanced search for user:
```
python InstaLookup.py -u resources/users.txt -a resources/useragents.txt -o grant3.txt -p resources/proxies.txt
```

Always open for contribution
Thank you for using InstaLookup 🎉🎉🎉
