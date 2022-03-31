# PySAC
A Python based Machine Lreaning (ML) algorithm for the Gibbs free enegy of various intermediates on single atom catalysts # (SACs)
************************************************************
Developed by Mohsen Tamtaji (mtamtaji@connect.ust.hk) under supervision of Professor Tom Luo at HKUST

The developed ML algorithm can be used for the prediction of Gibbs free energy of N2*, H*, OH*, O*, OOH*, COOH*, CO*, and CHO* intermediates for NRR, HER, ORR, and CO2RR

Support vector regression (SVR) model using scikit-learn package is trained based on 2104 DFT-calculated data which is produced by our group and also collected from literature for graphene-based and porphyrin-based SACs

The ML model is applicable for all the 3d, 4d, and 5d transition metals (TM) embedded into nitrogen-doped graphen- and porphyrin-based SACs with the structures of TM@N4, TM@N3C1, TM@N2C2, TM@N1C3, TM@C4, TM@C3, and TM@C2. It distinguishes the difference effect of pyrrolic and pyridinic nitrogen on the Gibbs free energy.

************************************************************

# Requirments:

1-rdkit (https://www.rdkit.org/docs/Install.html)

2-mendleev(https://pypi.org/project/mendeleev/)

3- matplotlib

4- numpy

************************************************************

# Run the program:

Note: there is not "pip install" of this version yet, so you need to download the ML algorithm and run the program as follows:

1- Download the PySAC2.sav and Propertyoriginal.pkl files into your directory

2- Put the .mol file of your graphen-based SAC into your directory (you need to prepare .mol file of SAC structure by using Avogadro or other softwares. You may chack the Test.mol file)

3- Download the PySAC.py and put into your directory, open in your PyCharm, Spider, or other Python environments, change the directory (Location) and filename in the PySAC.py file and run the code. The program will generate 3 figure for HER, ORR, and CO2RR and also will give you the overpotential and limiting potential of ORR. The free energy of N2*, H*, OH*, O*, OOH*, COOH*, CO*, and CHO* intermediates will be wrote into a .txt file which will be saved is in your directory.

4- Enjoy :)

************************************************************

# Citation:

For the citation, please cite the following papers:

1- DOI: 10.1039/D1TA08337F 

2- https://doi.org/10.1021/acsanm.1c01436
