![Angular Frontend](https://github.com/acipm/kibicara/workflows/Angular%20Frontend/badge.svg)
![Python Backend](https://github.com/acipm/kibicara/workflows/Python%20Backend/badge.svg)

# Kibicara

Kibicara relays messages between different platforms (= social networks).

In its web interface, a hood admin (= registered user) can create a hood to
build a connection between different platforms.

Users can message a specific hood account on a specific platform (e.g. @xyz on
Telegram). This pushes the announcement to all platform accounts of a hood.
For example: User A writes a message to @xyz on Telegram (which has been
connected to Kibicara by a hood admin). This publishes the message on e.g.
Twitter and other platforms which have been connected to the hood.

The admin of a hood has to define trigger words and bad words. Messages need to
contain a trigger word to be relayed, and must not contain a bad word.

Kibicara needs to be hosted on a server by an instance maintainer. That way,
hood admins don't need a server of their own.

## Deploy Kibicara on a production server

Read `DEPLOYMENT.md` to learn how to deploy Kibicara.

## Contribute!

Read `CONTRIBUTING.md` to learn how to get started.
