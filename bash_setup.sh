basedir=`pwd`

echo PWD:  $basedir

export PATH toolsdir srcdir

toolsdir=$basedir

PATH=$toolsdir/nodejs-x86:$PATH
PATH=$toolsdir/putty/Putty-beta-0.65:$PATH
PATH=$toolsdir/PortableGit:$PATH
PATH=$toolsdir/WinPython-32bit-2.7.10.3:$PATH
PATH=$toolsdir/WinPython-32bit-2.7.10.3/Python-2.7.10:$PATH
PATH=$toolsdir/mosquitto:$PATH
PATH=$toolsdir/arduino-1.6.8:$PATH

echo --
echo Environment setup is complete 
echo --
srcdir=$basedir/../Dev

cd $srcdir

curr_dir=`pwd`

echo Current directory is set to $curr_dir 
echo --
echo Commands you can use include:
echo --
echo "arduino   to run the arduino IDE."
echo "putty     to connect to other machines."
echo "git-bash  to use git and do lots of other things."
echo "node      to run node-JS programs.  E.g.  node your_prog.js"
echo "idle      to run the python IDE."
echo "python    to run your python programs E.g. python your_program.py"
echo
echo "mosquitto_pub   to publish mqtt messages to a topic."
echo "mosquitto_sub   to subscribe to mqtt topics."
echo
echo "notepad   to write your source-code."
echo --
echo Please save your programs on the flash drive in $curr_dir
echo --
echo You are now ready to program!
