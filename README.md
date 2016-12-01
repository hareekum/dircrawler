# dircrawler
dircrawl leverages python's os.walk and supports a set of operations during traversal

Operations supported so far -
- diff - Compares the current state of directory with given state represented as set of (filepath, modified_ts) and returns state of each file. State can be added, modified or removed.
- transform - Transforms the contents of a filepath per given method returns transformed output

