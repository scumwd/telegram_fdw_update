# telegram_fdw - a Telegram BOT, for PostgreSQL

`telegram_fdw` is a [Telegram BOT](https://core.telegram.org/bots) implemented using the PostgreSQL
foreign data wrapper interface.

## Install

`telegram_fdw` was tested under PostgreSQL versions 9.4 and 9.5.0
(Multicorn actually has a bug on PostgreSQL 9.5.1)


To install `telegram_fdw` on Debian is easy, just follow the steps:


```bash
sudo apt-get install postgresql-9.4-python-multicorn
sudo pip install twx.botapi
sudo pip install http://github.com/guedes/telegram_fdw/archive/v0.1.0.zip
```

The example bellow shows how to use the extension on database `monitoring`
that owner is the user `monitor`.

First, creating the multicorn extension:

```sql
psql -d monitoring -U postgres
create extension multicorn;
grant usage on foreign data wrapper multicorn to monitor;

```

Then, create the multicorn server on `monitoring` database:

```sql
psql -d monitoring -U monitor
create server multicorn_srv
       foreign data wrapper multicorn
       options (wrapper 'telegram_fdw.TelegramForeignDataWrapper');
```

## Creating bots

To create a bot, just create a foreign table, like:


```sql
create foreign table telegram_monitor_bot 
(
       update_id     bigint,
       chat_id     	 bigint,
       message	     varchar,
       payload		 json
)
server multicorn_srv
options (primary_key 'update_id', bot_id '<<THE BOT TOKEN>>');

```

> **NOTE**: See how [BotFather](https://core.telegram.org/bots#botfather) can give you **THE BOT TOKEN**

## Testing your bot

In the Telegram app, search your bot (created in [BotFather](https://core.telegram.org/bots#botfather)) and send it a messagem.

You can get all messages sent to your bot with a simple `SELECT`:

```sql
SELECT * from telegram_monitor_bot;

 update_id |  chat_id  |  message  |                                                                                                                                                                                                                                                                                                                                                                   payload                                                                                                                                                                                                                                                                                                                                                                    

-----------+-----------+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 58493114  | 11123574  | Hi Bot!!  | {"update": {"message": {"delete_chat_photo": null, "new_chat_photo": null, "text": "Hi Bot!!", "sticker": null, "video": null, "chat": {"id": 1123574, "type": "private", "title": null, "username": "testuser", "first_name": "John", "last_name": "Smith"}, "group_chat_created": null, "forward_date": null, "left_chat_participant": null, "location": null, "photo": null, "document": null, "forward_from": null, "new_chat_participant": null, "date": 145210377, "audio": null, "reply_to_message": null, "sender": {"id": 11123574, "first_name": "John", "last_name": "Smith", "username": "testuser"}, "message_id": 101, "caption": null, "contact": null, "voice": null, "new_chat_title": null}, "update_id": 58493114}}
(1 row)
```

To list all current chats:

```sql
SELECT DISTINCT
	payload #>> '{update,message,chat,id}'         as chat_id,
	payload #>> '{update,message,chat,first_name}' as first_name,
	payload #>> '{update,message,chat,last_name}'  as last_name,
	payload #>> '{update,message,chat,username}'   as username
FROM telegram_monitor_bot;

  chat_id  | first_name | last_name | username 
-----------+------------+-----------+----------
 11123574  | John       | Smith     | testuser
 11329588  | Foo        | Bar       | foobar
(1 row)
```

> **NOTE**: `payload` returns a `json` field so we can use [json functions](http://www.postgresql.org/docs/current/static/functions-json.html) to get the values.

Your bot can respond a message to a chat, using the respective `chat_id`. From the example above let's respond to *Foo Bar*:

```sql
INSERT INTO telegram_monitor_bot (chat_id, message)
VALUES (11329588, 'Hi! How are you?');
```

What about send a little :elephant: ?

```sql
INSERT INTO telegram_monitor_bot (chat_id, message)
VALUES (11329588, E'Hi! \U0001f418');
```

> **TIP**: [Emoji Unicode](https://telegram.me/emodibot) is a Telegram Bot that receives an emoji and returns the respective UNICODE.

That's it! Have fun!

# TODO

1. a BG Worker to async communication,
2. functions to help creating bots, send messages, etc,
3. a MonitorBot as an example of using KeyboardMarkup,
4. translate :emojis: to respective UNICODE
5. ...

# License

`telegram_fdw` was created by Dickson S. Guedes and is released under PostgreSQL License.

See [LICENSE](LICENSE) file for information.


