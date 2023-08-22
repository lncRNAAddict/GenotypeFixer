# GenotypeFixer


Here, we present a Python tool called `GenotypeFixer` which offers an easy-to-use command line interface that corrects genotype calls and imputes missing data to improve the accuracy of genetic mapping. Popular tools require to input parameters such as type of population (F2, RIL etc), homozygous and heterozygous error rate, and sliding window size. GenotypeFixer doesn't need any of these parameters. GenotypeFixer uses a three-step process to achieve this. First, the missing genotype labels are imputed by using K-nearest neighbor approach. Secondly, anomalies in the genotype calls are detected. Thirdly, the anomalies are corrected using K-nearest neighbor approach. The main advantage of GenotypeFixer is that it eliminates the need for the user to provide parameters which other tools do. The optimal parameters for the K-nearest neighbor approach and thresholding in anomaly detection algorithms are internally computed by GenotypeFixer. This eliminates the need for the user to perform guesswork. The only input the user need to provide is the input genotype file.




## Installation and Dependencies

GenotypeFixer has been tested with Python 3.8.12 version. It should work with Python >= 3.0 version. We recommend installing the anaconda python distribution. Download the anaconda python distribution from https://www.anaconda.com/products/distribution and install it following the instructions provided.

PySmooth depends on the following Python libraries. These libraries are already included in the Anaconda distribution. Therefore, you do not need to install them.

- `numpy`
- `Pandas`
- `Sklearn`
- `matplotlib`
- `PyThresh`:  Python package for thresholding outlier detection likelihood scores
- `PyOD`: Python package for outlier/anomaly detection


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
GenotypeFixer Generates the following outputs.

- Corrected genotype File: `<output>.corrected.csv` This is the corrected genotype file. A screeshot of a portion of an example corrected file is shown below


![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/corrected.jpg)

- Summary stats file: `<output>.corrected.stats.csv` This file contains statistics on the correction performed by GenotypeFixer. A screeshot of a portion of an example corrected file is shown below. For each sample, the number of corrections for seven different categories are provided.
![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/corrected_stats.jpg)

- Summary stats files: `<genotype_file>.summary.stats.csv` and `<output>.summary.stats.csv` that contain `%` of homozygous, heterozygous, missing calls for each individual for the raw genoytpe filer and after error correction, respectively. Examples are shown below.

Count and percentage of each type of genotype call in the original file

  ![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/original_homo.jpg)


Count and percentage of each type of genotype call in the corrected file


![Example Input Genotype File](https://github.com/lncRNAAddict/GenotypeFixer/blob/main/Figures/corrected_homo.jpg)

### Example Data

In the `Data` folder, there are two example genotype files : `fixed_columns_set_RIL_20_0M_10_0F.csv` and `fixed_columns_set_F2_20_0M_10_0F.csv`

To execute `GenotypeFixer` on the file `fixed_columns_set_RIL_20_0M_10_0F.csv`, simply use the following command

`python run_GenotypeFix.py -g Data/fixed_columns_set_RIL_20_0M_10_0F.csv -o Data/my_output`

It will generate the folllowing files:

- `Data/my_output.corrected.csv`
- `Data/my_output.corrected.stats.csv`
- `Data/fixed_columns_set_RIL_20_0M_10_0F.csv.summary.stats.csv`
- `Data/my_output.summary.stats.csv`


