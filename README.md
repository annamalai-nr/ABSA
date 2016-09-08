Apsect Based Sentiment Analysis (ABSA) python implementations
- SemEval 2014 solutions: 
	- NRC Canada: http://www.aclweb.org/anthology/S14-2076
	- JUSCE 
- SemEval 2015 solutions: TBD
- Deep Learning solutions for ABSA: 
	- CNN based impl by Wang & Liu (Stanford): https://cs224d.stanford.edu/reports/WangBo.pdf
	- LSTM based impl by Tang et. al.: https://arxiv.org/pdf/1605.08900.pdf

For stanford corenlp python wrapper, https://github.com/dasmith/stanford-corenlp-python is used
- Need to run 'python corenlp.py' first. This starts a RPC service that is invoked by other python wrapped APIs. 
- Since this RPC invoations, CANNOT RUN PARALLEL requests!
- Need to make sure 'jsonrpc.py' is in the same folder as 'corenlp.py'
- import jsonrpc, that's it!

reference for CRF:
- http://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html
- http://stats.stackexchange.com/questions/38216/implementation-of-crf-in-python

reference for NLKT parse tree to NX graph:
- http://stackoverflow.com/questions/25815002/nltk-tree-data-structure-finding-a-node-its-parent-or-children
- http://stackoverflow.com/questions/29397460/extract-parent-and-child-node-from-python-tree
- http://www.nltk.org/api/nltk.html#nltk.tree.ParentedTree

Aspect Location (May be TBD):
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval059.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval075.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval076.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval092.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval099.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval101.pdf

- clustering paper: http://www.aclweb.org/anthology/N/N16/N16-1093.pdf

