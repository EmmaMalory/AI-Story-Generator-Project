import streamlit as st
from openai import OpenAI

key = st.secrets["OPENAI_KEY"]

# set up open AI
client = OpenAI(api_key=key)

def story_generator(prompt, the_client):

  response = the_client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = [
          {'role': 'system',
          'content': 'You are a bestselling author. You write romance stories for young adults. Based on the user input, write a 100 word short story following the prompt.'},
          {'role': 'user',
          'content': prompt}
      ],
      max_tokens = 400,
      temperature = 1
  )
  
  story = response.choices[0].message.content
  
  return story

def book_cover_prompt(story, the_client):
  response = the_client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = [
          {'role': 'system',
          'content': 'Based on the story given, design a detailed image prompt for the cover image of this story. The book cover image prompt is detailed and contains relevant story plotline. The output should be an image prompt within 100 characters.'},
          {'role': 'user',
          'content': story}
      ],
      max_tokens = 100,
      temperature = 1
  )

  cover_prompt = response.choices[0].message.content

  return cover_prompt

def cover_generator(cover_prompt, the_client):
  pic = the_client.images.generate(
      model='dall-e-2',
      prompt = cover_prompt,
      n = 1,
      size = '256x256',
      quality='standard'
  )

  image_url = pic.data[0].url

  return image_url

st.header('Short Story Generator')

with st.form('prompter'):
  prompt = st.text_input(label="Enter your story prompt")
  submit = st.form_submit_button('Submit')
  if submit:
    new_story = story_generator(prompt, client)

    book_cover = book_cover_prompt(new_story, client)
    cover = cover_generator(book_cover, client)

    while cover is None:
      cover = cover_generator(book_cover, client)
      
    st.image(cover)
    st.write(new_story)