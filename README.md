# GenotypeFixer

Here, we present a python tool called `GenotypeFixer` which offers an easy-to-use command line interface that corrects genotype calls and imputes missing data to improve the accuracy of genetic mapping. 



## Installation and Dependencies

GenotypeFixer has been tested with Python 3.8.12 version. It should work with Python >= 3.0 version. We recommend installing the anaconda python distributon. Download anaconda python distribution from https://www.anaconda.com/products/distribution and install following the instructions provided.

PySmooth depends on the following python libraries. These libraries are already included in the anaconda distribution. Therefore, you do not need to install them.

- `numpy`
- `Pandas`
- `Sklearn`
- `matplotlib`

## Installation


You can simply download the following scripts from `src` folder in `ChromNetMotif` GitHub page and put them in a single folder. 

- `utilities_parallel.py`
- `motif_viz.py`
- `run_ChromNetMotif.py`


## Usage

`ChromNetMotif` is executed using the python script `run_ChromNetMotif.py` in the python command line.

`run_ChromNetkMotif.py` takes the following arguments

- `-g` or `--network`: Name of the input chromatin state network file. This MUST be provided.
- '-o' or `--output`: Prefix to name of output files to be generated. If not provided, default is `test`.
- `-n` : number of random networks to be generated for motif enrichment testing, `p-value`, and `z-score`. Default is 500.
- `-m` : number of nodes in the motif or motif size to be extracted. Default is 3. It can only handle motif of size 3 and 4. 
- `-p` : number of processors to be used. Default is 1.
- `-t` : p-value threshold to detect statistically enriched motifs. Default value is 0.05.
- `-f` : minimum frequency in the real network for a chromatin-state marked motif to be counted as statistically enriched. Default value is 1. There might be some chromatin-state marked motifs which occur at very few instances in the network. The user has the choice to disregard such motifs using this threshold.
- `-r`, or `--randomization`: method to generated randomized networks. options are `I` or `II`. `I`: swapping of edges while degree preserving in the network. `II`: only the chromatin states of the nodes are randomized. Default is `I`.

To execute `run_ChromNetkMotif.py`, change working directory to the folder where the `ChromNetworkMotif` scripts are stored. You can do that by simply typing the following command in the `terminal`, or `command prompt`, or  `anaconda command prompt` depending on your python installation or OS.

`cd <path to where ChromNetworkMotif scripts are stored>`

Once the working directory is set, shown below is an example of executing `run_ChromNetMotif.py`.

`python run_ChromNetMotif.py -g <path to the network file>/my_network_file.csv  -o my_output -n 500 -m 3 -p 4 -t 0.05`

The code above will extract chromatin-state marked motifs of size 4 and generate all output files with prefix `my_output`. Computation will be done using 4 processors in parallel. P-value of 0.05 and minimum frequency of 50 will be used to identify significant motifs selected for visualization.
  
### Input Chromatin state network file format
