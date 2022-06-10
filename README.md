# Web-Backend-Project-4
Tracking the State of Game using Redis Database

In this project I have used a NoSQL database to build a stateful back-end microservice and to improve the performance of an existing service.

The following are the learning goals for this project:

Gaining further experience with implementing back-end APIs in Python and FastAPI.

Learning to design a data model for a key-value store.

Exploring the features of the Redis NoSQL database.

Introducing polyglot persistence to a service by splitting data between data stores.


Implementing a Service to Track State

While you can successfully combine the services from previous projects to check that users are making valid guesses, check those guesses to see if they are correct,
and record wins and losses, so far there is no ability to limit users to the six tries required by the game, or to restore a game in progress.

Create a new microservice for tracking the state of a game. Your service should expose the following operations:

Starting a new game. The client should supply a user ID and game ID when a game starts. If the user has already played the game, they should receive an error.
Updating the state of a game. When a user makes a new guess for a game, record the guess and update the number of guesses remaining. 
If a user tries to guess more than six times, they should receive an error.

Note: you do not need to check whether the guess is valid, if the guess is correct, or report on the placement of the letters in the answer. This functionality was completed in Project 2.

Restoring the state of a game. Upon request, the user should be able to retrieve an object containing the current state of a game, including the words guessed so far and the number of guesses remaining.


