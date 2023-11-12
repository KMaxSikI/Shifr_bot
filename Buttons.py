from aiogram import types


# Клавиатура
kb = [[types.KeyboardButton(text='🔐 Зашифровать сообщение'),
       types.KeyboardButton(text='🔓 Расшифровать сообщение')],
      [types.KeyboardButton(text='📄 Описание')]
      ]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                     resize_keyboard=True,
                                     input_field_placeholder="Ваше сообщение#ключ шифрования")