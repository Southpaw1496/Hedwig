# Hedwig (BETA)
[Latest Releases](https://github.com/Southpaw1496/Hedwig/releases)

**Note:** Hedwig is in BETA. There shouldn't be too many (if any) bugs as the code is pretty simple, but it is in no way feature complete.

Hedwig (named after the faithful letter-carrying owl in Harry Potter) is a simple mod mail bot. Mod mail works on a simple premise: A user will DM the bot, and the bot will create a channel in a designated category in your server, just for that user. Any messages they send to the bot will be relayed to that channel, and any messages sent in their channel will be relayed, annonymysly, to the DM. In this way, any reports can be handled efficiently, collaberatively and anonymously by your moderation team.

[Why use Hedwig?](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#why-use-hedwig)

[Planned 1.0 Features](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#planned-10-features)

[Possible Future Features](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#possible-future-features)

[Installing](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#installing)

[Contributing](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#contributing)

[Support](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#support)

[Known Issues](https://github.com/Southpaw1496/Hedwig/new/main?readme=1#known-issues)

## Why use Hedwig?
While Hedwig may not be the most full-featured mod mail bot out there, there are a few reasons why you might want to use Hedwig over a similar mod mail or ticket bot.
1. Hedwig is **simple**: Because I don't know how to write complex code, Hedwig is written in simple language. This means that she is easier to modify for your own purposes if you want (which you can do; Hedwig is lisenced under MIT), and it means she's less likely to break and easier to fix if something goes wrong. Even if you're not much of a coder, I designed Hedwig to be easy to set up: Just install the dependencies, fill in the environment variables, start the script and off you go!

2. Hedwig is designed to be **self-hosted**: While Hedwig is not the only self-hosted mod-mail bot out there, being self-hosted gives her some advantages over public mod-mail bots. First, you can customise its name and avatar all you want. Want her in a Greek mythology-themed server? Name her Hermes and give her some winged boots, she won't mind. Second, there is no need for the user to select the server they wish to DM every time they DM the bot in case they share multiple servers with her, as she only exists in one server (yours).

3. [Planned] Hedwig uses **webhooks**: The primary reason I created Hedwig instead of using an existing bot is so that she can take advantage of webhooks. Unlike plain messages or cluttered embeds, webhooks make it seem (in the server channels) as though you are directly communicating with the user in question, so that you don't forget which one you're talking to. 

## Planned 1.0 Features
These features will be added to Hedwig before the first full release.

* **Webhook Support**: Hedwig will be able to use webhooks to display users you're communicating with in their channel.
* **Channel archiving**: Hedwig will be able to move channels marked as resolved channels to an archive category where they can live until needed again
**Welcome message**: If a user is not in Hedwig's database, she'll send them a message expalining how she works the first time they DM her.
**Reaction Confirmation**: Headwig will react to a message so that you can confirm if you want to send it or not (and cancel messages that were an accident).
**Server-side mail initialisation**: The name needs work, but this feature will allow the moderators of a server to initiate a modmail conversation with any user who is a member of that server.

## Possible future features
* Discord / command support

## Installing
(Detailed instructions for installation will be in the wiki on the full release, if you're running the beta you probably know somewhat what you're doing)
1. Create an application at https://discord.com/developers and add a bot user. Configure the name and avatar as you wish (it would be nice if you named it Hedwig but you don't have to). Save the bot token for later (but keep it secret).
2. Download the [Latest Release](https://github.com/Southpaw1496/Hedwig/releases)
3. Install python 3.8.6 and the necessary dependancies: sqlite3 (installed by default), [discord.py](https://github.com/Rapptz/discord.py) (`pip install discord.py`) and [dotenv](https://github.com/theskumar/python-dotenv) (`pip install python-dotenv`)
4. Fill out the values in the .env.example
5. Run the bot

## Contributing
Pull requests that fix bugs will generally be accepted. Those at add features will generally not be accepted. If you want a feature pull request to be accepted, the best way to improve your chance is to create a [Feature Request Issue](https://github.com/Southpaw1496/Hedwig/issues/new?assignees=&labels=&template=feature_request.md&title=%5BREQUEST%5D) and wait to get that approved before PRing 

## Support
If you need support with installing or using Hedwig (AFTER following the installation instructions) you can DM me on [Twitter](https://twitter.com/Southpaw1496) or Discord (Southpaw#1496, will only work if we share a server with DMs on), or you can create a GitHub issue. I may create a Discord server if there is enough demand.

## Known Issues
* ~~Deleting a channel Hedwig-created channel will probably make bad things happen as there is nothing to remove the channel's entry from the database.~~ Fixed in Beta 2
