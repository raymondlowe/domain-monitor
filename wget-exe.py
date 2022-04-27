# use wget.exe on windows to get files, so it behaves like requests.get but it 
# is actually windows wget.exe under the hood.
#
# handles some obscure ssl cases that wget can do but requests can't

# define a wgetGet function that takes a url and returns a response containig success or failure and the content of the url as a string

import subprocess
import os 
import tempfile
import sys

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    errorlevel = process.returncode
    if verbose:
        print(std_out.strip(), std_err)
    pass
    # if there is an error print it
    if errorlevel:
        print(f"errorlevel : {errorlevel}")
        return False
    return True # success

def wgetGet(url):

    # check is url a valid url
    if not url.startswith('http'):
        return False, ''
    
    with tempfile.TemporaryDirectory() as tmp:
        tempfilename = os.path.join(tmp, 'output.file')
        # use os to delete the output.file
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
        
        runcmdstr = f"wget -aasdf -O {tempfilename} {url}"
        if not runcmd(runcmdstr, verbose = False):
            return False, ''

        # check if the file exists
        if not os.path.isfile(tempfilename):
            return False, ''

        # get the content of the file
        with open(tempfilename, 'r') as f:
            content = f.read()
        # clean up the temp file

        
        # if content is empty then error
        if not content:
            return False, ''
        
        return True, content


# use __main__ to run a test if this file is run directly
if __name__ == '__main__':
    # if there is a url on the arguement line
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'https://www.example.com/'

    print(f"wgetting {url}")        
    success, content = wgetGet(url)
    if success:
        print(content)
    else:
        print('failed to get content')

