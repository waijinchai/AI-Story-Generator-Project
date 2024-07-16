import streamlit as st
from openai import OpenAI

def generate_story(prompt, client):
  story_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[{
          "role": "system", 
          "content": "You're a bestseller story writer. You will take user's prompt and generate a 100 words short story for adults age 20-30"
      }, {
          "role": "user",
          "content": f"{prompt}"
      }],
      max_tokens=400,
      temperature=0.8
  )

  story = story_response.choices[0].message.content
  # print(story)
  return story

# refine prompt
def refine_story(story, client):
  design_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[{
          "role": "system", 
          "content": "Based on the story given, You will design a detailed image prompt for the cover image of this story. The image prompt should include the theme of the story with relevant colour, stuitable for adults. The output should be within 100 characters."
      }, {
          "role": "user",
          "content": f"{story}"
      }],
      max_tokens=400,
      temperature=0.8
  )

  design_prompt = design_response.choices[0].message.content
  print(design_prompt)
  return design_prompt

def generate_cover_image(design_prompt, client):
  cover_response = client.images.generate(
      model='dall-e-2',
      prompt=f"{design_prompt}",
      size="256x256",
      quality="standard",
      n=1
  )

  image_url = cover_response.data[0].url
  # print(image_url)
  return image_url

api_key = st.secrets["OPENAI_SECRET"]
client = OpenAI(api_key=api_key)

st.title("AI Story Generator :sunglasses:")

with st.form("my_form"):
  st.write("This is for users to key in information")
  msg = st.text_input(label="Some keywords to generate a story")
  submitted = st.form_submit_button("Submit")
  if submitted:
    story = generate_story(msg, client)
    design_prompt = refine_story(story, client)
    image_url = generate_cover_image(design_prompt, client)
    st.image(image=image_url)
    st.write(story)
    
