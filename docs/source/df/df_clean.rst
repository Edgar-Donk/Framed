=============
Cleaning Data
=============

Before data cleaning check what state the dataframe is in::

    df.info()
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4 entries, 0 to 3
    Data columns (total 2 columns):
     #   Column   Non-Null Count  Dtype 
    ---  ------   --------------  ----- 
     0   Product  4 non-null      object
     1   Price    4 non-null      int64 
    dtypes: int64(1), object(1)
    memory usage: 192.0+ bytes

When cleaning data save to a new dataframe or overwrite the existing
dataframe, otherwise the result is lost. 
If you want to keep a working copy in memory
give the action a new name (df1, df2 ..), when you want to keep the result 
and overwrite the working dataframe save to the same name or add the parameter
**inplace=True** (this last command is discouraged). 

Right Character Set
^^^^^^^^^^^^^^^^^^^^

Python 3 works in the UTF-8 character set, if you experience errors associated
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 .... or something 
similar check that the file is actually UTF-8. The file may still be in ASCII.

When checking with **chardet** ensure that the program reads the contents
of the `file <https://stackoverflow.com/questions/54389780/using-chardet-to-detect-encoding>`_
and not the name of the file::

    with open('beer_list.csv') as f:
        print(f)
        
    <_io.TextIOWrapper name='beer_list.csv' mode='r' encoding='cp1252'>

"beer_list.csv" is stored on a windows machine, hence encoding='cp1252'::

    import chardet
    filecsv_list = ['beer_list.csv']
    
    for csv in filecsv_list:
        with open(csv,'rb') as f:
            data = f.read()  # or a chunk, f.read(1000000)
        encoding=chardet.detect(data).get("encoding")
        print(encoding)

        b=pd.read_csv(csv,encoding=encoding,header=None,sep=',',engine='python')
                    
    UTF-8-SIG

If the answer had returned 'iso-8859-1' (equivalent to latin-1) then it needs
converting. External sites may require **encoding='iso-8859-1'**, internal
files can be converted by most file editors.

Missing Values
^^^^^^^^^^^^^^

First check whether there are any missing values::

    df.isnull()
        Product  Price
    0    False  False
    1    False  False
    2    False  False
    3    False  False

This may be all that is required in a small dataframe, for a larger dataframe
use a summary query::

    df.isnull().sum()
    Product    0
    Price      0

On some dataframes there may be columns that are of little interest and can
be safely removed:: 

    df.dropna(subset=['column_name'], inplace=True)

If there is a reason to hold back then::
    df = df[df['column_name'].notna()]

Wrong Data Type
^^^^^^^^^^^^^^^^

See whether the data types correspond to the expected. Uncleaned data has
a lot of unassigned data type. The general catchall is **object** for 
anything not a number, which is assigned int64 or float64::

    df.dtypes
    Unnamed: 0     int64
    Product       object
    Price          int64
    dtype: object

Make a small dataframe with an error::

    data = {'a': [0, 1, 2, 'a'],
        'c': ['a', 'b', 'c', 'd']}
    dferr = pd.DataFrame(data)
    dferr
       a  c
    0  0  a
    1  1  b
    2  2  c
    3  a  d

    dferr.dtypes
    a    object
    c    object
    dtype: object

Both columns are object as they either have mixed dtypes or are characters.
Clean up column "a", if on a large dataframe it may not be so easy to spot::

    dferr['a'] = pd.to_numeric(dferr['a'], errors='coerce')
    dferr
        a  c
    0  0.0  a
    1  1.0  b
    2  2.0  c
    3  NaN  d
    
    dferr.dtypes
    a    float64
    c     object
    dtype: object

Column "a" now shows as float64, as the replacement **NaN** is a float type.

If the command raises a warning::

    SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead

    df.loc[pd.to_numeric(df['column_name'], errors='coerce').isna(), 'column_name']

Our original data had integers, a different replacement command is necessary::

    dferr['a'] = dferr['a'].replace(np.nan, -1).astype(np.int64)
    dferr
       a  c
    0  0  a
    1  1  b
    2  2  c
    3 -1  d
    
    dferr.dtypes
    a     int64
    c    object
    dtype: object

The numbers are now integers and the cleaned up data is **-1** which should
be different to the other valid entries.



Date Time Columns
^^^^^^^^^^^^^^^^^^

Whittle down those columns with object dtypes, using a similar cleanup command
to to_numeric above, clean up date columns::

    pd.to_datetime(df['date_col'], errors='coerce').isnull().value_counts()

This time we are counting the number of errors and successes that exist. Knowing
the dataframe size the result will show **False df_size** when everything
is correct and the number of errors **True err_size**. Also a new column will
be generated whilst searching for errors, this allows the old data to remain
in the original column while the new column will display the errors as NaT
(not a time).

.. sidebar:: Detecting False Dates

    The query shows whether an error occurred, therefore an error occurred
    or not it displays the opposite of a correct answer. Hence *False* should
    have a large number, if clean the same as the dataframe size, whereas
    *True* should be small the number of errors found.

Date time errors require a bit of unravelling. There can be errors caused by
the wrong format, pandas reads the year first, then month then day in default
mode. Since it is programmed in America it interprets 03-04-2021 as the 4th
March and not the 3rd of April:: 

    pd.to_datetime('2014-04-03')
    
    Timestamp('2014-04-03 00:00:00')

    pd.to_datetime('03-04-2014')
    
    Timestamp('2014-03-04 00:00:00')
    
    pd.to_datetime('03-04-2014', format='%d-%m-%Y')
    
    Timestamp('2014-04-03 00:00:00')

Pandas was shown the intention by **format**, unfortunately date and time formats
can vary from place to place, so the following is a summary of normally used
values

* %Y
    complete year (4 integers)
* %m
    month, zero padded (2 integers)
* %d
    day, zero padded (2 integers)
* %H
    hour, 24 hour zero padded (2 integers)
* %M
    minute, zero padded (2 integers)
* %S
    second, zero padded (2 integers)

The dates are separated by hyphens the times by full colons with a space between
the date and time. Other formats can be used, see the `datetime table <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>`_
for a full list of the many other possibilities.

Start off with a dictionary containing some errors to correct::

    # create a dataframe
    df = pd.DataFrame({
        'Date': ['2021-02-29','2021-04-02','03-04-2021','2021-04-04','2021-04-05'],
        'Units Sold': [120, 123, 150, 160, 140]
    })
    
    df
                 Date  Units Sold
        0  2021-02-29         120
        1  2021-04-02         123
        2  03-04-2021         150
        3  2021-04-04         160
        4  2021-04-05         140

    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5 entries, 0 to 4
    Data columns (total 2 columns):
    #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
    0   Date        5 non-null      object
    1   Units Sold  5 non-null      int64 
    dtypes: int64(1), object(1)
    memory usage: 208.0+ bytes

    # change data type to datetime
    df['Date'] = pd.to_datetime(df['Date'])

Creates a pile of error statements, finishing off with::

    dateutil.parser._parser.ParserError: day is out of range for month: 
    2021-02-29 present at position 0

This detected the false date in the first line::

    pd.to_datetime(df['Date'], errors='coerce').isnull().value_counts()
    False    4
    True     1
    Name: Date, dtype: int64

Confirms the finding, 4 not null values, 1 false line. With a small dataframe
one can view and rectify easily. On a larger dataframe create a separate
column with the corrected datetimes::

    df['correct'] = pd.to_datetime(df['Date'],errors='coerce')
    df
             Date  Units Sold    correct
    0  2021-02-29         120        NaT
    1  2021-04-02         123 2021-04-02
    2  03-04-2021         150 2021-03-04
    3  2021-04-04         160 2021-04-04
    4  2021-04-05         140 2021-04-05

Although the column **correct** has the right value **NaT** for the first
line the change in date on the third line might have slipped in unnoticed.
Add **format** to the date, then any differences will be hightlighted and
can be tackled accordingly::

    df['correct'] = pd.to_datetime(df['Date'], format='%Y-%m-%d',errors='coerce')
    df
             Date  Units Sold    correct
    0  2021-02-29         120        NaT
    1  2021-04-02         123 2021-04-02
    2  03-04-2021         150        NaT
    3  2021-04-04         160 2021-04-04
    4  2021-04-05         140 2021-04-05

In a larger dataframe it is impractical to find the errors by inspection,
use a query to find the errors::

    df[df['correct'].isna()]
             Date  Units Sold correct
    0  2021-02-29         120     NaT
    2  03-04-2021         150     NaT

Now the index numbers are known it is straightforward to change the **Date**
to correct the errors::

    df.at[0, 'Date'] = '2021-02-28'
    df.at[2, 'Date'] = '2021-04-03'
    df
             Date  Units Sold    correct
    0  2021-02-28         120        NaT
    1  2021-04-02         123 2021-04-02
    2  2021-04-03         150        NaT
    3  2021-04-04         160 2021-04-04
    4  2021-04-05         140 2021-04-05
    
    df['correct'] = pd.to_datetime(df['Date'], format='%Y-%m-%d',errors='coerce')
    df
             Date  Units Sold    correct
    0  2021-02-28         120 2021-02-28
    1  2021-04-02         123 2021-04-02
    2  2021-04-03         150 2021-04-03
    3  2021-04-04         160 2021-04-04
    4  2021-04-05         140 2021-04-05

The dataframe is now ready to accept the dtype conversion of the Date
column::

    df['Date'] = pd.to_datetime(df['Date'])
    df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5 entries, 0 to 4
    Data columns (total 3 columns):
    #   Column      Non-Null Count  Dtype         
    ---  ------      --------------  -----         
    0   Date        5 non-null      datetime64[ns]
    1   Units Sold  5 non-null      int64         
    2   correct     5 non-null      datetime64[ns]
    dtypes: datetime64[ns](2), int64(1)
    memory usage: 248.0 bytes

The dtype for datetime is **datetime64(ns)**, where ns refers to nanoseconds.
Now the dataframe can be cleaned up by removing the **correct** column and 
saving.

Currency Symbols
^^^^^^^^^^^^^^^^

Pandas does not handle currency signs, so where necessary replace the local
currency symbol with an empty value::

    data = {'Cost': ['€100', '€150', '€200', '€250'],
        'Item': ['a', 'b', 'c', 'd']}
    dferr = pd.DataFrame(data)
    dferr
        Cost Item
    0  €100    a
    1  €150    b
    2  €200    c
    3  €250    d
    dferr.dtypes
    Cost    object
    Item    object
    dtype: object

    dferr['Cost'] = dferr['Cost'].str.replace('€','')
    
    dferr
      Cost Item
    0  100    a
    1  150    b
    2  200    c
    3  250    d
    
    dferr.dtypes
    Cost    object
    Item    object
    dtype: object

The **Cost** column is still an object, convert to integer::

    dferr['Cost'] = dferr['Cost'].astype(int)
    dferr.dtypes
    Cost     int32
    Item    object
    dtype: object

.. note:: astype()

    Only specify int, not int32, float is similar only use float
    not float64.

Thousand Delimiters
^^^^^^^^^^^^^^^^^^^^

Columns that show integers might have various delimiters to show thousands.
It is easiest to remove delimiters and only show when displaying. Integers 
are hard coded not to allow delimiters. Under normal circumstances loading
data directly with a dictionary does not allow delimiters.

Using a similar method to datetime, check whether the column has any 
disallowed numeric values. This time 'Price' shows as an object::

    df = pd.read_csv("file4.csv", sep=";")
    df
          Product     Price
    0      Tablet    250.00
    1     Printer    105.00
    2      Laptop  1,200.00
    3  UHD Screen    400.00
    
    df.dtypes
    Product    object
    Price      object
    
    print(pd.to_numeric(df['Price'], errors='raise'))
    
    ...
    ValueError: Unable to parse string "1,200.00"
    ...
    ValueError: Unable to parse string "1,200.00" at position 2

An error is produced together with its position - we already know it's in
the column 'Price'::

    df['Price'] = df['Price'].str.replace(',','')
    df['Price'] = df['Price'].astype(float)
    
    df.dtypes
    Product     object
    Price      float64

Categories
^^^^^^^^^^

Check for columns with a few known values - maybe these columns are not so 
relevant and can be deleted. With a large dataframe find these
columns, and check that all values are in place, like the following
small example. First load the dataframe, show it and then call its info::

    dfb = pd.read_csv("beer_list.csv", sep=";")
    dfb
                  Beer Type Ferment Type    OE°P  ...  FP°C  TMD°C  Gravity
    0             Topvar 10       bottom    10.0  ... -2.11   2.94        P
    1             Topvar 12       bottom    12.0  ... -2.49   2.68        P
    2   Pilsner Urquelle 10       bottom    10.0  ... -2.04   2.69        P
    3   Pilsner Urquelle 12       bottom    12.0  ... -2.36   2.18        P
    4       Zlaty Bazant 10       bottom    10.0  ... -2.04   2.69        P
    5           Heavy Czech       bottom    13.6  ... -2.40   1.03        P
    6              Bitter 1          top  1030.9  ... -1.51   2.60        B
    7              Bitter 2          top  1045.3  ... -2.19   2.20        B
    8                Mild 1          top  1030.7  ... -1.35   2.02        B
    9                Mild 2          top  1036.5  ... -1.77   2.42      NaN
    10      Zlaty Bazant 12       bottom    12.0  ... -2.36   2.18      NaN

    [11 rows x 13 columns]
    
    dfb.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 11 entries, 0 to 10
    Data columns (total 13 columns):
     #   Column              Non-Null Count  Dtype  
    ---  ------              --------------  -----  
     0   Beer Type           11 non-null     object 
     1   Ferment Type        11 non-null     object 
     2   OE°P                11 non-null     float64
     3   AbV%                11 non-null     float64
     4   AbW%                11 non-null     float64
     5   DoF%                11 non-null     float64
     6   TE°P                11 non-null     float64
     7   AE°P                11 non-null     float64
     8   Wort Density kg/m³  11 non-null     float64
     9   Beer Density kg/m³  11 non-null     float64
     10  FP°C                11 non-null     float64
     11  TMD°C               11 non-null     float64
     12  Gravity             9 non-null      object 
    dtypes: float64(10), object(3)
    memory usage: 1.2+ KB

    dfb['Ferment Type'].nunique()
    2
    dfb['Ferment Type'].value_counts()
    bottom    7
    top       4
    Name: Ferment Type, dtype: int64

In the column **Ferment Type** the count of unique entries is 2 (function
``nunique()``), value_counts 
totals 11 which equals the number of rows, so this row requires no adjustment. 
Try the same with the column **Gravity**::

    dfb['Gravity'].nunique()
    2
    dfb['Gravity'].value_counts()
    P    6
    B    3
    Name: Gravity, dtype: int64

    dfb['Gravity'].isnull().values.any()
    True
    dfb['Gravity'].isnull().sum()
    2
    dfb['Gravity'].isnull()
    0     False
    1     False
    2     False
    3     False
    4     False
    5     False
    6     False
    7     False
    8     False
    9      True
    10     True
    Name: Gravity, dtype: bool

Once again in **Gravity** column the count of unique entries is 2, but the 
value_counts are 6 and 3, only 9 rows filled out of 11. The **Beer Type** is not 
alphabetical so use the index to find the row. The previous 3 commands confirm
what we already know, the last, **dfb['Gravity'].isnull()**, is closer to 
what we require, but is
impractical for a larger dataframe::

    dfb[dfb['Gravity'].isna()]
              Beer Type Ferment Type    OE°P  ...  FP°C  TMD°C  Gravity
    9            Mild 2          top  1036.5  ... -1.77   2.42      NaN
    10  Zlaty Bazant 12       bottom    12.0  ... -2.36   2.18      NaN

    [2 rows x 13 columns]

That's better! We now have just the rows where there are empty inputs in the 
target column. In case you were wondering there are 13 columns, hidden 
columns are not as relevant as the index, name and the target column. When
constructing a dataframe it is important to have the columns with names 
first, close to the index.

Looking at row 9, 'Gravity' we have a value of "NaN"::
    
    dfb.at[9, 'Gravity']
    NaN

as does the next row. Since row 9 is 'Beer Type' Mild 2 Gravity would be in
British units, and row 10 is Zlaty Bazant 12 the Gravity would be in P. 
Update the values. 

    dfb.at[9, 'Gravity'] = 'B'
    
    dfb.at[10, 'Gravity'] = 'P'

.. sidebar:: Alternative Index

    If Beer Type had unique values then it could have been made into an
    index in which case our modified commands would have been::
    
        dfb.at['Mild 2', 'Gravity'] = 'B'
        dfb.at['Zlaty Bazant 12', 'Gravity'] = 'P'

When working with single cells use **at** or **iat**, these are similar to
**loc** and **iloc** when working with rows or columns.

There is still work to be done on the columns **Ferment Type** and **Gravity**
even after all empty inputs are rectified. These columns have limited values
and we can let pandas autodetect all these values in declared columns::

    dfb["Ferment Type"] = pd.Categorical(dfb["Ferment Type"])
    dfb["Gravity"] = pd.Categorical(dfb["Gravity"])

Check on what changes if any have occurred::

    dfb.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 11 entries, 0 to 10
    Data columns (total 13 columns):
    #   Column              Non-Null Count  Dtype   
    ---  ------              --------------  -----   
    0   Beer Type           11 non-null     object  
    1   Ferment Type        11 non-null     category
    2   OE°P                11 non-null     float64 
    3   AbV%                11 non-null     float64 
    4   AbW%                11 non-null     float64 
    5   DoF%                11 non-null     float64 
    6   TE°P                11 non-null     float64 
    7   AE°P                11 non-null     float64 
    8   Wort Density kg/m³  11 non-null     float64 
    9   Beer Density kg/m³  11 non-null     float64 
    10  FP°C                11 non-null     float64 
    11  TMD°C               11 non-null     float64 
    12  Gravity             11 non-null     category
    dtypes: category(2), float64(10), object(1)
    memory usage: 1.3+ KB

The non-null count in Gravity has been eliminated and the column type has
changed from object to category. On a larger dataframe memory 
savings would also be seen::

    dfb['Beer Type'].dtype
    dtype('O')
    
    dfb['Ferment Type'].dtype
    CategoricalDtype(categories=['bottom', 'top'], ordered=False)
    dfb['Gravity'].dtype
    CategoricalDtype(categories=['B', 'P'], ordered=False)

Smaller Types
^^^^^^^^^^^^^^

Often the numerical data type is stored in a much larger format than 
necessary. In the dataframe dfb there are 10 numeric columns stored as 
float64, in this instance the storage type can be changed without any loss::

    float64_cols = list(dfb.select_dtypes(include='float64'))
    dfb[float64_cols] = dfb[float64_cols].astype('float32')

alternatively::

    import numpy as np
    dfb[dfb.select_dtypes(np.float64).columns] = 
        dfb.select_dtypes(np.float64).astype(np.float32)

    dfb.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 11 entries, 0 to 10
    Data columns (total 13 columns):
    #   Column              Non-Null Count  Dtype   
    ---  ------              --------------  -----   
    0   Beer Type           11 non-null     object  
    1   Ferment Type        11 non-null     category
    2   OE°P                11 non-null     float32 
    3   AbV%                11 non-null     float32 
    4   AbW%                11 non-null     float32 
    5   DoF%                11 non-null     float32 
    6   TE°P                11 non-null     float32 
    7   AE°P                11 non-null     float32 
    8   Wort Density kg/m³  11 non-null     float32 
    9   Beer Density kg/m³  11 non-null     float32 
    10  FP°C                11 non-null     float32 
    11  TMD°C               11 non-null     float32 
    12  Gravity             11 non-null     category
    dtypes: category(2), float32(10), object(1)
    memory usage: 926.0+ bytes

The memory use has gone down.

A similar method can be used to change int64 to int32.

Invalid Data
^^^^^^^^^^^^

Continuing with data cleanup, invalid data is even more of a headache than
non-existing data. If the data does not exist it can be readily detected and
updated, replaced or dropped. First where we have columns with the wrong 
type has been inserted should be straightforward in the Categorical types.
Help with numeric data comes with statistical information, first set the
display output to show all the rows::

    pd.set_option('display.max_columns', None)
    dfb.describe()
                  OE°P       AbV%       AbW%       DoF%         TE°P         AE°P  \
    count    11.000000  11.000000  11.000000  11.000000    11.000000    11.000000   
    mean    383.909091   4.284545   3.419091  64.570909   371.301818   368.437273   
    std     516.889786   0.901902   0.723194   5.812398   509.667698   508.073459   
    min      10.000000   2.500000   1.990000  52.120000     2.960000     1.340000   
    25%      11.000000   3.950000   3.150000  62.435000     3.455000     1.730000   
    50%      12.000000   4.500000   3.590000  65.870000     4.270000     2.480000   
    75%    1030.800000   4.965000   3.965000  68.360000  1012.800000  1008.100000   
    max    1045.300000   5.400000   4.320000  71.490000  1016.200000  1011.300000   

           Wort Density kg/m³  Beer Density kg/m³       FP°C      TMD°C  
    count           11.000000           11.000000  11.000000  11.000000  
    mean           946.946364          917.256364  -2.056364   2.330000  
    std            313.806788          303.900661   0.372995   0.517958  
    min              1.050000            1.010000  -2.490000   1.030000  
    25%           1033.700000         1006.665000  -2.360000   2.180000  
    50%           1040.030000         1007.640000  -2.110000   2.420000  
    75%           1046.835000         1009.670000  -1.905000   2.685000  
    max           1055.130000         1016.730000  -1.350000   2.940000

Obviously British and Continental units cannot be mixed, so the beer types
should have been separated, as different dataframes or additional rows used,
whichever is appropriate.

.. sidebar:: Change the Display Limits

    The option for more columns has been already used::
    
        pd.set_option('display.max_rows', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', -1)

Splitting the Dataframe
^^^^^^^^^^^^^^^^^^^^^^^^

Update **Zlaty Bazant 12** to continental units.
Remove the British beers, then the continental ones, save to separate pickle 
files::

    dfc = dfb.drop(dfb[dfb.Gravity == 'B'].index)
    dfc
                  Beer Type Ferment Type  OE°P  AbV%  AbW%       DoF%  TE°P  AE°P  \
    0             Topvar 10       bottom  10.0  4.50  3.59  71.489998  2.96  1.34   
    1             Topvar 12       bottom  12.0  5.40  4.32  71.080002  3.63  1.69   
    2   Pilsner Urquelle 10       bottom  10.0  4.30  3.43  68.360001  3.28  1.73   
    3   Pilsner Urquelle 12       bottom  12.0  5.00  3.99  65.870003  4.27  2.48   
    4       Zlaty Bazant 10       bottom  10.0  4.30  3.43  68.360001  3.28  1.73   
    5           Heavy Czech       bottom  13.6  4.93  3.94  57.450001  6.03  4.26   
    10      Zlaty Bazant 12       bottom  12.0  5.00  3.99  65.870003  4.27  2.48   

        Wort Density kg/m³  Beer Density kg/m³  FP°C  TMD°C Gravity  
    0          1040.030029         1005.219971 -2.11   2.94       P  
    1          1048.369995         1006.590027 -2.49   2.68       P  
    2          1040.030029         1006.739990 -2.04   2.69       P  
    3          1048.369995         1009.690002 -2.36   2.18       P  
    4          1040.030029         1006.739990 -2.04   2.69       P  
    5          1055.130005         1016.729980 -2.40   1.03       P  
    10         1048.369995         1009.690002 -2.36   2.18       P

    dfc.to_pickle('beer_list_cont')
    
    dfb.drop(dfb[dfb.Gravity == 'P'].index, inplace=True)
    dfb
      Beer Type Ferment Type         OE°P  AbV%  AbW%       DoF%         TE°P  \
    6  Bitter 1          top  1030.900024   3.0  2.39  61.889999  1011.900024   
    7  Bitter 2          top  1045.300049   4.6  3.67  64.809998  1016.200012   
    8    Mild 1          top  1030.699951   2.5  1.99  52.119999  1014.799988   
    9    Mild 2          top  1036.500000   3.6  2.87  62.980000  1013.700012   

              AE°P  Wort Density kg/m³  Beer Density kg/m³  FP°C  TMD°C Gravity  
    6  1007.599976         1030.900024         1007.640015 -1.51   2.60       B  
    7  1009.599976         1045.300049         1009.650024 -2.19   2.20       B  
    8  1011.299988         1030.699951         1011.260010 -1.35   2.02       B  
    9  1008.599976         1036.500000         1008.549988 -1.77   2.42       B

    dfb.to_pickle('beer_list_brit')

When retrieving the data from the pickle files note that the original indexing
is in place, as are the float32 and categorized columns. If saved in csv then
remember to switch off the index when saving, as a new index will be made
when reloaded. Remember that columns will lose their categorisation and 
numbers will be the highest type.
