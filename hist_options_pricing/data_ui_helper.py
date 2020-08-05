# Description: This script is just used to abstract uninteresting UI code that I don't want in the main codebase

import time

# just some printing / instructions to introduce the program
def intro_screen():
    print_sleep(3)
    print("*****************************************************************")
    print(" ")
    print("      Historical Options Pricing Chart Tool")
    print(" ")
    print("*****************************************************************")
    print("* Type 'exit' at any time to terminate program.")
    print_sleep(11)
    
def print_sleep(times):
    for i in range(times):
        print("*"); time.sleep(0.05)