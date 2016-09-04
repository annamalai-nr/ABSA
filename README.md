Apsect Based Sentiment Analysis (ABSA) python implementations
- SemEval 2014 solutions: NRC Canada, JUSCE 
- SemEval 2015 solutions: TBD
- Deep Learning solutions for ABSA: CNN based impl by Wang & Liu (Stanford), LSTM based impl by Tang et. al.

For stanford corenlp python wrapper, https://github.com/dasmith/stanford-corenlp-python is used
- Need to run 'python corenlp.py' first. This starts a RPC service that is invoked by other python wrapped APIs. 
- Since this RPC invoations, CANNOT RUN PARALLEL requests!
- Need to make sure 'jsonrpc.py' is in the same folder as 'corenlp.py'
- import jsonrpc, that's it!

reference for CRF:
- http://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html
- http://stats.stackexchange.com/questions/38216/implementation-of-crf-in-python
