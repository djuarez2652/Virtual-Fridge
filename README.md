# SEO Week 4 Project - Virtual Fridge

## Project Story

The user could input a list of food / ingredients and the website would in turn generate a recipe that uses as many of those foods as possible. 

On a separate page, there is a graphical interface that displays the foods and allows the user to keep track of their expiration dates. 

The user can also upload pictures of the food label / fresh produce and the website will use AI assistance to parse or generate the expiration date.

## Implementation Details

Front End:
- recipe generation page
- fridge / food tracking page

Back End:
- multi-user
- For each user:
  - 1 table for food & expiration date
  - 1 table for generated recipes

API:
- [Edamam](https://developer.edamam.com/edamam-docs-recipe-api)
- [ChatGPT](https://platform.openai.com/docs/api-reference/introduction)
