
## DNS-proxy server implementation
Working DNS-proxy server implentation
## Details
Proxy Server class creates a proxy server that acts as a intermediate between the nameserver and the host
It will cache a specific number of requests
The DNS query will be resolved at the proxy server if we find the query in the Cache
Otherwise the request is forwarded to the Name Server.
 
## Cache Implentation
Cache Implementation :
The Cache is implemented using the a Dictionay and List.
The key of the Dictionary is the request query without the queryid.
The value of the Dictionary the responce without the queryid.
The cache size is fixed.
The List is maintained to delete the oldest query in the cache.
If the List is full the first element of the list is deleted and also its entry in the Dictionary.

## Installation
python 2.7 and a operating system with Berkeley Sockets distribution.

# Configure
Configure your local dns config file so that the request redirects to your file.

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits
Who else. Me. :D
