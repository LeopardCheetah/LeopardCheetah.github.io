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

#############################################################


# known conversions to do:
# --- -> <hr /> (horizontal rule)

# ok let's parse!

import os
import os.path
import sys

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
            
            # there WILL need to be some markdown to html processing here
            # e.g. <h1s> <hr>, etc. 
            # for now just assume we can throw it in raw and call it a day
            # TODO: (restated) -- make everything below here HTML compatible

            # e.g. -- turn ## into headers, --- into horizontal bars, - into bullet points (of lists), etc.
            # follow the markdown specs 

            ctnt.append(l.strip())
            continue 
        
        file.append([2] + ['CONTENT'] + ctnt[1:])




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



