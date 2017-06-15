-*- coding: utf-8 -*-

The Python modules in this directory contain a few complex expressions (in
particular those assigned to 'refTree') that serve to test the correctness of
some intermediate representations used by CondConfigParser (most notably,
abstract syntax trees). In order to make sure these expressions are themselves
correct, the following procedure should be applied whenever their content must
be changed in a non-trivial way:

  1. Write a representation of the expression in the new, desired format to a
     file using dev-tools/test.py. Let's call this file 'new_data'. test.py
     relies on the new code, which might be buggy, but we'll carefully compare
     its output with the old, validated data to make sure the changes are what
     we expect.

  2. In GNU Emacs, open 'dev-tools/auto_format_for_unittest_datafiles.el' and
     type `M-x eval-buffer'. This defines a new command named
     `flo-custom-replace-1' and binds it to Super_L-Pause (<s-pause> in
     Emacs-speak, the "s" corresponding to the Logo key on my system).

  3. Open 'new_data' in Emacs and select the region to be treated by
     `flo-custom-replace-1' (you may use `C-x h' to select the whole buffer).

  4. Run `flo-custom-replace-1' with the <s-pause> shortcut or by typing
     `M-x flo-custom-replace-1'. This causes several series of interactive
     `query-replace' or `query-replace-regexp' (5 at the time of this
     writing). You may approve the replacements one at a time with `y' or `n',
     or do all of them for a given series with `!' (type `?' for help). This
     formats the complex expression in the same way as used in the *.py files
     from this directory, which makes it relatively easy to read and compare
     to the old data.

  5. Optionally save the file with the new, formatted data.

  6. Compare it with the corresponding .py file containing the old, formatted
     data (e.g., 'refTree' before a change to the abstract syntax tree format
     that has a large, difficult to validate impact on the value). For this
     step, I suggest to open the two buffers to compare and use
     `M-x ediff-buffers' (can be found in the menu bar too:
     Tools → Compare (Ediff) → Two Buffers...).

     With this method, if for instance the old data is in the buffer labelled
     A and the new data in B, you can replace the old data with the new data
     for the highlighted part by simply typing `b' and proceed to the next
     chunk with `n' (`p' to get back to the previous one). Use `?' for help
     and `q' to quit Ediff when you are finished with the changes (all these
     shortcuts must be typed when the small Ediff window has focus).

Be very careful with the changes to this complex data. It is a valuable
automated test tool, but only as long as the data is correct! If the new code
is buggy, test.py may produce a "wrong" data representation. This wrong data
must not be put blindly into a .py file as the new reference data for
automated tests!

All the data currently contained in the .py files has been carefully checked
for correctness. Should a change in its format be necessary, the Ediff-based
method explained here should make it reasonably easy to validate the changes
without having to check the whole expression from ground up.
