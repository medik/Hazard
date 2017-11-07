# Specification for Server to Client and Client to Server Communication

(version 0.1)

The purpose of this document is to inform what available commands you
can send to the server for each client. This document is divided into
two section, first the client to server communication and next server
to client. Each section will be divided into availbable commands and
responses.

## Client to Server

### Start the game
Send:
```
{'my_name': <string>, 'start_game': true}
```
Response:
None, ask the server for the board.

### Get the board
Send:
```
{'get_board': true}
```

Response:
```
{ 'board': ..., 'active_block': ..., 'next_block': ..., 'tick': <integer> }
```

### Movement
Send:
```
{ 'movement': <movement_str> }
```
where `<movement_str>` is a string with values `left`,`right`, `rotate` or `hard_drop`.

Response:
```
{ 'status': <status_int> }
```
where `<status_int>` is a integer with value 1 (ok) or 0 (error).

## Server to Client

### Game over
Send:
```
{ 'game_over': true }
```