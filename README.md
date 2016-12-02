# dircrawler
dircrawl leverages python's os.walk and supports a set of operations during traversal

## Snapshots
If a snapshot file and snapshot handler is specified, dircrawler will compare current directory tree
with snapshot information and return state of a file.

State can be one of
- ADDED (file present and not listed in snapshot)
- REMOVED (file not present and listed in snapshot)
- MODIFIED (file present and listed in snapshot, current mod timestamp < mod timestamp in snapshot)
- UNCHANGED (file present and listed in snapshot, same mod timestamps
- UNKNOWN (file present and listed in snapshot, current mod timestamp < mod timestamp in snapshot)

Snapshot handlers are classes extending AbstractSnapshotHandler and implementing their own parse()
method. The expected result of parse() is a tuple of filepath and SnapshotState object
Currently, dircrawler only supports snapshot handlers accepting a filepath as an argument to
the parse() method

Here are the snapshot handlers which come along with dircrawler:
*WhiteSpaceSeparatedSnapshotHandler* - Parses file states from a file having values split by whitespaces


## Transformers
If a transformer is specified, dircrawler will return transformed output from the transformer
implementation.

Transformers are classes extending AbstractTransformer and implementing their own transform() method.
The expected result of transform() is a string representing the transformation.
Currently, dircrawler only supports transformers accepting a filepath as an argument to
the transform() method

Here are the transformers which come along with dircrawler:
*MD5Transformer* - Computes MD5 hash of a file
*FirstLineTransformer* - Gets the first line of a file

Both snapshot handlers and transformers are meant to be pluggable, meaning you plug in your own classes
as long as they implement the required method. One way to ensure compatibility is to have your classes
extend and implement the appropriate abstract class

## Trying it out
- First, create a virtualenv and activate it
- Checkout the project and pip install it in your virtual env

    ```bash
    dircrawler> pip install .
    ```
- Run the crawler

    ```bash
    crawl -d /some/dir -p -sf /some/snapshot.txt -sh dircrawler.snapshot_handlers.WhiteSpaceSeparatedSnapshotHandler -t dircrawler.transformers.FirstLineTransformer
    ```
