import json
from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres, ERROR, WARNING, DEBUG
from twx.botapi import TelegramBot, ReplyKeyboardMarkup

class TelegramForeignDataWrapper(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(TelegramForeignDataWrapper, self).__init__(options, columns)

        self.bot = TelegramBot(options['bot_id'])
        self.columns = columns
        self._row_id_column = options['primary_key']

    def execute(self, quals, columns):

        updates = self.bot.get_updates().wait()

        for update in updates:
            line = {}
            line['update_id'] = update.update_id
            line['chat_id'] = update.message.chat.id
            line['message'] = update.message.text
            line['payload'] = json.dumps({ "update": { "update_id": update.update_id, "message": { "message_id": update.message.message_id, "sender": update.message.sender, "date": update.message.date, "chat": update.message.chat, "forward_from": update.message.forward_from, "forward_date": update.message.forward_date, "reply_to_message": update.message.reply_to_message, "text": update.message.text, "audio": update.message.audio, "document": update.message.document, "photo": update.message.photo, "sticker": update.message.sticker, "video": update.message.video, "voice": update.message.voice, "caption": update.message.caption, "contact": update.message.contact, "location": update.message.location, "left_chat_participant": update.message.left_chat_participant, "new_chat_title": update.message.new_chat_title, "new_chat_photo": update.message.new_chat_photo, "delete_chat_photo": update.message.delete_chat_photo, "group_chat_created": update.message.group_chat_created }}})
            yield line

    def insert(self, values):
        result = self.bot.send_message(int(values['chat_id']), values['message']).wait()

    @property
    def rowid_column(self):
        if self._row_id_column is None:
            log_to_postgres(
                'You need to declare a primary key option in order '
                'to use the write features')
        return self._row_id_column
