TEMPLATE: base
PAGETITLE: Website Info :)
-x-x-x-x-

# Website Information
Last updated: 11/26/2025

---

This website is written from scratch.

Inspiration for my website taken from Flask, Hugo, [ukarim](https://github.com/ukarim), and [Logan Graves](https://logangraves.com/website).

### Motivation

I decided to rewrite my website because I wanted to make it better (and to not write in html). From my brief overview, it seemed like the things I could do were (ranked from most to least abstraction):    

1. Use Hugo. Hugo is a static site generator and abstracts hard stuff away, but it does require a software installation :/     
2. Use flask. I have some previous experience with it (see PAIR) but flask can be dynamic so it can't really be hosted with github pages :<.     
3. Write my site from scratch.

And I went with option 3.

As a result, the website you're reading was/is originally a markdown file that got converted into a static html file that is getting served to your computer by Github Pages and stuff.

---

## Structure

All markdown files that make up this website (including this one) are in a folder called `raw/` (e.g. the markdown that was used to generate this file is called `raw/info.md`). In each of these `.md` files, there's a brief 3-line header with some meta-info detailing how exactly to turn the `.md` file into `.html`. The rest of the `.md` file is the webpage's content, and is written in regular[1] markdown. 

([1]: With some caveats. I found ordered lists too hard to implemnt so that along with footnotes and nested block quotes are unimplemented. Also of course specific ambiguous markdown lines can probably confuse my primitive programming so the bottom line is that clear, boring, and simple markdown files will have no problem being turned into html files.)

Specificallly, the brief 3-line header should look something like this (this is the header used to generate this file):

```TEMPLATE: base
PAGETITLE: Website Info :)
-x-x-x-x-
```

The first line (`TEMPLATE: base`) tells the generator program which html template should be used when generating the `.html` file. All `.html` templates should be located in `generators/templates/` and a different template will correspond to different css code and html layout.      
The second line (`PAGETITLE: Website Info :)`) ends up being the corresponding webpage's page title (Look up! Next to to the shark favicon should be some text that says "Website Info". That's what this line does).    
The third and final line of barbed wire is simply a delimiter that the generator program looks for to confirm that the file header is done. And the fourth line (which should be empty) is a mandatory spacer.

           

Generally, page content should be changed in the corresponding `.md` file, while the overall page structure should be changed in the template `.html` file. The only caveat to this is the navigation bar; that's hard coded in the presets section of the webpage generator (located at the top of `generators/generator.py`). 

Also note that any files that start with an underscore character in `raw/` are ignored. This is useful for archiving past drafts and markdown  templates.

---
## Build

#### Prerequisites

Some prerequisites to help you succeed with this project:

- Be familiar with Python (or have your code machine generator be familiar with Python)
- Be somewhat familiar with HTML
- Have the patience to debug someone else's code
- Have Python >= 3.9.6 (this is arbitrary - I just like Python 3.9)

#### Build

To build this exact repository (Note: I have not figured out ordered lists so an unordered one must do for now):
- Clone this repository (`git clone https://github.com/LeopardCheetah/LeopardCheetah.github.io.git`).
- Replace all markdown files in `raw/` with **your own** markdown files. Remember to follow the spec as labelled above!
- Replace all template files in `generators/templates/` with your own template html files. 
- Change the specific presets located at the top of `generators/generator.py` to your own presets. Mainly change that nav bar.
- Run the python file in `generators/generator.py`. This should turn all your `.md` files into corresponding `.html` files that will end up in the repo home directory.
- Profit!

I obviously cannot promise that every markdown file will generate properly with my program, so to any brave soul who attempts to use my code, know that I am both happy that you're using my code and also that there will need to be some debugging done if you want a good website. 

Anyways, go out there and go make your own website, no matter how simple it is. I'm sure it'll be great :).
