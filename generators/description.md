this folder (**generators**) contains all the necessary elements needed to generate webpages for my websites.    
namely it has the script that turns `.md` files into `.html` ones and all the `.html` templates that I need.   

---

## Disclaimer

Disclaimer: `generator.py` will not perfectly convert ALL `.md` files -- there are most definitely edge cases that I've missed and/or weird behaviors that I code wrong.     
In the case of one of those edge cases, you *can* open a PR (I may not get around to it), but it's most likely quicker if you either (a) tweak the specific markdown code to make it more 'tame', (b) fix the corresponding `.html` file manually to what you want it to be, or (c) rewrite `generator.py` to your liking.


## Specs

Specifically, here are some dos and donts for my generator:    
Do:  
* leave whitespace so everything is easier to parse :)
* use whitespace at the end of a line for a line break


Don't:  
* use unnecessary whitespace (spaces before paragraphs; random spaces in headers, etc.) -- it may or may not be rendered in the final html
* use closing hashtags in headers. these will be rendered as text 
* use underscores (`_`) to italicize or bold (e.g. `the __fox__`)
* use emojis in markdown (~~why are you doing this anyways~~)
* use backslashes (`\\`) to signal the end of a line. 




Maybe:
* use weird unicode characters. this is just out of my use case so