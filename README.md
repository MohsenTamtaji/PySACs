# PySACs

A Python-based Machine Learning (ML) algorithm for the Gibbs free enegy (ΔG) of various intermediates on single atom catalysts (**SACs**)
************************************************************
Developed by Mohsen Tamtaji (mtamtaji@connect.ust.hk) under the supervision of Professor Zhengtang Tom Luo at HKUST, [Advanced Materials & Devices Laboratory](https://tomluogroup.wixsite.com/nanomaterials)


The developed ML algorithm can be used for the prediction of Gibbs free energy (ΔG (eV)) of *N2, *H, *OH, *O, *OOH, *COOH, *CO, and *CHO intermediates for NRR, HER, ORR, and CO2RR

Support vector regression model (SVR) using scikit-learn package is trained based on 2104 DFT-calculated data which is produced by our group and also collected data from the literature for graphene-based and porphyrin-based SACs

The ML model is applicable for all the 3d, 4d, and 5d transition metals (TM) embedded into nitrogen-doped graphen- and porphyrin-based SACs with the structures of TM@N4, TM@N3C1, TM@N2C2, TM@N1C3, TM@C4, TM@C3, TM@N1C1, TM@N2, and TM@C2. It distinguishes the difference effect of pyrrolic and pyridinic nitrogen on the Gibbs free energy.

************************************************************

![SAC](https://github.com/MohsenTamtaji/PySACs/blob/09c3272990b3c9772fadb94f36cd25eefc11d0b5/Figure8%20-%20Copy%20(2).png)

************************************************************

# Requirments and Dependencies:

PySACs needs the following pakages:

1-[rdkit](https://www.rdkit.org/docs/Install.html)

2-[mendleev](https://pypi.org/project/mendeleev/)

3- [matplotlib](https://matplotlib.org/stable/users/installing/index.html)

4- [numpy](https://numpy.org/install/)

************************************************************

# Running PySACs:

Note: There is not "pip install" of this version yet, so you need to download the ML algorithm and run the program as follows:

1- Download the PySACs.sav and Propertyoriginal.pkl files into your directory

2- Put the .mol file of your graphen-based SAC into your directory (you need to prepare .mol file of SAC structure by using Avogadro or other softwares. You may check the Test.mol file)

3- Download the PySACs.py and put into your directory, open in your PyCharm, Spider, or other Python environments, change the directory (Location) and filename in the PySACs.py file and run the code. The program will generate 3 figures for HER, ORR, and CO2RR and also will give you the overpotential and limiting potential of ORR. The free energy of *N2, *H, *OH, *O, *OOH, *COOH, *CO, and *CHO intermediates will be wrote into Results.txt file which will be saved in your directory.

4- Enjoy :)

************************************************************

# Contributing training data:
We are very interested to recieve community contributions to the training data and re-train the PySACs model to make it more accurate and more general for graphene- and porphyrin-based and also other SAC systems. Please contact us though mtamtaji@connect.ust.hk, so that we may incorporate your data into PySACs. Thanks for your contribution. 

************************************************************

# Citation:

For the citation, please cite the following papers:

1- DOI: [10.1039/D1TA08337F](https://pubs.rsc.org/en/content/articlehtml/2022/ta/d1ta08337f)

2- https://doi.org/10.1021/acsanm.1c01436
