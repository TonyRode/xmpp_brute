# xmpp_brute
An XMPP v1 bruteforce using Hydra and a custom localhost server

Perfs : 1400 passwords / min on a Kali VM with 2Go RAM and 2 CPUs

## Usage
* Read your wireshark (filter : xmpp) packets from server -> client : the successful authentication tcp stream
* Extract hex values of the 4 packets and put it in the code
  * 1rst packet : you can customize the first packet to force the client to use a specific mechanism (by removing the unnecessary ones)
  * Don't hesitate to switch from hex to ascii to see what you do
* Run with python3 xmpp_brute.py
* Launch hydra with your wordlist with hydra xmpp://127.0.0.1:65535 -l login -P wordlist.txt
  * The login can be found on the 3rd packet sent from the client to the server, by decoding it (base64), it's the "n=" value, as a response of an empty challenge
* Wait

Enjoy !