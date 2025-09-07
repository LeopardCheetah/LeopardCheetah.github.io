"""
generates .html files from .md files
works (hopefully)
if it doesn't it fails noisely (i hope)
"""
# may or may not take up a ton of memory

######### Presets -- these should be CONSTANTS ##############

# what's on the nav bar left/right?
# format: (Descriptor, link, flag)
# flag -- 0 -> relative link (may need ..); 1 -> absolute link (is constant)
nav_bar_left = [("Home", "index.html", 0), ("Projects", "projects.html", 0)]
nav_bar_right = [("Github", "https://github.com/LeopardCheetah", 1), ("Resume", r"assets\resume.pdf", 0), ("Blog", "https://thelonewolf.bearblog.dev", 1)]
nav_bar_delimiter = "|" # separator between elements


# separates the meta stuff from the actual information stuff
template_delimiter = "-x-x-x-x-"


#############################################################

######### other presets -- idrk #############################

# generate .html files from the .md files in this file path
folder_to_generate_from = r'..\raw'
path_to_templates = r'..\generators\templates' # go from folder to generate from to the template folder
path_templates_to_end_directory = r'..\..' # go from template folder out to where you want the .html files to be

# ignore .md files with a leading _ char such as _test.md or _a-cool-file.md
ignore_leading_underscore_files = True 
whitespace_chars = [' ', '', '\t', '\n']

#############################################################


# known conversions to do:
# --- -> <hr /> (horizontal rule)

# ok let's parse!

import os
import os.path



# in: string 
# out: (char, index)
def get_first_non_whitespace_char(s):
    global whitespace_chars

    _i = 0
    c = ''
    for _c in s:
        if _c not in whitespace_chars:
            c = _c
            break
    
        _i += 1

    if _i == len(s) - 1:
        return '', -1

    return c, _i
def fchar(s): # make this easier to type
    return get_first_non_whitespace_char(s)
    
    
# in: string -- not a header, not part of a list, etc etc -- just the raw string to be parsed (e.g. add bold, italics, underlines.)
# out: bool, string, in html form of this string
def parse_str(s):
    # TODO - implement.
    # also do link rendering in here
    return False, ''

# in: string
# out: (bool, string) -> string out only if string in was a valid html header and stuff; otherwise bool is false
def is_header(s):
    # headers!
    global whitespace_chars

    if fchar(s) != '#':
        return False, ''
    
    _f = False 
    _count = 0

    for _c in s:
        if _c in whitespace_chars and not _f:
            continue 

        if _c == '#':
            _count += 1
            _f = True
            continue 

        if _c == ' ' or _c == '\t':
            _f = True 
            break

        _f = False 
        break

    if not _f:
        return False, ''

    if _count > 6:
        # too many #s lol
        return False, ''
    
    # turn title into html
    # NOTE: i am not parsing for unnecessary whitespace here
    # so like "#  x" might become "<h1> x</h1>"" instead of "<h1>x</h1>"
    _parsed = parse_str(s[s.index(' ', s.index('#')) + 1:])

    return True, f'<h{_count}>{_parsed}</h{_count}>'




# in: list of strings representing the content in a md file (line by line)
# out: list of strings representing the content of an html file (line by line)
# do NOT worry about adding \n characters to the end

# note: this will NOT 100% accurately convert every single md file into html. don't count on that.
def md_to_html(md):
    _div_stack = [] # stack of open divs 

    # state = 0 ==> normal text
    # state = 1 -> in an ordered list
    # state = 2 -> ul
    # state = 3 -> in blockquotes
    _state = 0 

    # line(S) of whitespace?
    _w = 0

    html = []

    for _line in md:

        # line of whitespace
        if not len(_line) or _line.isspace():
            # add 'linebreak' ONLY if enough lines have been moved
            if _w == 3:
                html.append('<p> </p>')
                _w += 1
                continue 

            if _w:
                html.append('')
                _w += 1
                continue 

            _w += 1
            # usually just close empty par tag or a list
            # TODO - make sure this thing is closing the right thing; currently this is arbitrary.
            # TODO - also make sure this is compliant with specs and stuff
            # html.append('<p> </p>')
            html.append('???????????')
            continue 
        
        if _state:
            # idk, do later
            # TODO - parse this when state = 1 or state = 2 (e.g. when in list)
            continue 


        # check if its header
        _b, _s = is_header(_line)
        if _b:
            _w = 0
            html.append(_s)
            continue 
        
        # TODO
        # check if its one of those weird things that turn the text above into a header 


        # check if we are blockquoting


        # check if we are starting a list


        # check if this is a horizontal rule


        

        # parse text normally (also beware linebreaks and stuff)
        pass 

    


    return html


def main():
    # check to make sure .md folder is valid 
    if not os.path.isdir(folder_to_generate_from):
        raise NotADirectoryError(f"{folder_to_generate_from} is NOT a valid directory!")
        return 

    os.chdir(folder_to_generate_from)

    # each pair in here is of form (filename, file lines)
    files_lines = []

    with os.scandir() as iterator:
        for entry in iterator:
            if not entry.name.startswith('.') and entry.is_file():
                if ignore_leading_underscore_files and entry.name.startswith('_'):
                    continue 

                if len(entry.name) < 3 or entry.name[-3:] != '.md':
                    continue # not a valid .md file

                with open(entry.name, 'r') as f:

                    lines = f.readlines()
                    files_lines.append((entry.name.strip(), lines))
                    continue 

                continue 
    
    # parse files_lines for juicy information
    # i'm p sure this is automated as all information given should be above the barbed wire.
    # and everything below that is content
    # so it works out.


    file_infos = []
    for p in files_lines:

        # contains all the file information
        # format: [int, kwargs]
        # int = 0 -> this is a setup thing (find and replace)
        # int = 1 -> nav bar (do this separately)
        # int = 2 -> content.

        file = []

        ctnt = []
        lines = p[1]
        md_lines = []

        _content = False 
        for l in lines:
            # split with ":" as the delimiter
            # until we get to the line "-x-x-x-x-"
            if l.strip() == template_delimiter:
                _content = True 
                continue 

            if not _content:
                # append basically all the stuff before the : and the content after the :
                file.append([
                    0, 
                    l.strip().split(':')[0], 
                    l.strip().split(':')[1][1:]
                ])
                continue 
            

            md_lines.append(l)
            continue 

        md_lines = md_lines[1:] # remove empty line after delimiter
        # turn into markdown
        generated_html_lines = md_to_html(md_lines)
        
        file.append([2] + ['CONTENT'] + generated_html_lines)



        # ASSUME nav bar is constant for now
        # make nav bar html compatible
        nav_left = [1, 'NAV']
        nav_right = [1, 'NAV-right']

        for thing in nav_bar_left:
            # format: (Descriptor, link, flag) 
            # flag = 0 -> relative; 1 -> absolute
            
            if thing[2] == 1:
                nav_left.append(f'<a href="{thing[1]}">{thing[0]}</a>')
                nav_left.append(nav_bar_delimiter)
                continue 
        
            if thing[2] == 0:
                # gonna assume we are at base level right now
                # NOTE: if subpages are involved, we are COOKED.
                nav_left.append(f'<a href="{thing[1]}">{thing[0]}</a>')
                nav_left.append(nav_bar_delimiter)
                continue

            raise ValueError(f"I'm not sure what a flag of {thing[2]} means when converting navbar files. See thing {thing} during file {file} when processing nav bar left.")
    
        nav_left.pop() # remove ending "|"

        # copy
        for thing in nav_bar_right:            
            if thing[2] == 1:
                nav_right.append(f'<a href="{thing[1]}">{thing[0]}</a>')
                nav_right.append(nav_bar_delimiter)
                continue 
        
            if thing[2] == 0:
                nav_right.append(f'<a href="{thing[1]}">{thing[0]}</a>')
                nav_right.append(nav_bar_delimiter)
                continue

            raise ValueError(f"I'm not sure what a flag of {thing[2]} means when converting navbar files. See thing {thing} during file {file} when processing nav bar right.")
        nav_right.pop()


        file.append(nav_left)
        file.append(nav_right)


        # insert file name
        file.insert(0, p[0])


        # ts is a messs
        file_infos.append(file)
        continue
    
    # okay!
    # file_infos should now be a really messy list of all html stuffs
    # now move to the html template, do a find and replace, then write to the final file

    os.chdir(path_to_templates)
    html_files = [] # schema: each item in it is a list of [file name, [<file content>]] (content to be directly written.)


    for fi in file_infos:
        f_name = fi.pop(0)[:-3] # [-3] to get rid of the ".md"

        template_name = ''
        # look through and find the template
        for t in fi:
            if type(t) != type([0]):
                # some random thing
                # theoretically this shouldn't be happening
                # too lazy to put an exception here
                continue

            if t[1] == 'TEMPLATE':
                template_name = t[2]
                break
        
        if template_name == '':
            raise ValueError(f"When trying to turn file {f_name} from .md to .html, no valid template for {f_name} was found!See below:\nFile dump: {file_infos}")
        

        template_exists = False 
        with os.scandir() as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():

                    # take first word
                    if entry.name.split('.')[0] == template_name:
                        # exists
                        template_exists = True
                        break
                    
                    continue 

        if not template_exists:
            raise ValueError(f"When turning {f_name}.md into a .html file, no valid template could be found!\nApparently, template name {template_name} does not exist. See logs below:\ncore dump: {file_infos}")
        
        # so template exists.
        # now do a find and replace on it -> anything with $$ delimiters will be cast aside
        

        html_content_file = []
        with open(f'{template_name}.html', 'r') as f:
            html_content_file = f.readlines()
        
        # now go through base_html_file line by line instead of file object; then modify that to fit content.

        # stack kinda thing
        # assume balanced bracket-style enclosures
        _cur_keyword = []
        for _ind, _line in enumerate(html_content_file):
            if len(_line.strip()) == 0:
                continue 
            
            if _line.strip()[:6] == '<!-- [' and _line.strip()[-5:] == '] -->':
                # get keyword and throw it on stack
                _cur_keyword.append(_line.strip()[6:-5])
                continue 

            if _line.strip()[:10] == '<!-- [end ' and _line.strip()[-5:] == '] -->':
                if (len(_cur_keyword) == 0) or (_cur_keyword[-1] != _line.strip()[10:-5]):
                    # yikes 
                    raise Exception(f"When processing {f_name}.md to .html, some brackets were not balanced!!\ncore dump: {file_infos}")
                
                _cur_keyword.pop()
                continue 
        
            if _line.strip()[0] == _line.strip()[-1] == '$' and _line.strip()[1:-1] in _cur_keyword:
                # find and replace
                # wlog the dollar sign thing is on its own line so i wont worry about weirdities

                # note: list 'fi' here still has all the info
                # of the form [int, name, kwargs]
                word = _line.strip()[1:-1]
                
                _content_ind = 0
                for _i, _v in enumerate(fi):
                    if _v[1] == word:
                        _content_ind = _i 
                        break
                
                _content = fi.pop(_content_ind)

                if _content[0] == 0:
                    # replaces the $delimiter$ with actual content
                    html_content_file[_ind] = _line.replace(f"${_content[1]}$", _content[2])
                    continue 

                if _content[0] == 1:
                    # nav bar.
                    _mega_string = ''
                    for _index in range(2, len(_content)):
                        _mega_string += _content[_index] + '\n'
                    
                    _mega_string = _mega_string[:-1] # remove last \n char
                    html_content_file[_ind] = _line.replace(f"${_content[1]}$", _mega_string)
                    continue 

                if _content[0] == 2:
                    # actual content lmao
                    # do same thing as above as it's basically exactly the same
                    _mega_string = ''
                    for _index in range(2, len(_content)):
                        _mega_string += _content[_index] + '\n'
                    
                    _mega_string = _mega_string[:-1] # remove last \n char
                    html_content_file[_ind] = _line.replace(f"$CONTENT$", _mega_string)
                    continue 

                raise ValueError(f"You shouldn't be here. Apparently, this find and replace thing that you have cannot be found to be replaced.\nFind and replace index: {_content[0]}\nFind and replace popped content:{_content}\nCore dump: {file_infos}")

            # this is just a normal line :)
            continue 
    
        html_files.append([f_name, html_content_file])



    os.chdir(path_templates_to_end_directory)
    for _name, _content in html_files:
        # check if path is vailablae
        if os.path.isfile(f'{_name}.html'):
            os.remove(f'{_name}.html')

        with open(f'{_name}.html', 'w') as f:
            for _item in _content:
                f.write(_item) # '\n's are already taken care of
    

    # we are done!
    print('All files succesfully (re)generated.')

    return 0




if __name__ == '__main__':
    print('\n')
    main()  



