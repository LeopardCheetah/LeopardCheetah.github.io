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


# ok let's parse!

import os
import os.path





# in: list of strings representing the content in a md file (line by line)
# out: list of strings representing the content of an html file (line by line)
# do NOT worry about adding \n characters to the end

# note: this will NOT 100% accurately convert every single md file into html. don't count on that.
def md_to_html(md):
    # remove ending '\n' from each line in md
    
    _md = []
    for _l in md:
        _md.append(_l[:-1])
    
    # last line doesn't have a newl char
    if md[-1][-1] != '\n':
        _md[-1] += md[-1][-1]


    _div_stack = [] # stack of open divs 
    
    html = ['']
    global whitespace_chars
    _in_code_block = False
    _in_list, _was_in_list = False, False # in unordered list, prev iteration was also in said list.

    for line_ind, line in enumerate(_md):
        hline = line # line after being html'd

        if '```' not in line and _in_code_block:
            html.append(line)
            continue 

        # ???
        if len(line) == 0 or len(line.strip()) == 0:
            _in_list = False 
            if _was_in_list:
                html.append('</ul>')
                _was_in_list = False

            if len(_div_stack) and _div_stack[-1] == 'p':
                _div_stack.pop()
                html.append('</p>')
                continue 
            continue



        # check if its an hr
        # aka (***)/(___) (not --- here)
        if line.strip() == '*'*len(line.strip()) or line.strip() == '_'*len(line.strip()):
            _in_list = False 
            if _was_in_list:
                html.append('</ul>')
                _was_in_list = False

                
            # add hr and call it a day
            # unpop all divs rq
            s = ''
            while len(_div_stack):
                s += f'</{_div_stack.pop()}>'

            html.append(s)
            html.append('<hr />')
            continue 

        
        # check if it's those stupid ---- headers or something
        # if it is a header from === flag will be 1; if its from ---- flag will be 2
        # otherwise flag = 0
        # flag = 3 -> indecisive
        flag = 3
        # dont write stupid md files
        for c in hline:
            if flag == 3 and c in whitespace_chars:
                continue 

            if flag == 3 and c == '=':
                flag = 1
                continue 

            if flag == 3 and c == '-':
                flag = 2
                continue 

            if flag == 3:
                flag = 0 
                break

            if flag == 1 and (c != '=' and c not in whitespace_chars):
                flag = 0 
                break
            
            if flag == 2 and (c != '-' and c not in whitespace_chars):
                flag = 0
                break

        if flag == 3 or (flag == 1 and not hline.count('===')) or (flag == 2 and not hline.count('---')):
            flag = 0


        # replace line above with a header version
        if flag and line_ind and not _in_code_block:
            if len(html) > 5:
                if html[-1][0] == '<' and html[-1][1] == 'h' and html[-1][3] == '>' or html[-1].strip() == '</p>':
                    # already a header, pass
                    # might actually be a hr
                    
                    if flag == 2:
                        html.append('<hr />')
                        continue 

                    html.append('') # spacers are good
                    continue 
            
            # remove the <p> tag if that's lurking in here
            if html[-1][:3] == '<p>':
                html[-1] = html[-1][3:]
                if _div_stack.pop() != 'p': # ASSUMING this is a p tag
                    # fail hard
                    print('Critical WARNING!!!!')
                    print(f'On md file with contents {md}, could not render line {line_ind} because of some weird open divs!!')
                    print(f'Please inspect the html for said file before use.')
                    print()


            # turn the text above into a header.
            html[-1] = f'<h{flag}>{html[-1]}</h{flag}>'
            html.append('')
            continue 


        # check if we block quoting or not 
        # sorry about the if-statement nesting
        if '>' in hline:
            

            # check if theres a space after (e.g. "> xyz" vs ">xyz")
            if len(hline) > hline.index('>') + 1 and hline[hline.index('>') + 1] == ' ':
                flag = 1
                # check to make sure  everything b4 '>' is whitespace
                for c in hline:
                    if c == '>':
                        break

                    if c not in whitespace_chars:
                        flag = 0
                        break

                    continue 

                if flag and not _in_code_block:
                    # first remove the "> " from the thing
                    # then add approproatie flags

                    # count = 1
                    hline = f'<blockquote>{hline.replace("> ", "", 1)}</blockquote>'

        
            
        # check if in list - the bullet point and the space
        _in_list = len(hline.strip()) > 2 and hline.strip()[0] in ['-', '+', '*'] and hline.strip()[1] == ' '
        if _in_list:
            hline = hline[2:] # remove bullet point + space preceding
        
        if _was_in_list and not _in_list:
            # end the list :(
            html.append(f'</ul>')
            _was_in_list = False 
            # no continue since this code gotta continue on with the execution


        #########################
        # basic text processing #
        #########################
        # turn `` into code, ** into bold/it/both, etc.
        # also turn double/triple dashes into em dashes


        # asterisk replacement (manual)
        _hline = ''
        _str_ind = -1
        _strong_em = 0 # 0 for none, 1 for strong open, 2 for em open, 3 for both open
        _code = 0 # 0 for closed, 1 for open
        _s = 0 # chars to skip

        

        for v in hline:
            _str_ind += 1
            if _s > 0:
                _s -= 1
                continue 

            if v == '`':
                # NOTE: this has limitations.
                # at this point however, it's whatever
                if _str_ind > 0 and hline[_str_ind - 1] == '\\':
                    _hline += '`'
                    continue 


                if len(hline) > _str_ind + 2 and hline[_str_ind + 1] == hline[_str_ind + 2] == '`':
                    # yikes, this seems to be a code fence.
                    # let's just leave it be 
                    _s = 2 

                    if not len(_div_stack) or (len(_div_stack) and _div_stack[-1] != 'pre'):
                        _hline += '<pre><code>'
                        _div_stack.append('pre')
                        _in_code_block = True 
                        continue 
                    
                    _div_stack.pop()
                    _hline += '</code></pre>'
                    _in_code_block = False
                    

                    continue 

                if _code:
                    _hline += '</code>'
                    _code = 0
                    continue 

                _code = 1
                _hline += '<code>'
                continue 

                    
            if _in_code_block:
                _hline += v
                continue 
            

            if v == '*':
                if _str_ind and hline[_str_ind - 1] == '\\':
                    _hline += '*'
                    continue 

                # actual thing happening
                # figure out what we got
                if len(hline) > _str_ind + 2 and hline[_str_ind + 1] == hline[_str_ind + 2] == '*':
                    # 3!
                    _s = 2 # skip the two asterisks
                    if _strong_em == 0:
                        # open both
                        _strong_em = 3
                        _hline += '<em><strong>'
                        continue 

                    if _strong_em == 1:
                        _strong_em = 2
                        _hline += '</strong><em>'
                        continue 

                    if _strong_em == 2:
                        _strong_em = 1
                        _hline += '</em><strong>'
                        continue 

                    if _strong_em == 3:
                        _strong_em = 0
                        _hline += '</strong></em>'
                        continue 

                    # ??
                    continue 

                if len(hline) > _str_ind + 1 and hline[_str_ind + 1] == '*':
                    _s = 1
                    if _strong_em % 2: # if 1 or 3, aka strong is open
                        _strong_em -= 1
                        _hline += '</strong>'
                        continue 

                    _strong_em += 1
                    _hline += '<strong>'
                    continue 

                # 1 char
                if _strong_em // 2:
                    _strong_em -= 2
                    _hline += '</em>'
                    continue 
                
                _strong_em += 2
                _hline += '<em>'
                continue 

            # NOTE: maybe excape some characters here.

            _hline += v
            continue 
        
        if not _in_code_block:
            _b = False
            while '~~' in _hline:
                _b = not _b 

                if _b:
                    # add <s>
                    _hline = _hline.replace('~~', '<s>', 1)
                    continue 

                _hline = _hline.replace('~~', '</s>', 1)
                continue                 
            
            if _b:
                # yikes, let's close the strikethoguh
                _hline += '</s>'


            # &#8211; | &ndash; || &#8212; | &mdash;
            # em/en dash replacement
            _hline = _hline.replace('---', '&mdash;')
            _hline = _hline.replace('--', '&ndash;')


        hline = _hline 

        ########### end basic text processing ###############


        #### process links #######

        # part 1: check to see if theres anything of the form [a](b)
        # part 2: convert to links
        _link_indices = [] 
        for i, v in enumerate(list(hline)):
            if v == '[' and len(_link_indices) % 4 == 0:
                _link_indices.append(i)
                continue 

            if v == ']' and len(_link_indices) % 4 == 1:
                if len(hline) > i + 1 and hline[i + 1] == '(':
                    _link_indices.append(i) 
                    _link_indices.append(i + 1)
                    continue 
                
                _link_indices.pop() # remove the last element in the list
                continue 
            
            if len(_link_indices) % 4 == 3 and v == ')':
                _link_indices.append(i)
                continue 

            continue 

        _link_indices = _link_indices[:(len(_link_indices) // 4)*4] # get rid of last n (n < 4) elements if they exist (the ones hanging on)

        # process each link index thing.
        # wlog if indices i < j, then l[i] < l[j].
        
        # do from BACK TO FRONT. (else string indices get fucked)
        for i in range(len(_link_indices) // 4):
            # 4*(max_i - i) + 0/1/2/3. 
            _sq_br_l = _link_indices[len(_link_indices) - 4*(1 + i)]
            _sq_br_r = _link_indices[len(_link_indices) - 4*(1 + i) + 1]
            _par_r = _link_indices[len(_link_indices) - 4*(1 + i) + 3]


            _ref_text = hline[_sq_br_l + 1:_sq_br_r]
            _link = hline[_sq_br_r + 2:_par_r]

            # essentially, replace the whole part of hl
            # indices to replace are from sq_br_l to _par_r onwards
            # +1 for the parentheses.
            hline = hline[:_sq_br_l] + f'<a href="{_link}">{_ref_text}</a>' + hline[_par_r + 1:]  
            continue 


        #### end link processing #######


        # check header
        flag = 0 
        for i in range(1, 7):
            if hline.strip()[:i] == i*'#' and hline.strip()[i] == ' ':
                flag = i # got the header
                break
        
        if flag:
            # lowkey there might be an open <p>
            # let's close that 
            if len(_div_stack) and _div_stack[-1] == 'p':
                _div_stack.pop()
                html.append('</p> ')
            
            if len(_div_stack) and _div_stack[-1] == 'pre':
                # ignore
                pass 
            else:
                html.append(f'<h{flag}>{hline[flag+1:]}</h{flag}>')
                continue 
            

        


        # assume all emblishments (italics, line breaks, bullets) are added
        # check if in list and stuffs
        if _in_list and not _was_in_list: # start a list!
            html.append(f'<ul>')
            html.append(f'<li>{hline}</li>')
            
            _was_in_list = True 
            continue 
    
        if _in_list and _was_in_list: # continue the list!
            html.append(f'<li>{hline}</li>')
            # was in list is true and remains true
            continue 


        # assume you just want a plain old paragraph
        # :D
        if len(_div_stack) == 0:
            if '</pre>' in hline:
                # yikes; push with caution
                html.append(f'{hline}')
                continue 
            
            # push 
            _div_stack.append('p')
            html.append(f'<p>{hline}')
            continue 

        if _div_stack[-1] == 'p' and len(_div_stack) == 1:
            _div_stack.pop()
            # nice, just add in the text that you have

            # with a line break (maybe, go search for it)
            if len(_md[line_ind - 1]) < 3:
                if _md[line_ind - 1][-2:] == '  ' or _md[line_ind - 1][-2:] == r'\\' or md[line_ind - 1][-1][-3:] == r'\\ ': # add in a line break
                    html.append('<br>')

            html.append(f'{hline}</p>')
            continue 

        # awkward
        # last div was NOT a p
        # gotta close that i guess


        # 2nd chance
        if _div_stack[-1] == 'pre' and len(_div_stack) == 1:
            # _div_stack.pop()
            # we still in this codeblock together gang
            html.append(f'{hline}')
            continue 
        

        # clear out whatever abomination is happening
        print('Warning!! -- something weird is happening')
        print(f'trying to make p object on line {line_ind} with the line text being {line} but there\'s some stuff in the way')
        print()
        print(_div_stack)
        print()

        for i in range(len(_div_stack)):
            
            # do back to front
            html.append(f'</{_div_stack[-(i + 1)]}> ')
            _div_stack = []
        
        html.append('')
        # add our own paragraph
        html.append(f'<p>{hline}</p>')

        continue 



    # cleanup + close any remaining divs.
    while len(_div_stack) > 0:
        html.append(f'</{_div_stack.pop()}> ')


    return html + ['']


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
    print('\n------------------------------------')
    main()  



