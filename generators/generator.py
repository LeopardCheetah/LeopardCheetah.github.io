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
path_to_end_directory = r'..\..' # go from template folder out to where you want the .html files to be

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
                    # you're cooked lmao
                    continue 

                with open(entry.name, 'r') as f:

                    lines = f.readlines()
                    files_lines.append((entry.name.strip(), lines))
                    continue 

                continue 
    
    # parse files_lines for juicy information
    # for now this is MANUAL but yeah this is todo otherwise

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
            
            # TODO: there WILL need to be some markdown to html processing here
            # e.g. <h1s> <hr>, etc. 
            # for now just assume we can throw it in raw and call it a day
            # TODO: (restated) -- make everything below here HTML compatible
            ctnt.append(l.strip())
            continue 
        
        file.append([2] + ctnt[1:])





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

    return 




if __name__ == '__main__':
    main()  



