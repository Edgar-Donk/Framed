===========
Saving Data
===========

When using any of the previous pandas examples none of the changes have been 
saved to disk as pandas is running in memory. If one needs 
a temporary saving then use **pickle**, all 
data types are retained together with cleaning actions, by contrast csv files
will lose the data types::

    df3.to_pickle("my_data.pkl")

Then in a subsequent session::

    import pandas as pd
    
    df3= pd.read_pickle("my_data.pkl")
    df3
          Product  Price
    0      Tablet    250
    1     Printer    105
    2      Laptop   1200
    3  UHD Screen    400

.. note:: The old index is reused

The most used format for loading and saving is probably csv::

    df3.to_csv('file1.csv', index=False)

Results in the following::

    Product,    Price
    Tablet,     250
    Printer,    105
    Laptop,     1200
    UHD Screen, 400

If required the header and index need not be saved::

    df3.to_csv('file2.csv', header=False, index=False)

More importantly special separators may be required::

    df3.to_csv('file3.csv', sep=";")

Results in the csv::

    ;Product;Price
    0;Tablet;250
    1;Printer;105
    2;Laptop;1200
    3;UHD Screen;400

When reloaded::

    df3 = pd.read_csv("file3.csv")
    df3
     ;Product;Price
    0;Tablet;250
    1;Printer;105
    2;Laptop;1200
    3;UHD Screen;400

The output is squashed together, so it is not a well behaving dataframe, 
import again this time stating the separator::

    df3 = pd.read_csv("file3.csv", sep=";")
    df3
       Unnamed: 0     Product  Price
    0           0      Tablet    250
    1           1     Printer    105
    2           2      Laptop   1200
    3           3  UHD Screen    400

Oops now there are 2 indexes. Remove the old index::

    del df3['Unnamed: 0']
    df
        Product  Price
    0      Tablet    250
    1     Printer    105
    2      Laptop   1200
    3  UHD Screen    400

Alternatively we could have dropped a column by position::

    df3.drop(df.columns[[0]], axis=1)

When saving to csv remember to disable the index::

    df3.to_csv("file3.csv", sep=";", index=False)

A new index is produced automatically when loading/reloading csv files.