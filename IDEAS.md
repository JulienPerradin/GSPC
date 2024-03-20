# ideas:

flowchart to analyze a trajectory file:

1) cd /path/to/trajectory/file
2) create a launch-GSPC.py file
3) import gspc module and program the diverse general settings
   1) path to export directory
   2) general settings about the structural properties to compute
   3) further settings etc.
4) code in the launch-GSPC.py the function gspc.launch()
5) the gspc module read the trajectory 
6) it executes its internal function to process the analysis
7) the gspc module write the results in different files depending on the settings
8) done.
