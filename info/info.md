# Website Information
Updated: 08/17/2025

(Note: this stuff is mostly all for me)

----

Decided to rewrite my website. From my brief overview, seems like the things I could do are (ranked from most abstraction to least abstraction):    
1. Use Hugo. Hugo is a static site generator and abstracts hard stuff away, but it does require a software installation :/     
2. Use flask. I have some previous experience with it (see PAIR) but flask can be dynamic so it can't really be hosted with github pages :<.     
3. Write my site from scratch.

So it seems like I'll be going with option 3. 


Most likely I'll make my site something like flask but for static websites -- there are some set HTML templates for overall website structure, and content is filled in accordingly by running some sort of script. The pipeline then to making a page would be *create/find HTML template* -> *make md file* -> *run script to generate static html file from template and md file* (and then profit).

Inspiration taken from Flask, Hugo, [ukarim](https://github.com/ukarim), and [Logan Graves' post](https://logangraves.com/website).
