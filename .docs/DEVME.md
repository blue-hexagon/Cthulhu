# DevNotes

`git commit --no-verify -m "match not supported by numpy, use this"`

`pre-commit run --all-files`

`pytest --cov`

`bandit -r my_sum`

`pygount --format=summary ./src`

## Close vs. Shutdown of a Socket


Calling close and shutdown have two different effects on the underlying socket.

The first thing to point out is that the socket is a resource in the underlying OS and multiple processes can have a handle for the same underlying socket.

When you call close it decrements the handle count by one and if the handle count has reached zero then the socket and associated connection goes through the normal close procedure (effectively sending a FIN / EOF to the peer) and the socket is deallocated.

The thing to pay attention to here is that if the handle count does not reach zero because another process still has a handle to the socket then the connection is not closed and the socket is not deallocated.

On the other hand calling shutdown for reading and writing closes the underlying connection and sends a FIN / EOF to the peer regardless of how many processes have handles to the socket. However, it does not deallocate the socket and you still need to call close afterward.

- https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
