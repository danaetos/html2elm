# html2elm.py


## Purpose
Manually converting a piece of DOM written in HTML into an elm function is error-prone and cumbersome. The purpose of this little script therefore is to automate the process. It takes a well-formed piece of HTML and turns it into an HTML node (an Html Msg) that you can drop straight into your elm code. 

## Caveats
The script parses a number of basic attributes such as class, id, placeholder but does not attempt to make sense of event handlers or styles attributes. Use it to generate the basic elm scaffold, and insert anything else (such as elm messages) later.

## Usage

> usage: html2elm.py [-h] [--t T] [--i I]
> 
> convert snippets of html to elm functions
> 
> optional arguments:
>   -h, --help  show this help message and exit
>   --t T       input html
>   --i I       input file
 

