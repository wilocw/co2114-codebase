"""CO2114_LAB02.PY

Use this file to edit your Python code and 
  try the exercises in Lab 02
"""


## Write your class definitions here


## 
def main():
    """ Main method for running script code """
    # write your non-class code here
    print("Hello World")


#################################
## DO NOT EDIT BELOW THIS LINE ##
##   UNLESS YOU KNOW WHAT YOU  ##
##     ARE DOING               ##
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="co2114_lab02")
    parser.add_argument("-d","--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        print("Demo")
        pass
    else:
        main()