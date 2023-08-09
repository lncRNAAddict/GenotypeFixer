# GenotypeFixer

Here, we present a python implementation of SMOOTH (van Os,H. et al. (2005) ) called `PySmooth` which offers an easy-to-use command line interface and solves the drawbacks of SMOOTH. PySmooth reads the input genotype file and identifies singletons based on the algorithm described in SMOOTH with some modifications to allow four genotype codes, and flexible parameters. Unlike SMOOTH which doesn’t correct the singletons and missing data, PySmooth corrects genotype errors using a k-nearest algorithm. At each step, PySmooth generates summary files and visualizations that can be inspected by the user for further interpretation.


## Installation and Dependencies

PySmooth has been tested with Python 3.8.12 version. It should work with Python >= 3.0 version. We recommend installing the anaconda python distributon. Download anaconda python distribution from https://www.anaconda.com/products/distribution and install following the instructions provided.

PySmooth depends on the following python libraries. These libraries are already included in the anaconda distribution. Therefore, you do not need to install them.

- `numpy`
- `Pandas`
- `Sklearn`
- `matplotlib`
