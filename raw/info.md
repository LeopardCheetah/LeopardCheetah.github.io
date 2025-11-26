TEMPLATE: base
PAGETITLE: Website Info :)
-x-x-x-x-

# Website Information
Updated: 11/26/2025


---

### Motivation

I decided to rewrite my website because I wanted to make it better (and to not write html). From my brief overview, it seemed like the things I could do were (ranked from most to least abstraction):    
1. Use Hugo. Hugo is a static site generator and abstracts hard stuff away, but it does require a software installation :/     
2. Use flask. I have some previous experience with it (see PAIR) but flask can be dynamic so it can't really be hosted with github pages :<.     
3. Write my site from scratch.

So of course I went with option 3.

Now, this website is being served to you from Github pages.


Most likely I'll make my site something like flask but for static websites -- there are some set HTML templates for overall website structure, and content is filled in accordingly by running some sort of script. The pipeline then to making a page would be *create/find HTML template* -> *make md file* -> *run script to generate static html file from template and md file* (and then profit).

Inspiration taken from Flask, Hugo, [ukarim](https://github.com/ukarim), and [Logan Graves](https://logangraves.com/website).
