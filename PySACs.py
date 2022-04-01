from rdkit.Chem import Draw
from rdkit import Chem
from rdkit.Chem import rdqueries
import numpy as np
import pickle
import matplotlib.pyplot as plt
from mendeleev import element
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

print('************************************************************')
print('Developed by Mohsen Tamtaji (mtamtaji@connect.ust.hk) Under supervision of Professor Tom Luo at HKUST')
print('ML algorithm for the prediction of Gibbss free energy for HER, ORR, and CO2RR')
print('SVR model is trained based on 2104 data in the literature for graphene-based single atom catalysts')
print('************************************************************')

Location=r"E:\MLSAC\MlModel" #Define the location of your files (PySAC2.sav and Propertyoriginal.pkl)
Intermediates=[ 'H','N2-side','N2-end','OH','O','OOH','CO','CO2','COOH','CHO']
IntProperties=[[ 1,  2,        2,       1,   1,   1,   1,   1,    1,     1   ],#Numbers of atoms connected to SAC,      first ring
               [ 1,  14,       7,       8,   8,   8,   7,   7,    7,     7   ],#Atomic_nmber of atoms connected to SAC, first ring
               [ 1,  5,        5,       6,   6,   6,   4,   4,    4,     4   ],#Valance_electron of atoms connected to SAC, first ring
               [ 0,  0,        1,       1,   0,   1,   1,   2,    2,     2   ],#Numbers of atoms in the second ring
               [ 0,  0,        7,       1,   0,   8,   8,   16,   16,    9   ],#Atomic_number of atoms in the second ring
               [ 0,  0,        0,       0,   0,   1,   0,   0,    1,     0   ],#Numbers of atoms in the third ring
               [ 0,  0,        0,       0,   0,   1,   0,   0,    1,     0   ]]#Atomic_number of atoms in the third ring

MLModel = '\PySACs.sav' #The name of ML model
filename='\Test.mol' # Put the mol file of your SAC structure into your directory
loaded_model = pickle.load(open(Location+MLModel, 'rb'))# load the ML model
mol = Chem.MolFromMolFile(Location+filename)
Draw.MolToFile(mol,Location+'\Test.png') #Save the structure of your SAC

for atom in mol.GetAtoms():
     if atom.GetAtomicNum()>20:
         elementAN=element(atom.GetAtomicNum())
         TMsymbol=elementAN.symbol# the symbol of Transition Metal
         NeighborsAN=[x.GetAtomicNum() for x in atom.GetNeighbors()]
         NeighborsIndex=[x.GetIdx() for x in atom.GetNeighbors()]
NC,NN,Npr,Npy=0,0,0,0
for x in NeighborsAN:
    if x==6: NC+=1    #C
    elif x==7: NN+=1  #N
for x in NeighborsIndex:
    if str(mol.GetAtomWithIdx(x).GetSymbol())=='N':
        if str(mol.GetAtomWithIdx(x).IsInRingSize(5))=='True':
            Npr+=1
        if str(mol.GetAtomWithIdx(x).IsInRingSize(4))=='True':
            Npy += 1

q = rdqueries.AtomNumEqualsQueryAtom(6)#C
CTM=len(mol.GetAtomsMatchingQuery(q))
q = rdqueries.AtomNumEqualsQueryAtom(7)#N
NTM=len(mol.GetAtomsMatchingQuery(q))
Propertyoriginal = pickle.load(open(Location+'\Propertyoriginal.pkl', 'rb'))
Property=np.zeros((len(Intermediates),np.size(Propertyoriginal[0,:])))
i=0
for Species in Intermediates:
    elementname = element(TMsymbol)
    # print(elementname)
    m = str(elementname.ec)
    # print(m)
    if elementname.atomic_number < 32:
        d = '3d'
    elif elementname.atomic_number < 51:
        d = '4d'
    else:
        d = '5d'
    Property[i][0] = elementname.atomic_number
    Property[i][1] = float(m[m.index(d) + 2:m.index(d) + 4])
    Property[i][2] = elementname.atomic_radius
    Property[i][3] = elementname.en_pauling
    Property[i][4] = elementname.evaporation_heat
    if  m== 'Ru': Property[0][4] = 595
    Property[i][5] = elementname.ionenergies[1]
    Property[i][6] = elementname.electron_affinity
    if  m== 'Mn' or  m== 'Zn':
        Property[i][6] = 0
    elif  m== 'Cd':
        Property[i][6] = -0.7
    elif  m== 'Hg':
        Property[i][6] = -0.5
    Property[i][7] = NTM
    Property[i][8] =  CTM
    Property[i][9] =  CTM/(CTM+NTM)*100
    Property[i][10] = NN   #
    Property[i][11] = NC   #
    Property[i][12] = Npy   #
    Property[i][13] = Npr   #
    Property[i][14] = (elementname.nvalence()%2)/2*2+1  # Spin multiplicity of SACs
    Property[i][15] = IntProperties[0][Intermediates.index(Species)]
    Property[i][16] = IntProperties[1][Intermediates.index(Species)]
    Property[i][17] = IntProperties[2][Intermediates.index(Species)]
    Property[i][18] = IntProperties[3][Intermediates.index(Species)]
    Property[i][19] = IntProperties[4][Intermediates.index(Species)]
    Property[i][20] = IntProperties[5][Intermediates.index(Species)]
    Property[i][21] = IntProperties[6][Intermediates.index(Species)]
    i+=1
#Normalizing the input data between 0 and 1
for i in range(np.size(Propertyoriginal[0,:])):
    Property[:,i]=(Property[:,i]-np.min(Propertyoriginal[:,i]))/(np.max(Propertyoriginal[:,i])-np.min(Propertyoriginal[:,i]))
Response=loaded_model.predict(Property)

with open(Location + "\Results.txt", 'w+') as f:
    i=0
    for Species in Intermediates:
        f.write(Species+','+str(Response[i]))
        f.write("\n")
        i+=1
#ORR limiting potential
ULP=np.min([Response[3]-0,Response[4]-Response[3],Response[5]-Response[4],4.92-Response[5]])
UOP=4.92/4
print('Limiting potential for ORR is = ',np.round(ULP,2),' V')
print('Overpotential for ORR is = ',UOP,' V')
print('Find the free enegies in your directory')
print('Enjoy ...')

#Plot figure for HER
plt.figure()
plt.rcParams["font.family"] = "Arial"
plt.rcParams['axes.linewidth'] = 2
plt.rc('legend', fontsize=16)
plt.plot([0,1],[0,0],'b',[2,3],[Response[0],Response[0]],'b',[4,5],[0,0],'b',linewidth=2)
plt.plot([1,2],[0,Response[0]],'b--',[3,4],[Response[0],0],'b--',linewidth=2)
plt.xticks(fontsize=16,fontweight='bold',color='black')
plt.xticks([])
plt.yticks(fontsize=16,fontweight='bold',color='black')
plt.ylabel('Free energy (eV)', fontsize=20,fontweight='bold',color='black')
plt.xlabel('Reaction pathway', fontsize=20,fontweight='bold',color='black')
plt.tick_params(axis="x", direction="in", length=6, width=2, color="black")
plt.tick_params(axis="y", direction="in", length=6, width=2, color="black")
plt.text(2.3,Response[0],'H$_{ads}$*',fontsize=14,fontweight='bold',color='black')
plt.text(4.1,0,'1/2H2',fontsize=14,fontweight='bold',color='black')
plt.legend(['U=0 V'],loc='upper left',frameon=True)
plt.savefig(Location+"\HER.png",dpi=500)
plt.show
#[str(TMsymbol)+'N'+str(NN)+'C'+str(NC)]

#Plot figure for ORR
plt.figure()
plt.plot([9,8],[0,0],'k',[7,6],[Response[3],Response[3]],'k',[5,4],[Response[4],Response[4]],'k',[3,2],[Response[5],Response[5]],'k',[1,0],[4.92,4.92],'k',linewidth=2)
plt.plot([8,7],[0,Response[3]],'k--',[6,5],[Response[3],Response[4]],'k--',[4,3],[Response[4],Response[5]],'k--',[2,1],[Response[5],4.92],'k--',linewidth=1.5)
plt.plot([9,8],[0,0],'r',[7,6],[Response[3]-ULP*1,Response[3]-ULP*1],'r',[5,4],[Response[4]-ULP*2,Response[4]-ULP*2],'r',[3,2],[Response[5]-ULP*3,Response[5]-ULP*3],'r',[1,0],[4.92-ULP*4,4.92-ULP*4],'r',linewidth=2)
plt.plot([8,7],[0,Response[3]-ULP*1],'r--',[6,5],[Response[3]-ULP*1,Response[4]-ULP*2],'r--',[4,3],[Response[4]-ULP*2,Response[5]-ULP*3],'r--',[2,1],[Response[5]-ULP*3,4.92-ULP*4],'r--',linewidth=1.5)
plt.plot([9,8],[0,0],'r',[7,6],[Response[3]-UOP*1,Response[3]-UOP*1],'b',[5,4],[Response[4]-UOP*2,Response[4]-UOP*2],'b',[3,2],[Response[5]-UOP*3,Response[5]-UOP*3],'b',[1,0],[4.92-UOP*4,4.92-UOP*4],'b',linewidth=2)
plt.plot([8,7],[0,Response[3]-UOP*1],'b--',[6,5],[Response[3]-UOP*1,Response[4]-UOP*2],'b--',[4,3],[Response[4]-UOP*2,Response[5]-UOP*3],'b--',[2,1],[Response[5]-UOP*3,4.92-UOP*4],'b--',linewidth=1.5)
plt.xticks(fontsize=16,fontweight='bold',color='black')
plt.xticks([])
plt.yticks(fontsize=16,fontweight='bold',color='black')
plt.ylabel('Free energy (eV)', fontsize=20,fontweight='bold',color='black')
plt.xlabel('Reaction pathway', fontsize=20,fontweight='bold',color='black')
plt.tick_params(axis="x", direction="in", length=6, width=2, color="black")
plt.tick_params(axis="y", direction="in", length=6, width=2, color="black")
plt.text(8,0.1,'H2O(l)',fontsize=14,fontweight='bold',color='black')
plt.text(6,Response[3]+0.1,'OH*',fontsize=14,fontweight='bold',color='black')
plt.text(4,Response[4]+0.1,'O*',fontsize=14,fontweight='bold',color='black')
plt.text(2,Response[5]+0.1,'OOH*',fontsize=14,fontweight='bold',color='black')
plt.text(0,4.95,'O2',fontsize=14,fontweight='bold',color='black')
plt.legend(['U=0      V','U='+str(np.round(ULP,2))+' V','U='+str(np.round(UOP,2))+' V'],loc='upper right',frameon=True)
plt.savefig(Location+"\ORR.png",dpi=500)
plt.show

#Plot figure for CO2RR
plt.figure()
plt.plot([0,1],[0,0],'b',[2,3],[Response[8],Response[8]],'b',[4,5],[Response[6],Response[6]],'b',[6,7],[Response[9],Response[9]],'b',linewidth=2)
plt.plot([1,2],[0,Response[8]],'b--',[3,4],[Response[8],Response[6]],'b--',[5,6],[Response[6],Response[9]],'b--',linewidth=1.5)

plt.xticks(fontsize=16,fontweight='bold',color='black')
plt.xticks([])
plt.yticks(fontsize=16,fontweight='bold',color='black')
plt.ylabel('Free energy (eV)', fontsize=20,fontweight='bold',color='black')
plt.xlabel('Reaction pathway', fontsize=20,fontweight='bold',color='black')
plt.tick_params(axis="x", direction="in", length=6, width=2, color="black")
plt.tick_params(axis="y", direction="in", length=6, width=2, color="black")
plt.text(0,0,'*+CO2',fontsize=14,fontweight='bold',color='black')
plt.text(2,Response[8],'*COOH',fontsize=14,fontweight='bold',color='black')
plt.text(4,Response[6],'*CO',fontsize=14,fontweight='bold',color='black')
plt.text(6,Response[9],'*CHO',fontsize=14,fontweight='bold',color='black')
plt.legend(['U=0 V'],loc='upper right',frameon=True)
plt.savefig(Location+"\CO2RR.png",dpi=500)
plt.show()
