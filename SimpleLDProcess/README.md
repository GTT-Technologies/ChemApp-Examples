# Simple LD converter model

This example was used in a webinar, which was recored. The files are slightly
polished and instructive comments are added.

https://www.youtube.com/watch?v=ftF98LmqPYo

The purpose of this example is to model a very basic concept of an LD converter.
It is assumed that a hot iron rich metal liquid phase has oxygen blown into it.
Controlling the amount of added oxygen is crucial to the process control in a
real LD process, which is used to reduce the carbon content of the liquid phase.

A series of calculations is done for variable amounts of added gaseous oxygen,
to calculate the enthalpy difference (which is a measure for the exothermic
intensity of the process), and how the amount of carbon in the liquid phase
changes with added oxygen.

Finally, a brief analysis step is added to determine the critical amount of
oxygen to add so that less than 0.1wt% of carbon remains in the liquid for a set
of varied compositions, to simulate the varying compositions typically used in
steel metallurgy process modelling.

Please be aware that all numbers and values are purely of educational value and
do not reflect any actual process. For simplification purposes, to keep the
webinar concise, quite a few necessary metallurgical or thermophysical
considerations have been left purposefully undiscussed, to focus on the
functionality of ChemApp within the Python ecosystem.


## Requirements
### Python packages:
* chemapp>826
* pandas
* numpy
* Jupyter/IPython/...

### Databases
* FTmisc
* FactPS
* FToxid

Note that these databases may be replaceable with databases available to you,
however, some of the phase names likely need to be adapted, and the results will
not be numerically identical.


## First step
The first calculation is a simple demonstration of the `Equi2Py` tool that is
used to convert an Equilib save file (here: `LDprocess_start.equi`) into a
Python Jupyter Notebook (`HotMetalLiquid.ipynb`)

If you want to run the Notebook, make sure to create a cst file first, using
Equilib. Take note to correctly adjust the database file that is loaded in the
notebook if you choose a different file name.

You should be able to generate the same or a very similar file simply by using
the export function in Equilib.

## Second step
A tabulated set of varying compositions is read and iterated over:
`hotmetal.csv`. A Jupyter notebook can be found in
`MultipleHotMetalLiquids.ipynb`, that is an iteration on the first step
notebook, but with the added code to read the csv table into a `pd.DataFrame`
and subsequently iterate over this, so that results for all row entries of that
table are calculated.

## Third step
Putting together the full workflow - First, calculate and equilibrate the hot
metal liquid, then isolate this liquid phase and use it as a 'constant' input
into a series of calculations in which the amount of added oxygen is varied.
The combined script can be found in `LDprocess.ipynb`.

At the end of the process model, the questions from the start are answered -
using a naive search logic. This is not an efficient way to solve the problem,
but mostly an instructive way how to approach such a model.


## Final remarks
The file `final_results.csv` contains the same table data as the input csv file
`hotmetal.csv`, and two additional columns `minO2` and `dH`, which are answering
the questions we set out to answer.

