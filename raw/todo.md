TEMPLATE: base
PAGETITLE: Website todo list.
-x-x-x-x-

todo list:

done:    
- [x] make my website (semi-functionally)    
- [x] make a custom 404 page    
- [x] turn -- or --- into em dashes  
- [x] make the generator ACTUALLY turn `.md` into `.html` (as opposed to just adding the lines raw)    
- [x] do a strikethrough (~~)     
- [x] make code (`<code>`/`<pre>`) blocks actually look good (a.k.a. change the css so they don't stick out, add some margins, box outline/indent)      
- [x] do unordered lists - NOTE: you cannot stack lists with other things or have sub-bullet points      
- [x] do links (href) -- this will probably be done in text processing section
- [x] add support for images.    
- [x] fix my broken shark favicon (does it need to be of type ico?)    


in progress/considering/whatever:   
- [ ] make my 404 page look cooler 
- [ ] make a custom 500 page (+ when would i need this)        


----

way later (aka never):   

- [ ] add a stupid license
- [ ] implement subpages (currently this is IMPOSSIBLE lmao)   
- [ ] figure out escape characters
- [ ] implement custom tags! -- e.g. custom box tihngies that can be made during .md -> .html    
- [ ] make my basic webpage be in the style of playing cards (consult notebook drawings) 
- [ ] add footnote support
 

not doing:   
- [ ] make `generator.py` conform to the markdown spec. is just too time consuming + annoying for me to cover the edge cases, and I'll assume that most md is written nicely -- aka written the way i write it. (spec: https://spec.commonmark.org/0.31.2/)    
- [ ] turn this into a legit open src thing with good readmes + docs (or maybe rewrite this)
- [ ] make block quotes be able to nest / be able to accomodate more than a quote in the block quote thing (bro just edit the html yourself)
- [ ] ordered (numbered) lists. I just don't like them (change `<ul>` to `<ol>` if you're annoyed)


