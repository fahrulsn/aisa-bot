import tensorflow as tf
import pandas as pd
import numpy as np
import re
import os
import joblib
import asyncio
from discord.ext import commands
import discord
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from server import server

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

violations = {}

model = tf.keras.models.load_model('./model/model.keras')
tokenizer = joblib.load('./assets/tokenizer.joblib')
alayDict = pd.read_csv('./assets/new_kamusalay.csv', encoding='latin-1', header=None)
alayDict = alayDict.rename(columns={0: 'original', 1: 'replacement'})
factory = StemmerFactory()
stemmer = factory.create_stemmer()


def lowercase(text):
  return text.lower()


def remove_unnecessary_char(text):
  text = re.sub('\n', ' ', text)  # Remove every '\n'
  text = re.sub('\r', ' ', text)  # Remove every '\r'
  text = re.sub(
      '(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?',
      '', text)  # Remove every URL
  text = re.sub('(?i)rt', ' ', text)  # Remove every retweet symbol
  text = re.sub('@[^\s]+[ \t]', '', text)  # Remove every username
  text = re.sub('(?i)user', '', text)  # Remove every username
  text = re.sub('(?i)url', ' ', text)  # Remove every url
  text = re.sub(r'\\x..', ' ', text)  # Remove every emoji
  text = re.sub('  +', ' ', text)  # Remove extra spaces
  text = re.sub(r'(\w)\1{2,}', r'\1\1',
                text)  #Remove characters repeating more than twice
  return text


def remove_nonaplhanumeric(text):
  text = re.sub('[^0-9a-zA-Z]+', ' ', text)
  return text


alayDictMap = dict(
    zip(alayDict['original'], alayDict['replacement'], strict=False))


def normalize_alay(text):
  return ' '.join([
      alayDictMap[word] if word in alayDictMap else word
      for word in text.split(' ')
  ])


def stemming(text):
  return stemmer.stem(text)


def preprocess(text):
  text = remove_unnecessary_char(text)  # 1
  text = lowercase(text)  # 2
  text = remove_nonaplhanumeric(text)  # 3
  text = normalize_alay(text)  # 4
  text = stemming(text)  # 5
  text = text.strip()
  print(text)
  return text


def processed(text):
  text = preprocess(text)
  text_sekuens = tokenizer.texts_to_sequences([text])
  text_padded = pad_sequences(text_sekuens,
                              maxlen=900,
                              padding='post',
                              truncating='post')
  return text_padded


def predict(msg):
  processed_text = processed(msg)
  predictions = model.predict([processed_text])
  hasil = np.argmax(predictions[0])
  return hasil


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('>test'):
    await message.channel.send('Hello!')

  result = predict(message.content)
  if result == 3 or result is None:
    return
  messages = ""
  if result == 0:
    messages = "mengandung ujaran kebencian :("
  elif result == 1:
    messages = "mengandung kata-kata kasar :("
  elif result == 2:
    messages = "mengandung ujaran kebencian dan kata-kata kasar >:("

  user_id = str(message.author.id)
  violations[user_id] = violations.get(user_id, 0) + 1
  await message.channel.send(
      f"{message.author.mention}, pesan Anda {messages}\n Pelanggaran: {violations[user_id]}/3"
  )

  if violations[user_id] > 2:
    role = discord.utils.get(message.guild.roles, name='Muted')
    await message.author.add_roles(role)
    await message.channel.send(
        f"{message.author.mention}, Anda telah dimute karena melakukan pelanggaran yang berulang."
    )
    violations[user_id] = 0  # Reset jumlah pelanggaran setelah memberi sanksi

    # Tunggu 100 detik sebelum menghapus peran Muted
    await asyncio.sleep(100)
    await message.author.remove_roles(role)

  await client.process_commands(message)


server()
client.run(os.environ['TOKEN'])
