textSNE
=======

Python code for rendering t-SNE code with text labels for each point.

See test-output.expected.png for an example of the sort of visualization
this code will perform.

t-SNE is:
    van der Maaten, L. J. P. and Hinton, G. E. (2008)
    Visualizing Data using t-SNE.
    Journal of Machine Learning Research, Vol 9, (Nov) pp 2579-2605.

Where noted in header code or by directory name, I have included 3rd-party code.

My main change from the original t-SNE implementation is that I
disable PCA as a preprocessing step, unless specifically explicitly by
a function parameter. Since my data is high-dimensional and sparse,
PCA is painfully slow.

To get started:

1) Unpack the original tSNE package:
    cd 3rd-party/t-SNE_files/
    tar zxvf tSNE_linux.tar.gz 
If you are on a different architecture, you will have to unzip another package.

Alternately, you can use the pure Python implementation of t-SNE by
replacing all code that reads:
    from calc_tsne import tsne
with the following code:
    from tsne import tsne
You will need matplotlib to run the pure Python implementation. However, 

2) (Optional) Edit render.py and change DEFAULT_FONT to a TTF file
containing a font you like.

3) Run ./test.py to test your installation.
This will generate file 'test-output.rendered.png'.
Note that 'test-output.rendered.png' and 'test-output.expected.png'
are different, because each invockation of tSNE_linux uses a different
random initialization.

=======

REQUIREMENTS:
    imagemagick:
        We use convert at the end of render.render, to flatten an image.
        Type:
            which convert
        as a test to see if you have this executable.
        You could perhaps remove this image flattening step, if you like.
