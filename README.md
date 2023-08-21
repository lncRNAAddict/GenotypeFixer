# GenotypeFixer

Here, we present a Python tool called `GenotypeFixer` which offers an easy-to-use command line interface that corrects genotype calls and imputes missing data to improve the accuracy of genetic mapping. Popular tools require to input parameters such as homozygous and heterozygous error rate etc. GenotypeFixer doesn't need any of these parameters.



## Installation and Dependencies

GenotypeFixer has been tested with Python 3.8.12 version. It should work with Python >= 3.0 version. We recommend installing the anaconda python distribution. Download the anaconda python distribution from https://www.anaconda.com/products/distribution and install it following the instructions provided.

PySmooth depends on the following Python libraries. These libraries are already included in the Anaconda distribution. Therefore, you do not need to install them.

- `numpy`
- `Pandas`
- `Sklearn`
- `matplotlib`
- `PyThresh`:  thresholding outlier detection likelihood scores
- `PyOD`: for outlier/anomaly detection


The libraries `Numpy`, `Pandas`, `Sklearn`, and `Matplotlob` are already included in the anaconda distribution. Therefore, you do not need to install them. Installation instructions for 

- `PyOD`: https://pyod.readthedocs.io/en/latest/
- `PyThresh`: https://github.com/KulikDM/pythresh

## Installation


You can simply download the following scripts from the `src` folder in the `GenotypeFixer` GitHub page and put them in a single folder. 

- `ImputeMissingGenotype.py`
- `run_GenotypeFix.py`


## Usage

`GenotypeFix` is executed using the Python script `run_GenotypeFixer.py` in the Python command line.

`run_GenotypeFix.py` takes the following arguments

- `-g` or `--genotype`: Name of the input genotype file. This MUST be provided.
- '-o' or `--output`: Prefix to name of output files to be generated. If not provided, the default is `test`.
- `-a` or `--anomaly`: Name of anomaly detection algorithm to be used (`iforest`, `knn`, `pca` or `ecod` . The default is `iforest`.
- `-t` or `--thresh`: Name of thresholding algorithm to be used (`meta`, `filter`, or `clf` . The default is `meta`.
- `-c` or `--chrs`: list of chromosomes to be processed (should be separated by a comma). The default is `all`.


To execute `run_GenotypeFix.py`, change the working directory to the folder where the `GenotypeFix` scripts are stored. You can do that by simply typing the following command in the `terminal`, or `command prompt`, or  `anaconda command prompt` depending on your Python installation or OS.

`cd <path to where GenotypeFix scripts are stored>`

Once the working directory is set, shown below is an example of executing `run_GenotypeFix.py`.

`python run_GenotypeFix.py -g <path to the genotype file>/my_genotype_file.csv  -o my_output -a iforest -t meta -c all`

The code above will process all the chromosomes and fix the errors and missing data in the genotype file and generate all output files with the prefix `my_output`. 
  
### Input genotype file format

The First row is the header. Each row represents a unique marker.

The genotype file MUST have the following columns:

- Column 1: Chromosome name.
- Column 2: Genomic Position of the marker in the chromosome. For each chromosome,column 2 MUST already be sorted in ascending order.
- Column 3 and after: Genotype code for the individuals in the marker location. Four codes can be used. `A`: Reference parent homozygous, `B`: Alternatte parent homozygous, `X`: heterozygous, `-`: missing data.

A screeshot of a portion of an example input file is shown below

![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/genotype_file.JPG)


### Outputs

For each chromosome, PySmooth Generates the following outputs.

- Three summary csv files: `<output>_<chr>.stats.csv`, `<output>_<chr>_singletons_stats.csv`, and `<output>_<chr>_imputed_stats.csv` that contain `%` of homozygous, heterozygous calls for each individual for the raw genoytpe file, after singleton detection, and after error correction. Examples are shown below.


A screeshot of a portion of an example input file is shown below

![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/corrected.jpg)
