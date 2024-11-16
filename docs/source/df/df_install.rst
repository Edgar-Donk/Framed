=================
Using Pandas
=================

Install
=======

When working with data, often within a DataFrame, the library of choice is 
Pandas. Install Pandas::

    pip install pandas

Some OS already supply Pandas but before using the package check it is 
current::

    pip install -U pandas

One can use Anaconda, but there are over 100 packages, so one can control
the installation better by using Minicondas and install in a similar fashion 
to pip::

    conda install pandas

There are three plugins that may require installing, **dash**, **anyio** and 
**hypothesis**. If working with large amounts of data it is recommended to 
install **numexpr** for accelerating some numerical operations, and 
**bottleneck** for certain **nan** evaluations.

Other dependancies may be necessary but as a start ensure **matplotlib** and
**numpy** are present. If spreadsheet files are used for loading or saving 
**xlrd**, **xlwt** for xls files
or **openpyxl** for reading and writing xlsx files. When working with 
statistics **SciPy** may be required, although pandas has a useful collection 
of built-in functions.

**Seaborn** can quickly visualise data. Some of 
its built in functions blend in very nicely with Pandas, many of its built-in
tutorial examples are pandas' dataframes.

At a pinch the plotting functions of pandas itself can be used instead of
matplotlib.

Using Pandas
============

One can work with scripts but it is eminantly suitable to use interactively.
Some python IDEs (such as Idle and PyScripter) do not accept multiline inputs,
check on your IDE of choice. If using Jupyter remember to start it within
a directory that you have full control.

Open an OS command window, change to a user owned directory, then start with::

    jupyter lab

This opens a user website in your browser. After the startup procedure is 
complete it starts in a console. Select the upper tab with **+**, then select
the **notebook**.

Pandas works flexibly with the dataframes, if the command has no name (handle)
then nothing changes, but the results of that command is shown. 