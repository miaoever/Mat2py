#Mat2py 


Mat2py is short for Matlab to Python - a complier designed for translating matlab script into the code which may run in Python environment directly without any modification. 
<p>Now, it's consist of three main components:the lexer and parser for matlab script language, the code generator which generate corresponding python code. You may use some of these parts in your own project independently under the license.</p>

Notice: mat2py project is in a very early version, so any feedback is expecting :)

####Latest release: 0.1 (2013/08/19)

<br><br>
#Features
* Various methods for constructing matrix / vector
* Function / script (or combinded in one) file(s)
* Function declaration or call
* Expressions
* Assignments
* If statements
* Loop statement ( for / while )
* Plugin architecture for loading standard lib function dynamicly

#Usage
    # python ma2py.py source [target]
* source - the .m file you want to translate.
* \[target\](option) - the output file name , if you don't specify it, the target code will print out on the screen directly. 

#Requirement
* Python 2.7+
* Numpy\*

\* If you just want to translate the code without running it right now, the Numpy library is optional.

#License

The MIT License

Copyright (C) 2013 miaoo leo.miao.ever@gmail.com