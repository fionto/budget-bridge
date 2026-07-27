# In Python, file objects are iterators. This means I can iterate 
# through them line by line without first having to convert them 
# into a list.

with open('data/fake_wallet_record.csv', 'r', encoding='utf-8') as csv_source:
    
    # Read and discard only the first line (the header)
    # This is the built-in function specifically for "advancing one step" 
    # in an iterator. It's semantically clearer to say 
    # "grab the next element and ignore it" 
    # than to say "readline()" (even though they technically do the same thing in this context).
    next(csv_source)

    for row in csv_source:
        print(row, end="")