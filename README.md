# BaseballBot

## Overview
This is a discord bot that has multiple features. It was originally designed to only return baseball stats but the features have been expanded.

## Features
I have organized the bot's commands into three categories: Baseball Stats, Quote Board, and Miscellaneous.

Baseball Stats: This group allows you to retrieve statistics for a specific player by year, by specific stat, or for their entire career.

Quote Board: This group lets you manage a collection of quotes. You can add a new quote, remove an existing one, or fetch a random quote from the stored collection.

Miscellaneous: This group includes a variety of commands:

* Create a poll where users can vote by reacting with emojis.
* Fetch a random meme.
* Respond with a simple "ping pong" reply.
* Get the weather for a specified city.
* Roll a die with a specified number of sides.

## Tech Stack
Python: The main bot uses discord.py and is built in python
APIs:
* statsapi: gets baseball stats
* baseball_id: gets the id of baseball players by name to be inputted into the statsapi
* datetime: gets the current date and time
* requests: allows me to make api calls
* random: gets me random numbers
* openweathermap: lets me get weather data
* meme-ap: allows me to get random memes

## Contact
For any inquiries, please contact me at ECohen1125@gmail.com.