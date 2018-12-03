# xmpp_brute
An XMPP bruteforce using Hydra and a custom localhost server
Note : only works if you have a network capture of a successful authentication.

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

## Requirement : Config file
In order to run the bruteforce successfully, you need to put some of your sniffed packets in the "config" file.
1 packet per line.
Authentication schema :
4 Requests / Answers, 8 packets in total : 4 from client (~hydra) to server, 4 from server to client.
All lines of the conf file MUST be in hex format, and MUST be the whole xmpp message (easily extracted from a pcap with wireshark : copy as hex stream).
First line of conf file = the 1rst packet sent from the server to the client (with the allowed mechanisms supported by the server => customizable to force SCRAM-SHA1 for example (only remove the unecessary ones from the packet)).
2nd line = 3rd packet sent from the server to the client. MUST be the real challenge in case of successful attempt (use tcp streams if you see many auths in the capture).
3rd line = 4th packet sent from the client to the server = The processed response according to the real challenge.
4th line = 4th packet sent from the server to the client = The <success></success>.

Enjoy !