=================
Data Manipulation
=================

Rename Columns
==============

The columns can be renamed directly::

    df3.rename(columns = {"Product": "Computer Part"})
    df3
      Computer Part  Price
    0        Tablet    250
    1       Printer    100
    2        Laptop   1200
    3       Monitor    300
    4         Mouse     10

Use the pandas ``loc`` function to locate the required rows::

    df3.loc[df3['Product'] == 'Printer']
       Product  Price
    1  Printer    100

The method used a comparison, and returns the row data, 
this can be extended to use other comparisons. If the data has been 
cleaned one can make the search more flexible::

    df3[df3['Product'].str.contains('Printer')]
       Product  Price
    1  Printer    100

The relevant row can be located using the index::

    df3.loc[1, ['Price']] = [95]
    df3
          Product  Price
    0      Tablet    250
    1     Printer     95
    2      Laptop   1200
    3  UHD Screen    400

One can separately specify the condition::

    update = df3['Product'] == 'Printer'
    update
    0    False
    1     True
    2    False
    3    False

    df3.loc[update, ['Price']] = [105]
    df3
        Product  Price
    0      Tablet    250
    1     Printer    105
    2      Laptop   1200
    3  UHD Screen    400

**update** is only a handle or alias and not an action.

.. _wide:

Wide to Long Form
=================

Melt
----

Pandas **melt** is a generic command to change the format::

    df = pd.DataFrame({'team': ['A', 'B', 'C', 'D'],
                    'points': [88, 91, 99, 94],
                    'assists': [12, 17, 24, 28],
                    'rebounds': [22, 28, 30, 31]})

    #view DataFrame
    df

        team    points  assists rebounds
    0   A       88      12      22
    1   B       91      17      28
    2   C       99      24      30
    3   D       94      28      31

    #reshape DataFrame from wide format to long format
    df = pd.melt(df, id_vars='team', value_vars=['points', 'assists', 'rebounds'])

    df
    
        team    variable    value
    0   A       points      88
    1   B       points      91
    2   C       points      99
    3   D       points      94
    4   A       assists     12
    5   B       assists     17
    6   C       assists     24
    7   D       assists     28
    8   A       rebounds    22
    9   B       rebounds    28
    10  C       rebounds    30
    11  D       rebounds    31

The column **team** was the identifier, remaining a column in the long form,
whilst the former columns **points, assists and rebounds** became components 
of the new columns **variable and value**. The column names variable and value
can be customised::

    pd.melt(df, id_vars='team', value_vars=['points', 'assists', 'rebounds'],
        var_name='New_var', value_name='New_val')
    
       team   New_var  New_val
    0     A    points       88
    1     B    points       91
    2     C    points       99
    3     D    points       94
    4     A   assists       12
    5     B   assists       17
    6     C   assists       24
    7     D   assists       28
    8     A  rebounds       22
    9     B  rebounds       28
    10    C  rebounds       30
    11    D  rebounds       31

wide_to_long
------------

There is an explicit pandas command to change the data form from 
`wide to long <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html>`_ 

::

    np.random.seed(123)
    df = pd.DataFrame({"A1970" : {0 : "a", 1 : "b", 2 : "c"},
                   "A1980" : {0 : "d", 1 : "e", 2 : "f"},
                   "B1970" : {0 : 2.5, 1 : 1.2, 2 : .7},
                   "B1980" : {0 : 3.2, 1 : 1.3, 2 : .1},
                   "X"     : dict(zip(range(3), np.random.randn(3)))
                  })
                  
    df
    
        A1970   A1980   B1970   B1980   X           id
    0   a       d       2.5     3.2     -1.085631   0
    1   b       e       1.2     1.3     0.997345    1
    2   c       f       0.7     0.1     0.282978    2
    
    pd.wide_to_long(df, ["A", "B"], i="id", j="year")
    
                X           A   B
    id  year
    0   1970    -1.085631   a   2.5
    1   1970    0.997345    b   1.2
    2   1970    0.282978    c   0.7
    0   1980    -1.085631   d   3.2
    1   1980    0.997345    e   1.3
    2   1980    0.282978    f   0.1

All extra variables are left untouched. This simply uses pandas.melt under 
the hood, but is hard-coded to “do the right thing” in a typical case.

Long to Wide
============

pivot
-----

The long format can be made into a wide format by **pivot**::

    df
    
        team    New_var     New_val
    0   A       points      88
    1   B       points      91
    2   C       points      99
    3   D       points      94
    4   A       assists     12
    5   B       assists     17
    6   C       assists     24
    7   D       assists     28
    8   A       rebounds    22
    9   B       rebounds    28
    10  C       rebounds    30
    11  D       rebounds    31
    
    df=pd.pivot(df, index='team', columns='New_var', values='New_val')
    
    df
    
    New_var assists points  rebounds
    team
    A       12      88      22
    B       17      91      28
    C       24      99      30
    D       28      94      31

**team** became the index, the contents of **New_var** (points, assists and 
rebounds) became the new columns, whilst the contents of **New_val**, became
the values inside the dataframe.