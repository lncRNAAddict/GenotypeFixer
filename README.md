# GenotypeFix

Here, we present a python tool called `GenotypeFixer` which offers an easy-to-use command line interface that corrects genotype calls and imputes missing data to improve the accuracy of genetic mapping. 



## Installation and Dependencies

GenotypeFixer has been tested with Python 3.8.12 version. It should work with Python >= 3.0 version. We recommend installing the anaconda python distributon. Download anaconda python distribution from https://www.anaconda.com/products/distribution and install following the instructions provided.

PySmooth depends on the following python libraries. These libraries are already included in the anaconda distribution. Therefore, you do not need to install them.

- `numpy`
- `Pandas`
- `Sklearn`
- `matplotlib`

## Installation


You can simply download the following scripts from `src` folder in `GenotypeFixer` GitHub page and put them in a single folder. 

- `utilities_parallel.py`
- `motif_viz.py`
- `run_ChromNetMotif.py`


## Usage

`GenotypeFix` is executed using the python script `run_GenotypeFixer.py` in the python command line.

`run_GenotypeFix.py` takes the following arguments

- `-g` or `--genotype`: Name of the input genotype file. This MUST be provided.
- '-o' or `--output`: Prefix to name of output files to be generated. If not provided, default is `test`.
- `-a` or `--anomaly`: Name of anomaly detection algorithm to be used (`iforest`, `knn`, `pca` or `ecod` . Default is `iforest`.
- `-t` or `--thresh`: Name of thresholding algorithm to be used (`meta`, `filter`, or `clf` . Default is `meta`.
- `-c` or `--chrs`: list of chromosomes to be processed (should be separated by a comma). Default is `all`.


To execute `run_GenotypeFix.py`, change working directory to the folder where the `GenotypeFix` scripts are stored. You can do that by simply typing the following command in the `terminal`, or `command prompt`, or  `anaconda command prompt` depending on your python installation or OS.

`cd <path to where GenotypeFix scripts are stored>`

Once the working directory is set, shown below is an example of executing `run_GenotypeFix.py`.

`python run_GenotypeFix.py -g <path to the genotype file>/my_genotype_file.csv  -o my_output -a iforest -t meta -c all`

The code above will process all the chromosomes and fix the errors and missing data in the genotype file  and generate all output files with the prefix `my_output`. 
  
### Input genotype file format
