import sys
import argparse
import subprocess
from colorama import init as colorama_init
colorama_init(autoreset=True)

def parse_argument():
    ''' Definition of arguments '''
    parser = argparse.ArgumentParser(prog="mozilla-download",description="Download the latest version of Mozilla Firefox and Mozilla Thunderbird and install it in the directory </opt> or the directory you indicate. you can also choose the language with the format <en-EN> , <es-ES> for example.")
    parser.add_argument("mozilla",type=str,help="Choose which one you want to download, Mozilla Firefox or Mozilla Thunderbird", choices=["firefox","thunderbird"])
    parser.add_argument("-d","--directory",type=str,help="Directory to install, by default </opt>",default="/opt") 
    parser.add_argument("-l","--lang",type=str,help="Language to download. by default <en-US>",default="en-US")
    args = parser.parse_args()
    download(args)
    
def download(args):
    ''' Download the latest version of Mozila '''
    # Collect the arguments
    mozilla=args.mozilla
    lang=args.lang
    if mozilla == "firefox":
        file="/tmp/firefox-latest.tar.bz2"
        # Order to download the latest Mozilla Firefox
        resu_down=subprocess.run(["wget","-O",f"{file}", "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang="f"{lang}"])
    elif mozilla == "thunderbird":
        file="/tmp/thunderbird-latest.tar.bz2"
        # Order to download the latest Mozilla thunderbird
        resu_down=subprocess.run(["wget","-O",f"{file}", "https://download.mozilla.org/?product=thunderbird-latest&os=linux64&lang="f"{lang}"])
    valores=check(resu_down)
    print(f"{valores[1]}{valores[0]}")
    if valores[2] == False:
        # Exit the app if there is a download error
        sys.exit(f"\033[31mERROR!, Installation could not be completed")
    install(file,args.directory,mozilla)

def install(file,directory,mozilla):
    ''' Install Mozilla in /opt or in the folder defined by the <-d> <--directory> argument '''
    resu_inst=subprocess.run(["tar","-xvf",f"{file}", "-C",f"{directory}"])
    valores=check2(resu_inst)
    # Print the result of the Mozilla installation
    print(f"{valores[1]}Mozilla {mozilla} {valores[0]}")
    
def check(resu_down):
    ''' Check if it downloaded successfully or failed '''
    if resu_down.returncode!=0: 
        return("Download Failed","\033[31m",False)
    else:  
        return("Successful Download","\033[32m",True)
        
def check2(resu_inst):
    ''' Check if it was installed correctly or failed '''
    if resu_inst.returncode!=0:
        return("Installation Failed","\033[31m")
    else:
        return("Installation Completed","\033[32m")

if __name__ == "__main__":
    parse_argument()

