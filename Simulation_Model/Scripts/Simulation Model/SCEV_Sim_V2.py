"""
Global Supply Chain Simulation for EV Production
Supply Chain for Electric Vehicles (SCEV)- Simulation (Sim)
Author: Tareq Alsaleh
Toronto Metropolitan University
Laboratory of Innovation in Transportation 
Supervisor: Dr. Bilal Farooq 

"""

# Import Libraries # 
import searoute as sr
import pandas as pd
import numpy as np
from tqdm import tqdm

# Import Data From the Data File

data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Inputs/Simulation_Inputs_FutureS.csv", encoding='ISO-8859-1') # add absolute path here 

# Set Simulation Counters  

num_iterations = 10000

Cum_EP_Sea_HN = 0 ; Cum_EP_Land_HN = 0 ; Cum_EP_Emissions_HN = 0
Cum_EP_Sea_LFP = 0 ; Cum_EP_Land_LFP = 0 ; Cum_EP_Emissions_LFP = 0
Cum_EP_Sea_NMC = 0 ; Cum_EP_Land_NMC = 0 ; Cum_EP_Emissions_NMC = 0

Cum_PB_Sea_HN = 0 ; Cum_PB_Land_HN = 0 ; Cum_PB_Emissions_HN = 0
Cum_PB_Sea_LFP = 0 ; Cum_PB_Land_LFP = 0 ; Cum_PB_Emissions_LFP = 0
Cum_PB_Sea_NMC = 0 ; Cum_PB_Land_NMC = 0 ; Cum_PB_Emissions_NMC = 0

Cum_BV_Sea_HN = 0 ; Cum_BV_Land_HN = 0 ; Cum_BV_Emissions_HN = 0
Cum_BV_Sea_LFP = 0 ; Cum_BV_Land_LFP = 0 ; Cum_BV_Emissions_LFP = 0
Cum_BV_Sea_NMC = 0 ; Cum_BV_Land_NMC = 0 ; Cum_BV_Emissions_NMC = 0

Cum_VM_Sea_HN = 0 ; Cum_VM_Land_HN = 0 ; Cum_VM_Emissions_HN = 0
Cum_VM_Sea_LFP = 0 ; Cum_VM_Land_LFP = 0 ; Cum_VM_Emissions_LFP = 0
Cum_VM_Sea_NMC = 0 ; Cum_VM_Land_NMC = 0 ; Cum_VM_Emissions_NMC = 0

Cum_High_Ni_Bt = 0 ; Cum_LFP_Bt = 0 ; Cum_NMC_Bt = 0

Cum_Sea_Distance_HNI = 0 ; Cum_Land_HNI = 0
Cum_Sea_Distance_LFP = 0 ; Cum_Land_LFP = 0
Cum_Sea_Distance_NMC = 0 ; Cum_Land_NMC = 0

HN_Counter= 0
LFP_Counter= 0

# Attribute results 
Simulation_results =[]

pbar = tqdm(total=num_iterations)

for i in range(num_iterations):
    
    Li_random_number = np.random.rand() # One random number for each itteration for all choices 
    
    # Selection of Lithium Origin 
    
    Li_choices = data.iloc[0:11, 0]  # Locate the choice set within the data 
    Li_choice_prob = data.iloc[0:11,1] # Locate the probability of each choice within the data 
    Li_comulative_Prob = Li_choice_prob.cumsum() # Calculate the cumulative probabilities for the choice set 
    Selected_Li_index = (Li_comulative_Prob >= Li_random_number).idxmax() # return the row index of the selected choice based on the random number and the comulative probability
    Li_origin_Lat = data.iloc[Selected_Li_index, 3] # return the port latitude coordinates for the selected choice
    Li_origin_Long = data.iloc[Selected_Li_index, 4] # return the port Longitude coordinates for the selected choice
    Li_coor = [Li_origin_Long, Li_origin_Lat] # Construct the coordinates tuple for the selected choice

    # Selection of Lithium Processing Destination
    
    PLi_random_number = np.random.rand()
    
    if Selected_Li_index in {0,1,2,3,4,5,7}:
        PLi_choices= data.iloc[0:1, 6]
        PLi_choice_prob = data.iloc[0:1,7]
        PLi_comulative_Prob = PLi_choice_prob.cumsum()
        if PLi_random_number > sum(PLi_choice_prob):
            Selected_PLi_index =  Selected_Li_index
            PLi_origin_Lat = data.iloc[Selected_Li_index, 3] 
            PLi_origin_Long = data.iloc[Selected_Li_index, 4] 
            PLi_coor = [Li_origin_Long, Li_origin_Lat] 
            Li_PLi = 0  
            Land_Li_PLi =0
            Land_PLi= data.iloc[Selected_Li_index, 5]
        else:
           Selected_PLi_index = (PLi_comulative_Prob >= PLi_random_number).idxmax()
           PLi_Lat = data.iloc[Selected_PLi_index, 9]
           PLi_Long = data.iloc[Selected_PLi_index, 10]
           PLi_coor = [PLi_Long, PLi_Lat]
           
           # Calulate the Sea and Land Distance from the Selected Li Origin to the Proccessing Destination 
           
           Li_PLi = sr.searoute(Li_coor, PLi_coor, units='km') # Obtain the properties from the route between the two ports 
           Li_PLi = Li_PLi.properties['length'] # Report the length in KM for the sea route length 
           
           Land_PLi =  data.iloc[Selected_PLi_index, 11]
           Land_Li_PLi = data.iloc[Selected_Li_index, 5]+ data.iloc[Selected_PLi_index, 11] # Obtain and sum the land distance for the selected choice (Land to Li shipping port + Shipping port to processing location by land) 
    
    else: 
        
        PLi_choices= data.iloc[0:3, 6]
        PLi_choice_prob = data.iloc[0:3,7]
        PLi_comulative_Prob = PLi_choice_prob.cumsum()
        
        if PLi_random_number > sum(PLi_choice_prob): 
            
            Selected_PLi_index =  Selected_Li_index
            
            PLi_origin_Lat = data.iloc[Selected_Li_index, 3] 
            PLi_origin_Long = data.iloc[Selected_Li_index, 4] 
            PLi_coor = [Li_origin_Long, Li_origin_Lat] 
            Li_PLi = 0  
            Land_Li_PLi =0
            Land_PLi= data.iloc[Selected_Li_index, 5]
            
        else: 
            Selected_PLi_index = (PLi_comulative_Prob >= PLi_random_number).idxmax()
            PLi_Lat = data.iloc[Selected_PLi_index, 9]
            PLi_Long = data.iloc[Selected_PLi_index, 10]
            PLi_coor = [PLi_Long, PLi_Lat]
            
            # Calulate the Sea and Land Distance from the Selected Li Origin to the Proccessing Destination 
            
            Li_PLi = sr.searoute(Li_coor, PLi_coor, units='km') # Obtain the properties from the route between the two ports 
            Li_PLi = Li_PLi.properties['length'] # Report the length in KM for the sea route length 
            
            Land_PLi =  data.iloc[Selected_PLi_index, 11]
            
            Land_Li_PLi = data.iloc[Selected_Li_index, 5]+ data.iloc[Selected_PLi_index, 11] # Obtain and sum the land distance for the selected choice (Land to Li shipping port + Shipping port to processing location by land) 
    
        
    
    
    # Selection of Cobalt Origin
    
    Co_random_number = np.random.rand()
    
    Co_choices = data.iloc[11:19, 0] 
    Co_choice_prob = data.iloc[11:19,1] 
    Co_comulative_Prob = Co_choice_prob.cumsum()
    Selected_Co_index = (Co_comulative_Prob >= Co_random_number).idxmax() 
    Co_origin_Lat = data.iloc[Selected_Co_index, 3] 
    Co_origin_Long = data.iloc[Selected_Co_index, 4] 
    Co_coor = [Co_origin_Long, Co_origin_Lat] 
   
    # Selection of Cobalt Processing Destination 
    
    PCo_random_number = np.random.rand()
    
    if Selected_Co_index in {17}:
      
        PCo_choices= data.iloc[12:13, 6]
        PCo_choice_prob = data.iloc[12:13,7]
        PCo_comulative_Prob = PCo_choice_prob.cumsum()
        Selected_PCo_index = (PCo_comulative_Prob >= PCo_random_number).idxmax()
        PCo_Lat = data.iloc[Selected_PCo_index, 9]
        PCo_Long = data.iloc[Selected_PCo_index, 10]
        PCo_coor = [PCo_Long, PCo_Lat]
        
        # Calulate the Sea and Land Distance from the Selected Co Origin to the Proccessing Destination 
        
        Co_PCo = sr.searoute(Co_coor, PCo_coor, units='km')
        Co_PCo = Co_PCo.properties['length']
        
        Land_PCo= data.iloc[Selected_PCo_index, 11]
        Land_Co_PCo = data.iloc[Selected_Co_index, 5]+ data.iloc[Selected_PCo_index, 11]   
           
    else: 
        
        if  Selected_Co_index in {16,18}:
            PCo_choices= data.iloc[11:12, 6]
            PCo_choice_prob = data.iloc[11:12,7]
            PCo_comulative_Prob = PCo_choice_prob.cumsum()
            if PCo_random_number > sum(PCo_choice_prob):
                Selected_PCo_index =  Selected_Co_index
                PCo_origin_Lat = data.iloc[Selected_Co_index, 3] 
                PCo_origin_Long = data.iloc[Selected_Co_index, 4] 
                PCo_coor = [Co_origin_Long, Co_origin_Lat] 
                Co_PCo = 0  
                Land_Co_PCo =0
                Land_PCo= data.iloc[Selected_Co_index, 5]
            else:
               Selected_PCo_index = (PCo_comulative_Prob >= PCo_random_number).idxmax()
               PCo_Lat = data.iloc[Selected_PCo_index, 9]
               PCo_Long = data.iloc[Selected_PCo_index, 10]
               PCo_coor = [PCo_Long, PCo_Lat]
               
               # Calulate the Sea and Land Distance from the Selected Co Origin to the Proccessing Destination 
               
               Co_PCo = sr.searoute(Co_coor, PCo_coor, units='km')
               Co_PCo = Co_PCo.properties['length']
               
               Land_PCo= data.iloc[Selected_PCo_index, 11]
               Land_Co_PCo = data.iloc[Selected_Co_index, 5]+ data.iloc[Selected_PCo_index, 11]
        
        
        else: 
            PCo_choices= data.iloc[11:14, 6]
            PCo_choice_prob = data.iloc[11:14,7]
            PCo_comulative_Prob = PCo_choice_prob.cumsum()
            
            if PCo_random_number > sum(PCo_choice_prob): 
                
                Selected_PCo_index =  Selected_Co_index
                
                PCo_origin_Lat = data.iloc[Selected_Co_index, 3] 
                PCo_origin_Long = data.iloc[Selected_Co_index, 4] 
                PCo_coor = [Co_origin_Long, Co_origin_Lat] 
                Co_PCo = 0       
                Land_Co_PCo =0
                Land_PCo= data.iloc[Selected_Co_index, 5]
                
            else: 
                Selected_PCo_index = (PCo_comulative_Prob >= PCo_random_number).idxmax()
                PCo_Lat = data.iloc[Selected_PCo_index, 9]
                PCo_Long = data.iloc[Selected_PCo_index, 10]
                PCo_coor = [PCo_Long, PCo_Lat]
                
                # Calulate the Sea and Land Distance from the Selected Co Origin to the Proccessing Destination 

                Co_PCo = sr.searoute(Co_coor, PCo_coor, units='km')
                Co_PCo = Co_PCo.properties['length']
                
                Land_PCo= data.iloc[Selected_PCo_index, 11]
                Land_Co_PCo = data.iloc[Selected_Co_index, 5]+ data.iloc[Selected_PCo_index, 11]


    # Selection of Copper Origin  
    
    Cu_random_number = np.random.rand()
    
    Cu_choices = data.iloc[19:29, 0] 
    Cu_choice_prob = data.iloc[19:29,1] 
    Cu_comulative_Prob = Cu_choice_prob.cumsum()
    Selected_Cu_index = (Cu_comulative_Prob >= Cu_random_number).idxmax() 
    Cu_origin_Lat = data.iloc[Selected_Cu_index, 3] 
    Cu_origin_Long = data.iloc[Selected_Cu_index, 4] 
    Cu_coor = [Cu_origin_Long, Cu_origin_Lat] 
   
 
    # Selection of Copper Processing Destination
    
    PCu_random_number = np.random.rand()
    
    PCu_choices= data.iloc[19:22, 6]
    PCu_choice_prob = data.iloc[19:22,7]
    
    if Selected_Cu_index in {23,24,25,26,27,28}:
        PCu_choices= PCu_choices.drop(index=20)
        PCu_choice_prob= PCu_choice_prob.drop(index=20)

    PCu_comulative_Prob = PCu_choice_prob.cumsum()
          
    if PCu_random_number > sum(PCu_choice_prob): 
        
        Selected_PCu_index =  Selected_Cu_index
        
        PCu_origin_Lat = data.iloc[Selected_Cu_index, 3] 
        PCu_origin_Long = data.iloc[Selected_Cu_index, 4] 
        PCu_coor = [Cu_origin_Long, Cu_origin_Lat] 
        Cu_PCu = 0       
        Land_Cu_PCu =0
        Land_PCu= data.iloc[Selected_Cu_index, 5]
        
    else: 
        Selected_PCu_index = (PCu_comulative_Prob >= PCu_random_number).idxmax()
        PCu_Lat = data.iloc[Selected_PCu_index, 9]
        PCu_Long = data.iloc[Selected_PCu_index, 10]
        PCu_coor = [PCu_Long, PCu_Lat]
        
        # Calulate the Sea and Land Distance from the Selected Co Origin to the Proccessing Destination 
        Cu_PCu = sr.searoute(Cu_coor, PCu_coor, units='km')
        Cu_PCu = Cu_PCu.properties['length']
        
        Land_Cu_PCu = data.iloc[Selected_Cu_index, 5]+ data.iloc[Selected_PCu_index, 11]           
        Land_PCu= data.iloc[Selected_PCu_index, 11]       

    # Selection of Nikel Origin
    
    Ni_random_number = np.random.rand()
    
    
    Ni_choices = data.iloc[29:34, 0] 
    Ni_choice_prob = data.iloc[29:34,1] 
    Ni_comulative_Prob = Ni_choice_prob.cumsum()
    Selected_Ni_index = (Ni_comulative_Prob >= Ni_random_number).idxmax() 
    Ni_origin_Lat = data.iloc[Selected_Ni_index, 3] 
    Ni_origin_Long = data.iloc[Selected_Ni_index, 4] 
    Ni_coor = [Ni_origin_Long, Ni_origin_Lat] 
   
    
    #Selection of Nikel Processing Destination
    
    PNi_random_number = np.random.rand()

    if Selected_Ni_index in {31}:
        Selected_PNi_index =  Selected_Ni_index
        
        PNi_origin_Lat = data.iloc[Selected_Ni_index, 3] 
        PNi_origin_Long = data.iloc[Selected_Ni_index, 4] 
        PNi_coor = [Ni_origin_Long, Ni_origin_Lat] 
        Ni_PNi = 0       
        Land_Ni_PNi = 0
        Land_PNi=  data.iloc[Selected_Ni_index, 5]
        
    else:
        
        PNi_choices= data.iloc[29:32, 6]
        PNi_choice_prob = data.iloc[29:32,7]
        PNi_choices = PNi_choices.drop(index=31)
        PNi_choice_prob = PNi_choice_prob.drop(index=31)
        
        PNi_comulative_Prob = PNi_choice_prob.cumsum()
       
        
        if PNi_random_number > sum(PNi_choice_prob): 
            
            Selected_PNi_index =  Selected_Ni_index
            
            PNi_origin_Lat = data.iloc[Selected_Ni_index, 3] 
            PNi_origin_Long = data.iloc[Selected_Ni_index, 4] 
            PNi_coor = [Ni_origin_Long, Ni_origin_Lat] 
            Ni_PNi = 0       
            Land_Ni_PNi = 0
            Land_PNi=  data.iloc[Selected_Ni_index, 5]
            
        else: 
            
           Selected_PNi_index = (PNi_comulative_Prob >= PNi_random_number).idxmax()
           PNi_Lat = data.iloc[Selected_PNi_index, 9]
           PNi_Long = data.iloc[Selected_PNi_index, 10]
           PNi_coor = [PNi_Long, PNi_Lat]
           # Calulate the Sea and Land Distance from the Selected Ni Origin to the Proccessing Destination 
           Ni_PNi = sr.searoute(Ni_coor, PNi_coor, units='km')
           Ni_PNi = Ni_PNi.properties['length']
           
           Land_Ni_PNi =  data.iloc[Selected_Ni_index, 5]+ data.iloc[Selected_PNi_index, 11]
           Land_PNi =  data.iloc[Selected_PNi_index, 11]
        
    # Selection of Manganese Origin
    Mn_random_number = np.random.rand()
    
    Mn_choices = data.iloc[34:40, 0] 
    Mn_choice_prob = data.iloc[34:40,1] 
    Mn_comulative_Prob = Mn_choice_prob.cumsum()
    Selected_Mn_index = (Mn_comulative_Prob >= Mn_random_number).idxmax() 
    Mn_origin_Lat = data.iloc[Selected_Mn_index, 3] 
    Mn_origin_Long = data.iloc[Selected_Mn_index, 4] 
    Mn_coor = [Mn_origin_Long, Mn_origin_Lat] 
   
    
    # Selection of Aluminuim Origin 
    
    Al_random_number = np.random.rand()
    
    Al_choices = data.iloc[40:44, 0] 
    Al_choice_prob = data.iloc[40:44,1]  
    Al_comulative_Prob = Al_choice_prob.cumsum()
    Selected_Al_index = (Al_comulative_Prob >= Al_random_number).idxmax() 
    Al_origin_Lat = data.iloc[Selected_Al_index, 3] 
    Al_origin_Long = data.iloc[Selected_Al_index, 4] 
    Al_coor = [Al_origin_Long, Al_origin_Lat] 
   
  
    # Selection Graphite Origin 
    
    C_random_number = np.random.rand()
    
    C_choices = data.iloc[44:47, 0] 
    C_choice_prob = data.iloc[44:47,1] 
    C_comulative_Prob = C_choice_prob.cumsum()
    Selected_C_index = (C_comulative_Prob >= C_random_number).idxmax() 
    C_origin_Lat = data.iloc[Selected_C_index, 3] 
    C_origin_Long = data.iloc[Selected_C_index, 4] 
    C_coor = [C_origin_Long, C_origin_Lat] 
    
      
    #Selection of Graphite Processing Destination
    
    PC_random_number = np.random.rand()
    
    PC_choices= data.iloc[44:47,6]
    PC_choice_prob = data.iloc[44:47,7]
    PC_comulative_Prob = PC_choice_prob.cumsum()
    Selected_PC_index =(PC_comulative_Prob >= PC_random_number).idxmax()
    PC_Lat = data.iloc[Selected_PC_index, 9]
    PC_Long = data.iloc[Selected_PC_index, 10]
    PC_coor = [PC_Long, PC_Lat]
    
 
    # Calulate the Sea and Land Distance from the Selected Graphite Origin to the Proccessing Destination 

    C_PC = sr.searoute(C_coor,PC_coor, units='km')
    C_PC = C_PC.properties['length']
    
    if C_PC == 0:
        
        Land_C_PC = 0 
        Land_PC = data.iloc[Selected_C_index, 5]
        
    else: 
        
        Land_C_PC = data.iloc[Selected_C_index, 5]+ data.iloc[Selected_PC_index, 11]
        Land_PC =  data.iloc[Selected_PC_index, 11]
    
    
    # Selection of Iron Origin 
    
    Fe_random_number = np.random.rand()
    
    Fe_choices = data.iloc[47:52, 0] 
    Fe_choice_prob = data.iloc[47:52,1] 
    Fe_comulative_Prob = Fe_choice_prob.cumsum()
    Selected_Fe_index = (Fe_comulative_Prob >= Fe_random_number).idxmax() 
    Fe_origin_Lat = data.iloc[Selected_Fe_index, 3] 
    Fe_origin_Long = data.iloc[Selected_Fe_index, 4] 
    Fe_coor = [Fe_origin_Long, Fe_origin_Lat] 
      
    
    # Selection of Silicon Origin
    
    Si_random_number = np.random.rand()
    
    Si_choices = data.iloc[52:57, 0] 
    Si_choice_prob = data.iloc[52:57,1] 
    Si_comulative_Prob = Si_choice_prob.cumsum()
    Selected_Si_index = (Si_comulative_Prob >= Si_random_number).idxmax() 
    Si_origin_Lat = data.iloc[Selected_Si_index, 3] 
    Si_origin_Long = data.iloc[Selected_Si_index, 4] 
    Si_coor = [Si_origin_Long, Si_origin_Lat] 
   
    
    # Selection of Phosphorus Origin 
    
    P_random_number = np.random.rand()
    
    P_choices = data.iloc[57:62, 0] 
    P_choice_prob = data.iloc[57:62,1] 
    P_comulative_Prob = P_choice_prob.cumsum()
    Selected_P_index = (P_comulative_Prob >= P_random_number).idxmax() 
    P_origin_Lat = data.iloc[Selected_P_index, 3] 
    P_origin_Long = data.iloc[Selected_P_index, 4] 
    P_coor = [P_origin_Long, P_origin_Lat] 
    
   
    """    
    ## Selection of Battery Production Hub ## 
    
   """
    B_random_number = np.random.rand()
    
    B_choices = data.iloc[0:54, 12] 
    B_choice_prob = data.iloc[0:54,13] 
    B_comulative_Prob = B_choice_prob.cumsum()
    Selected_B_index = (B_comulative_Prob >= B_random_number).idxmax() 
    B_origin_Lat = data.iloc[Selected_B_index, 15] 
    B_origin_Long = data.iloc[Selected_B_index, 16] 
    B_coor = [B_origin_Long, B_origin_Lat]

  
    """
    ## Calculation of Travel Distance Between Mineral Processing and Battery Production Hubs ## 
    
    """ 
    
    # Calulate the Sea and Land Distance from the Li Proccessing Origin to the Battery production Hub  
    
    PLi_B = sr.searoute(PLi_coor, B_coor, units='km')
    PLi_B = PLi_B.properties['length']
    
    
    Land_PLi_B = Land_PLi + data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Co Processing Origin to the Battery production Hub  

    PCo_B = sr.searoute(PCo_coor, B_coor, units='km')
    PCo_B = PCo_B.properties['length']
    
    Land_PCo_B = Land_PCo + data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Cu Proccessing Origin to the Battery production Hub  

    PCu_B = sr.searoute(PCu_coor, B_coor, units='km')
    PCu_B = PCu_B.properties['length']
    
    Land_PCu_B = Land_PCu + data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Ni Proccessing Origin to the Battery production Hub  
    
    PNi_B = sr.searoute(PNi_coor, B_coor, units='km')
    PNi_B = PNi_B.properties['length']
    
    Land_PNi_B =Land_PNi + data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Mn Proccessing Origin to the Battery production Hub  

    Mn_B = sr.searoute(Mn_coor, B_coor, units='km')
    Mn_B = Mn_B.properties['length']
    
    Land_Mn_B = data.iloc[Selected_Mn_index, 5]+ data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Al Proccessing Origin to the Battery production Hub  

    Al_B = sr.searoute(Al_coor, B_coor, units='km')
    Al_B = Al_B.properties['length']
    
    Land_Al_B= data.iloc[Selected_Al_index, 5]+ data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the C Proccessing Origin to the Battery production Hub  
    
    PC_B = sr.searoute(PC_coor, B_coor, units='km')
    PC_B = PC_B.properties['length']
    
    Land_PC_B = Land_PC + data.iloc[Selected_B_index, 17]

    
    # Calulate the Sea and Land Distance from the Fe Processing Origin to the Battery production Hub  

    Fe_B = sr.searoute(Fe_coor, B_coor, units='km')
    Fe_B = Fe_B.properties['length']
    
    Land_Fe_B = data.iloc[Selected_Fe_index, 5]+ data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the Si Proccessing Origin to the Battery production Hub  

    Si_B = sr.searoute(Si_coor, B_coor, units='km')
    Si_B = Si_B.properties['length']
    
    Land_Si_B = data.iloc[Selected_Si_index, 5]+ data.iloc[Selected_B_index, 17]
    
    # Calulate the Sea and Land Distance from the P Proccessing Origin to the Battery production Hub  

    P_B = sr.searoute(P_coor, B_coor, units='km')
    P_B = P_B.properties['length']
    
    Land_P_B = data.iloc[Selected_P_index, 5]+ data.iloc[Selected_B_index, 17]
    
    
    """    
    ## Selection of Vehicle Production Hub ## 
    
   """
    V_random_number = np.random.rand()
    V_choices = data.iloc[0:52, 18] 
    
    if Selected_B_index in {0,1,2,3,4,5,6,7,8,9,10,13,14,15,17,25,26}:
        V_choice_prob = data.iloc[0:52,19] 
         
    if Selected_B_index in {18,24}:
        V_choice_prob = data.iloc[0:52,20] 
          
    if Selected_B_index in {11,12,19}:
        V_choice_prob = data.iloc[0:52,21] 
       
    if Selected_B_index in {20,21,22,23}:
        V_choice_prob = data.iloc[0:52,22] 
       
    if Selected_B_index in {16}:
        V_choice_prob = data.iloc[0:52,23] 
    
    V_comulative_Prob = V_choice_prob.cumsum()
    Selected_V_index = (V_comulative_Prob >= V_random_number).idxmax() 
    V_origin_Lat = data.iloc[Selected_V_index, 25] 
    V_origin_Long = data.iloc[Selected_V_index, 26] 
    V_coor = [V_origin_Long, V_origin_Lat]

    
    """    
   ## Selection of Market ## 
   
    """
    M_random_number = np.random.rand()
    M_choices = data.iloc[0:40, 28]
    
    if Selected_V_index in {2,5,6,7,8,9,11,15,22}:
        M_choice_prob = data.iloc[0:40,29]
    
    if Selected_V_index in {4,10,13,14,16,17,24}:
        M_choice_prob = data.iloc[0:40,30]
    
    if Selected_V_index in {0,1,3,12,21}:
        M_choice_prob = data.iloc[0:40,31]
        
    if Selected_V_index in {23}:
         M_choice_prob = data.iloc[0:40,32]
    
    if Selected_V_index in {18,19,20}:
        M_choice_prob = data.iloc[0:40,33]
    
    
    M_comulative_Prob = M_choice_prob.cumsum()
    Selected_M_index = (M_comulative_Prob >= M_random_number).idxmax() 
    M_origin_Lat = data.iloc[Selected_M_index, 35] 
    M_origin_Long = data.iloc[Selected_M_index, 36] 
    M_coor = [M_origin_Long, M_origin_Lat]
    
    # Calculate the Sea and Land Distance from the Battery Production Hub to the Vehicle Production Hub 
    
    B_V = sr.searoute(B_coor, V_coor, units='km')
    B_V = B_V.properties['length']
    
    Land_B_V= data.iloc[Selected_B_index, 17]+ data.iloc[Selected_V_index, 27]
    
  
  # Calculate the Sea and Land Distance from the Vehicle Production Hub to the Market 
  
    V_M = sr.searoute(V_coor, M_coor, units='km')
    V_M = V_M.properties['length']
  
    Land_V_M= data.iloc[Selected_V_index, 27]+ data.iloc[Selected_M_index, 37]
    
   
    """
    Calucation of Emissions As per Battery Type 
    
    """ 
    
    # Emissions Factor 
    
    LE = (0.09545/1000) ## Land Transport Emission Factor _Not for Vehicles Transport 
    LE_V = (0.0742050590604027/1000) ## Land Transport Emission Factor _ for Vehicles Transport
    LE_Ave = (LE+LE_V)/2
    
    SE_Bulk = (0.00353380456375839/1000) ## Sea Transport Emission Factor_ Bulk Cargo _Mineral Ore
    SE_Container = (0.0161185697986577/1000)  ## Sea Transport Emission Factor_ Bulk Cargo _Battery
    SE_Vehicle =  (0.0385229575838926/1000) ## Sea Transport Emission Factor_ Bulk Cargo _Battery
    SE_Ave= (SE_Bulk+SE_Container+SE_Vehicle)/3
    
    
    # Weights of Material at different stages in Kg
    
    # Bulk Material weight of minierals- The mass flows associated with these materials (i.e., how much earth is moved) relies on ore grade and through-process yield: 
        
    HN_NiW = 0.75/0.79
    HN_CuW = 0.17/0.81
    HN_LiW = 0.54/0.58
    HN_CW= 0.59/0.86
    HN_AlW = 0.09/0.9
    HN_SiW = 0.04/0.38
    HN_BW = (2.18/2.9)* 6.78
    
    # Emission Calculations Based on Weight and Battery Type 
    
    # High Niekel Battery:
    
        
    if (0 <= Selected_V_index <= 4) or (9 <= Selected_V_index <= 41):
        
        HN_Counter +=1
        
        # Extraction to Processing: 
            
        EP_Sea_HN = (HN_NiW *Ni_PNi*SE_Bulk)+ (HN_CuW *Cu_PCu*SE_Bulk)+ (HN_LiW *Li_PLi*SE_Bulk)+ (HN_CW * C_PC *SE_Bulk) 
        EP_Land_HN= (HN_NiW *Land_Ni_PNi*LE)+(HN_CuW *Land_Cu_PCu *LE) + (HN_LiW *Land_Li_PLi *LE) + (HN_CW *Land_C_PC *LE) 
        
        EP_Emissions_HN = EP_Sea_HN + EP_Land_HN

        # Processing to Battery: 
             
        PB_Sea_HN= (0.75 *PNi_B*SE_Bulk)+ (0.17 *PCu_B*SE_Bulk) + (0.54 *PLi_B*SE_Bulk) + (0.59* PC_B *SE_Bulk) + (0.09 *Al_B*SE_Bulk) +  (0.04*Si_B* SE_Bulk) 
     
        PB_Land_HN= (0.75*Land_PNi_B*LE) + (0.17*Land_PCu_B*LE) + (0.54*Land_PLi_B*LE) +  (0.59*Land_PC_B*LE) + (0.09 *Land_Al_B*LE)+ (0.04*Land_Si_B*LE)
           
        PB_Emissions_HN = PB_Sea_HN + PB_Land_HN
        
        # Battery to Vehicle: 
        
        BV_Sea_HN = (HN_BW*B_V*SE_Container)
        BV_Land_HN = (HN_BW*Land_B_V*LE)
        
        BV_Emissions_HN = BV_Sea_HN + BV_Land_HN 
        
        # Vehicle to Market 
        
        if 0 <= Selected_V_index <= 4 :
            
            VM_Sea_HN= (27.52*V_M*SE_Vehicle)
            VM_Land_HN = (27.52*Land_V_M*LE_V)
            
        elif  5 <= Selected_V_index <=8: 
            VM_Sea_HN= (30.33*V_M*SE_Vehicle)
            VM_Land_HN = (30.33*Land_V_M*LE_V)
            

        elif  9 <= Selected_V_index <=17: 
            VM_Sea_HN= (27.42*V_M*SE_Vehicle)
            VM_Land_HN = (27.42*Land_V_M*LE_V)
           
        else :
            
            VM_Sea_HN= (30.36*V_M*SE_Vehicle)
            VM_Land_HN = (30.36*Land_V_M*LE_V)
        
        VM_Emissions_HN = VM_Sea_HN + VM_Land_HN
        
        # Total Emmissions for the Supply Chain of High Nickel battery vehicles.  
         
        High_Ni_Supply_Emissions_Total = EP_Emissions_HN+  PB_Emissions_HN + BV_Emissions_HN +  VM_Emissions_HN
        
        # Record Averages: 
        
            # Extraction to Processing Sea & Land 
                    
        Cum_EP_Sea_HN += EP_Sea_HN 
        Cum_EP_Land_HN += EP_Land_HN  
        Cum_EP_Emissions_HN +=  EP_Emissions_HN
        
        Av_EP_Sea_HN = Cum_EP_Sea_HN / HN_Counter
        Av_EP_Land_HN  = Cum_EP_Land_HN / HN_Counter 
        Av_EP_Emissions_HN =  Cum_EP_Emissions_HN /HN_Counter
        
           # Processing to Battery Sea and Land
           
        Cum_PB_Sea_HN += PB_Sea_HN 
        Cum_PB_Land_HN += PB_Land_HN  
        Cum_PB_Emissions_HN +=  PB_Emissions_HN
        
        Av_PB_Sea_HN = Cum_PB_Sea_HN / HN_Counter
        Av_PB_Land_HN  = Cum_PB_Land_HN / HN_Counter
        Av_PB_Emissions_HN =  Cum_PB_Emissions_HN /HN_Counter
        
          # Battery to Vehicle Sea and Land:
              
        Cum_BV_Sea_HN += BV_Sea_HN 
        Cum_BV_Land_HN += BV_Land_HN  
        Cum_BV_Emissions_HN +=  BV_Emissions_HN
        
        Av_BV_Sea_HN = Cum_BV_Sea_HN / HN_Counter
        Av_BV_Land_HN  = Cum_BV_Land_HN / HN_Counter
        Av_BV_Emissions_HN =  Cum_BV_Emissions_HN /HN_Counter
        
          # Vehicle to Market:    
            
        Cum_VM_Sea_HN += VM_Sea_HN
        Cum_VM_Land_HN += VM_Land_HN  
        Cum_VM_Emissions_HN +=  VM_Emissions_HN
        
        
        Av_VM_Sea_HN = Cum_VM_Sea_HN / HN_Counter 
        Av_VM_Land_HN = Cum_VM_Land_HN / HN_Counter 
        Av_VM_Emissions_HN =  Cum_VM_Emissions_HN /HN_Counter
        
         # Total 
         
        Cum_High_Ni_Bt +=  High_Ni_Supply_Emissions_Total
        Average_High_Ni_Emissions_Bt = Cum_High_Ni_Bt/ HN_Counter
        
        # Distances
        
        Total_Sea_Distance_HNI = Li_PLi + PLi_B + Cu_PCu + PCu_B + Ni_PNi + PNi_B + C_PC+ PC_B+ Al_B+ Si_B+ B_V +V_M    
        Total_Land_Distance_HNI = Land_Li_PLi+ Land_PLi_B + Land_Cu_PCu + Land_PCu_B + Land_Ni_PNi + Land_PNi_B +Land_C_PC + Land_PC_B +  Land_Al_B  + Land_Si_B + Land_B_V + Land_V_M
        
        Cum_Sea_Distance_HNI += Total_Sea_Distance_HNI
        Average_Sea_Distance_HNI = Cum_Sea_Distance_HNI/HN_Counter
        
        Cum_Land_HNI += Total_Land_Distance_HNI
        Average_Land_HNI = Cum_Land_HNI/HN_Counter
        
    else: 
        
        if HN_Counter == 0 :
            
            HN_Counter = 1
            
        else: HN_Counter = HN_Counter
            
        
        EP_Sea_HN = 0
        EP_Land_HN= 0
        EP_Emissions_HN = 0

        PB_Sea_HN= 0
        PB_Land_HN= 0
        PB_Emissions_HN = 0
        
        BV_Sea_HN = 0
        BV_Land_HN = 0
        BV_Emissions_HN =0
        
        VM_Sea_HN= 0
        VM_Land_HN =0
        VM_Emissions_HN = 0
        
        High_Ni_Supply_Emissions_Total = 0
        
        Total_Sea_Distance_HNI = 0
        Total_Land_Distance_HNI = 0
        
        # Record Averages: 
        
            # Extraction to Processing Sea & Land 
                    
        Cum_EP_Sea_HN += EP_Sea_HN 
        Cum_EP_Land_HN += EP_Land_HN  
        Cum_EP_Emissions_HN +=  EP_Emissions_HN
        
        Av_EP_Sea_HN = Cum_EP_Sea_HN / HN_Counter
        Av_EP_Land_HN  = Cum_EP_Land_HN / HN_Counter 
        Av_EP_Emissions_HN =  Cum_EP_Emissions_HN /HN_Counter
        
           # Processing to Battery Sea and Land
           
        Cum_PB_Sea_HN += PB_Sea_HN 
        Cum_PB_Land_HN += PB_Land_HN  
        Cum_PB_Emissions_HN +=  PB_Emissions_HN
        
        Av_PB_Sea_HN = Cum_PB_Sea_HN / HN_Counter
        Av_PB_Land_HN  = Cum_PB_Land_HN / HN_Counter
        Av_PB_Emissions_HN =  Cum_PB_Emissions_HN /HN_Counter
        
          # Battery to Vehicle Sea and Land:
              
        Cum_BV_Sea_HN += BV_Sea_HN 
        Cum_BV_Land_HN += BV_Land_HN  
        Cum_BV_Emissions_HN +=  BV_Emissions_HN
        
        Av_BV_Sea_HN = Cum_BV_Sea_HN / HN_Counter
        Av_BV_Land_HN  = Cum_BV_Land_HN / HN_Counter
        Av_BV_Emissions_HN =  Cum_BV_Emissions_HN /HN_Counter
        
          # Vehicle to Market:    
            
        Cum_VM_Sea_HN += VM_Sea_HN
        Cum_VM_Land_HN += VM_Land_HN  
        Cum_VM_Emissions_HN +=  VM_Emissions_HN
        
        
        Av_VM_Sea_HN = Cum_VM_Sea_HN / HN_Counter 
        Av_VM_Land_HN = Cum_VM_Land_HN / HN_Counter 
        Av_VM_Emissions_HN =  Cum_VM_Emissions_HN /HN_Counter
        
         # Total 
         
        Cum_High_Ni_Bt +=  High_Ni_Supply_Emissions_Total
        Average_High_Ni_Emissions_Bt = Cum_High_Ni_Bt/ HN_Counter
        
        # Distances
        
        Total_Sea_Distance_HNI = Li_PLi + PLi_B + Cu_PCu + PCu_B + Ni_PNi + PNi_B + C_PC+ PC_B+ Al_B+ Si_B+ B_V +V_M    
        Total_Land_Distance_HNI = Land_Li_PLi+ Land_PLi_B + Land_Cu_PCu + Land_PCu_B + Land_Ni_PNi + Land_PNi_B +Land_C_PC + Land_PC_B +  Land_Al_B  + Land_Si_B + Land_B_V + Land_V_M
        
        Cum_Sea_Distance_HNI += Total_Sea_Distance_HNI
        Average_Sea_Distance_HNI = Cum_Sea_Distance_HNI/HN_Counter
        
        Cum_Land_HNI += Total_Land_Distance_HNI
        Average_Land_HNI = Cum_Land_HNI/HN_Counter
        
    # LFP Battery : 

    LFP_CuW = 0.27/0.81
    LFP_LiW = 0.61/0.58
    LFP_CW= 1.05/0.86
    LFP_AlW = 0.33/0.9
    LFP_FeW = 0.78/0.65
    LFP_PW = 0.42/0.5
    LFP_BW = (3.46/2.9)* 6.78
    
    
    if 0 <= Selected_V_index <= 8 :
        
        LFP_Counter +=1
        
        # Extraction to Processing 
        
        EP_Sea_LFP = (LFP_CuW *Cu_PCu*SE_Bulk)+ (LFP_LiW *Li_PLi*SE_Bulk)+ (LFP_CW * C_PC *SE_Bulk) 
        EP_Land_LFP = (LFP_CuW *Land_Cu_PCu *LE) + (LFP_LiW *Land_Li_PLi *LE) + (LFP_CW *Land_C_PC *LE) 
         
        EP_Emissions_LFP = EP_Sea_LFP + EP_Land_LFP
        
        
        # Processing to Battery: 
             
        PB_Sea_LFP= (0.27 *PCu_B*SE_Bulk) + (0.61 *PLi_B*SE_Bulk) + (1.05* PC_B *SE_Bulk) + (0.33 *Al_B*SE_Bulk) +  (0.78*Fe_B*SE_Bulk) + (0.42 *P_B*SE_Bulk)
     
        PB_Land_LFP= (0.27*Land_PCu_B*LE) + (0.61*Land_PLi_B*LE) +  (1.05*Land_PC_B*LE) + (0.33 *Land_Al_B*LE)+ (0.78 *Land_Fe_B*LE) + (0.42 *Land_P_B*LE)
           
        PB_Emissions_LFP = PB_Sea_LFP + PB_Land_LFP
        
       
        # Battery to Vehicle: 
        
        BV_Sea_LFP = (LFP_BW*B_V*SE_Container)
        BV_Land_LFP = (LFP_BW*Land_B_V*LE)
        
        BV_Emissions_LFP = BV_Sea_LFP + BV_Land_LFP
        
        
        # Vehicle to Market 
        
        if 0 <= Selected_V_index <= 4 :
            
            VM_Sea_LFP= (27.52*V_M*SE_Vehicle)
            VM_Land_LFP = (27.52*Land_V_M*LE_V)
            
        elif  5 <= Selected_V_index <=8: 
            VM_Sea_LFP= (30.33*V_M*SE_Vehicle)
            VM_Land_LFP = (30.33*Land_V_M*LE_V)
            

        elif  9 <= Selected_V_index <=17: 
            VM_Sea_LFP= (27.42*V_M*SE_Vehicle)
            VM_Land_LFP = (27.42*Land_V_M*LE_V)
           
        else :
            
            VM_Sea_LFP= (30.36*V_M*SE_Vehicle)
            VM_Land_LFP = (30.36*Land_V_M*LE_V)
        
        VM_Emissions_LFP = VM_Sea_LFP + VM_Land_LFP
        
        # Total Emmissions for the Supply Chain of LFP battery vehicles.  
         
        LFP_Supply_Emissions_Total = EP_Emissions_LFP+  PB_Emissions_LFP + BV_Emissions_LFP +  VM_Emissions_LFP
        
        # Counter ana Record Averages: 
        
            # Extraction to Processing Sea & Land 
                    
        Cum_EP_Sea_LFP += EP_Sea_LFP 
        Cum_EP_Land_LFP += EP_Land_LFP  
        Cum_EP_Emissions_LFP +=  EP_Emissions_LFP
         
        Av_EP_Sea_LFP = Cum_EP_Sea_LFP / LFP_Counter
        Av_EP_Land_LFP  = Cum_EP_Land_LFP / LFP_Counter
        Av_EP_Emissions_LFP =  Cum_EP_Emissions_LFP /LFP_Counter
        
           # Processing to Battery Sea and Land
           
        Cum_PB_Sea_LFP += PB_Sea_LFP 
        Cum_PB_Land_LFP += PB_Land_LFP  
        Cum_PB_Emissions_LFP +=  PB_Emissions_LFP
     
        Av_PB_Sea_LFP = Cum_PB_Sea_LFP / LFP_Counter 
        Av_PB_Land_LFP  = Cum_PB_Land_LFP / LFP_Counter
        Av_PB_Emissions_LFP =  Cum_PB_Emissions_LFP /LFP_Counter
        
          # Battery to Vehicle Sea and Land:
               
        Cum_BV_Sea_LFP += BV_Sea_LFP 
        Cum_BV_Land_LFP += BV_Land_LFP  
        Cum_BV_Emissions_LFP +=  BV_Emissions_LFP
        
        Av_BV_Sea_LFP = Cum_BV_Sea_LFP / LFP_Counter
        Av_BV_Land_LFP  = Cum_BV_Land_LFP / LFP_Counter
        Av_BV_Emissions_LFP =  Cum_BV_Emissions_LFP /LFP_Counter
        
          # Vehilce to Market 
          
        Cum_VM_Sea_LFP += VM_Sea_LFP
        Cum_VM_Land_LFP += VM_Land_LFP  
        Cum_VM_Emissions_LFP +=  VM_Emissions_LFP
        
        Av_VM_Sea_LFP = Cum_VM_Sea_LFP / LFP_Counter
        Av_VM_Land_LFP = Cum_VM_Land_LFP / LFP_Counter 
        Av_VM_Emissions_LFP =  Cum_VM_Emissions_LFP / LFP_Counter
        
        # Record Total Emmissions 

        Cum_LFP_Bt += LFP_Supply_Emissions_Total
        Average_LFP_Supply_Emissions_Bt = Cum_LFP_Bt/ LFP_Counter
        
        # Distances 
        
        Total_Sea_Distance_LFP = Li_PLi + PLi_B + Cu_PCu + PCu_B + C_PC+ PC_B+ Al_B+ Fe_B + P_B + B_V + V_M    
        Total_Land_Distance_LFP = Land_Li_PLi + Land_PLi_B + Land_Cu_PCu + Land_PCu_B + Land_C_PC + Land_PC_B+ Land_Al_B + Land_Fe_B + Land_P_B + Land_B_V + Land_V_M
        
        Cum_Sea_Distance_LFP += Total_Sea_Distance_LFP
        Average_Sea_Distance_LFP = Cum_Sea_Distance_LFP/LFP_Counter
        
        Cum_Land_LFP += Total_Land_Distance_LFP
        Average_Land_LFP = Cum_Land_LFP/LFP_Counter
        
    else: 
        
        if LFP_Counter == 0 :
            
            LFP_Counter = 1
            
        else: LFP_Counter = LFP_Counter
        
    
        EP_Sea_LFP = 0
        EP_Land_LFP= 0
        EP_Emissions_LFP = 0

        PB_Sea_LFP= 0
        PB_Land_LFP= 0
        PB_Emissions_LFP = 0
        
        BV_Sea_LFP = 0
        BV_Land_LFP = 0
        BV_Emissions_LFP =0
        
        VM_Sea_LFP= 0
        VM_Land_LFP =0
        VM_Emissions_LFP = 0
        
        LFP_Supply_Emissions_Total = 0
        
        Total_Sea_Distance_LFP = 0
        Total_Land_Distance_LFP = 0
        
        # Counter ana Record Averages: 
        
            # Extraction to Processing Sea & Land 
                    
        Cum_EP_Sea_LFP += EP_Sea_LFP 
        Cum_EP_Land_LFP += EP_Land_LFP  
        Cum_EP_Emissions_LFP +=  EP_Emissions_LFP
         
        Av_EP_Sea_LFP = Cum_EP_Sea_LFP / LFP_Counter
        Av_EP_Land_LFP  = Cum_EP_Land_LFP / LFP_Counter
        Av_EP_Emissions_LFP =  Cum_EP_Emissions_LFP /LFP_Counter
        
           # Processing to Battery Sea and Land
           
        Cum_PB_Sea_LFP += PB_Sea_LFP 
        Cum_PB_Land_LFP += PB_Land_LFP  
        Cum_PB_Emissions_LFP +=  PB_Emissions_LFP
     
        Av_PB_Sea_LFP = Cum_PB_Sea_LFP / LFP_Counter 
        Av_PB_Land_LFP  = Cum_PB_Land_LFP / LFP_Counter
        Av_PB_Emissions_LFP =  Cum_PB_Emissions_LFP /LFP_Counter
        
          # Battery to Vehicle Sea and Land:
               
        Cum_BV_Sea_LFP += BV_Sea_LFP 
        Cum_BV_Land_LFP += BV_Land_LFP  
        Cum_BV_Emissions_LFP +=  BV_Emissions_LFP
        
        Av_BV_Sea_LFP = Cum_BV_Sea_LFP / LFP_Counter
        Av_BV_Land_LFP  = Cum_BV_Land_LFP / LFP_Counter
        Av_BV_Emissions_LFP =  Cum_BV_Emissions_LFP /LFP_Counter
        
          # Vehilce to Market 
          
        Cum_VM_Sea_LFP += VM_Sea_LFP
        Cum_VM_Land_LFP += VM_Land_LFP  
        Cum_VM_Emissions_LFP +=  VM_Emissions_LFP
        
        Av_VM_Sea_LFP = Cum_VM_Sea_LFP / LFP_Counter
        Av_VM_Land_LFP = Cum_VM_Land_LFP / LFP_Counter 
        Av_VM_Emissions_LFP =  Cum_VM_Emissions_LFP / LFP_Counter
        
        # Record Total Emmissions 

        Cum_LFP_Bt += LFP_Supply_Emissions_Total
        Average_LFP_Supply_Emissions_Bt = Cum_LFP_Bt/ LFP_Counter
        
        # Distances 
        
        Total_Sea_Distance_LFP = Li_PLi + PLi_B + Cu_PCu + PCu_B + C_PC+ PC_B+ Al_B+ Fe_B + P_B + B_V + V_M    
        Total_Land_Distance_LFP = Land_Li_PLi + Land_PLi_B + Land_Cu_PCu + Land_PCu_B + Land_C_PC + Land_PC_B+ Land_Al_B + Land_Fe_B + Land_P_B + Land_B_V + Land_V_M
        
        Cum_Sea_Distance_LFP += Total_Sea_Distance_LFP
        Average_Sea_Distance_LFP = Cum_Sea_Distance_LFP/LFP_Counter
        
        Cum_Land_LFP += Total_Land_Distance_LFP
        Average_Land_LFP = Cum_Land_LFP/LFP_Counter
        
    # NMC Battery :
    NMC_NiW = 0.4/0.79  
    NMC_CuW = 0.23/0.81
    NMC_LiW = 0.63/0.58
    NMC_CoW = 0.06/0.77
    NMC_CW= 0.89/0.86
    NMC_AlW = 0.12/0.9
    NMC_MnW = 0.73/0.75
    NMC_BW = (3.06/2.9)* 6.78
    
    if 0 <= Selected_V_index <= 41 :
        
        # Extraction to Processing 
        
        EP_Sea_NMC = (NMC_NiW *Ni_PNi*SE_Bulk)+(NMC_CuW *Cu_PCu*SE_Bulk)+ (NMC_LiW *Li_PLi*SE_Bulk)+ (NMC_CoW * Co_PCo*SE_Bulk) + (NMC_CW * C_PC *SE_Bulk) 
        EP_Land_NMC = (NMC_NiW *Land_Ni_PNi *LE) + (NMC_CuW *Land_Cu_PCu *LE) + (NMC_LiW *Land_Li_PLi *LE) +(NMC_CoW *Land_Co_PCo *LE)+ (NMC_CW *Land_C_PC *LE) 
         
        EP_Emissions_NMC = EP_Sea_NMC + EP_Land_NMC
        
        # Processing to Battery: 
             
        PB_Sea_NMC= (0.4 *PNi_B*SE_Bulk) + (0.23 *PCu_B*SE_Bulk) + (0.63 *PLi_B*SE_Bulk) + (0.06 *PCo_B*SE_Bulk)+ (0.89* PC_B *SE_Bulk) + (0.12 *Al_B*SE_Bulk) +  (0.73*Mn_B*SE_Bulk) 
     
        PB_Land_NMC= (0.4 *Land_PNi_B*LE) + (0.23*Land_PCu_B*LE) + (0.63*Land_PLi_B*LE) + (0.06 *Land_PCo_B*LE) + (0.89 *Land_PC_B*LE) + (0.12 *Land_Al_B*LE)+ (0.73 *Land_Mn_B*LE) 
           
        PB_Emissions_NMC = PB_Sea_NMC + PB_Land_NMC
        
        # Battery to Vehicle: 
        
        BV_Sea_NMC = (NMC_BW*B_V*SE_Container)
        BV_Land_NMC = (NMC_BW*Land_B_V*LE)
        
        BV_Emissions_NMC = BV_Sea_NMC + BV_Land_NMC
        
        
        # Vehicle to Market 
        
        if 0 <= Selected_V_index <= 4 :
            
            VM_Sea_NMC= (27.52*V_M*SE_Vehicle)
            VM_Land_NMC = (27.52*Land_V_M*LE_V)
            
        elif  5 <= Selected_V_index <=8: 
            VM_Sea_NMC= (30.33*V_M*SE_Vehicle)
            VM_Land_NMC = (30.33*Land_V_M*LE_V)
            

        elif  9 <= Selected_V_index <=17: 
            VM_Sea_NMC= (27.42*V_M*SE_Vehicle)
            VM_Land_NMC= (27.42*Land_V_M*LE_V)
           
        else :
            
            VM_Sea_NMC= (30.36*V_M*SE_Vehicle)
            VM_Land_NMC = (30.36*Land_V_M*LE_V)
        
        VM_Emissions_NMC = VM_Sea_NMC + VM_Land_NMC
        
        NMC_Supply_Emissions_Total = EP_Emissions_NMC+  PB_Emissions_NMC + BV_Emissions_NMC +  VM_Emissions_NMC
        
        # Record Extraction to processing emissions both sea and land: 
     
        Cum_EP_Sea_NMC += EP_Sea_NMC 
        Cum_EP_Land_NMC += EP_Land_NMC  
        Cum_EP_Emissions_NMC +=  EP_Emissions_NMC
        
        Av_EP_Sea_NMC = Cum_EP_Sea_NMC / (i+1) 
        Av_EP_Land_NMC  = Cum_EP_Land_NMC / (i+1) 
        Av_EP_Emissions_NMC =  Cum_EP_Emissions_NMC /(i+1)
        
        # Record Processing to Battery emissions both sea and land:

        Cum_PB_Sea_NMC += PB_Sea_NMC 
        Cum_PB_Land_NMC += PB_Land_NMC  
        Cum_PB_Emissions_NMC +=  PB_Emissions_NMC
        
        Av_PB_Sea_NMC = Cum_PB_Sea_NMC / (i+1) 
        Av_PB_Land_NMC  = Cum_PB_Land_NMC / (i+1) 
        Av_PB_Emissions_NMC =  Cum_PB_Emissions_NMC /(i+1)

        # Record Battery to Vehicle both sea and land:
        
        Cum_BV_Sea_NMC += BV_Sea_NMC 
        Cum_BV_Land_NMC += BV_Land_NMC  
        Cum_BV_Emissions_NMC +=  BV_Emissions_NMC

        Av_BV_Sea_NMC = Cum_BV_Sea_NMC / (i+1) 
        Av_BV_Land_NMC  = Cum_BV_Land_NMC / (i+1) 
        Av_BV_Emissions_NMC =  Cum_BV_Emissions_NMC /(i+1)
        
       # Record Vehicle to Market both sea and land:   
           
        Cum_VM_Sea_NMC += VM_Sea_NMC
        Cum_VM_Land_NMC += VM_Land_NMC  
        Cum_VM_Emissions_NMC +=  VM_Emissions_NMC
        
        Av_VM_Sea_NMC = Cum_VM_Sea_NMC / (i+1) 
        Av_VM_Land_NMC = Cum_VM_Land_NMC / (i+1) 
        Av_VM_Emissions_NMC =  Cum_VM_Emissions_NMC /(i+1)
        
        # Record Total Emmissions 
        
        Cum_NMC_Bt += NMC_Supply_Emissions_Total
        Average_NMCSupply_Emissions_Bt = Cum_NMC_Bt/ (i+1)
        
        # Record Distances: 
        
        Total_Sea_Distance_NMC = Li_PLi + PLi_B + Co_PCo + PCo_B + Cu_PCu +  PCu_B + Ni_PNi + PNi_B + C_PC + PC_B+ Mn_B + Al_B+ B_V +V_M    
        Total_Land_Distance_NMC = Land_Li_PLi + Land_PLi_B +Land_Co_PCo + Land_PCo_B + Land_Cu_PCu + Land_PCu_B + Land_Ni_PNi + Land_PNi_B + Land_C_PC+ Land_PC_B+ Land_Mn_B + Land_Al_B + Land_B_V +Land_V_M
        
        Cum_Sea_Distance_NMC += Total_Sea_Distance_NMC
        Average_Sea_Distance_NMC = Cum_Sea_Distance_NMC/(i+1)
        
        Cum_Land_NMC += Total_Land_Distance_NMC
        Average_Land_NMC = Cum_Land_NMC/(i+1)
        
        
        
    # Attributing Results: 
        
        
    row =[]
    results =  High_Ni_Supply_Emissions_Total, Average_High_Ni_Emissions_Bt, \
        LFP_Supply_Emissions_Total , Average_LFP_Supply_Emissions_Bt, \
        NMC_Supply_Emissions_Total , Average_NMCSupply_Emissions_Bt, \
            Selected_Li_index, Selected_PLi_index , Selected_Co_index, Selected_PCo_index,\
                Selected_Cu_index, Selected_PCu_index, Selected_Ni_index, Selected_PNi_index,\
                Selected_C_index, Selected_PC_index, Selected_Mn_index, Selected_Al_index, \
                          Selected_Fe_index,  Selected_Si_index, Selected_P_index, Selected_B_index,\
                              Selected_V_index, Selected_M_index, Average_Sea_Distance_HNI, Average_Land_HNI, \
                                  Average_Sea_Distance_LFP, Average_Land_LFP, Average_Sea_Distance_NMC, Average_Land_NMC, \
                                     EP_Sea_HN , Av_EP_Sea_HN, EP_Land_HN, Av_EP_Land_HN, EP_Emissions_HN, Av_EP_Emissions_HN, \
                                         EP_Sea_LFP , Av_EP_Sea_LFP, EP_Land_LFP, Av_EP_Land_LFP, EP_Emissions_LFP, Av_EP_Emissions_LFP, \
                                             EP_Sea_NMC , Av_EP_Sea_NMC, EP_Land_NMC, Av_EP_Land_NMC, EP_Emissions_NMC, Av_EP_Emissions_NMC, \
                                                 PB_Sea_HN , Av_PB_Sea_HN, PB_Land_HN, Av_PB_Land_HN, PB_Emissions_HN, Av_PB_Emissions_HN, \
                                                     PB_Sea_LFP , Av_PB_Sea_LFP, PB_Land_LFP, Av_PB_Land_LFP, PB_Emissions_LFP, Av_PB_Emissions_LFP, \
                                                         PB_Sea_NMC , Av_PB_Sea_NMC, PB_Land_NMC, Av_PB_Land_NMC, PB_Emissions_NMC, Av_PB_Emissions_NMC, \
                                                             BV_Sea_HN, Av_BV_Sea_HN, BV_Land_HN,  Av_BV_Land_HN, BV_Emissions_HN, Av_BV_Emissions_HN, \
                                                                 BV_Sea_LFP, Av_BV_Sea_LFP, BV_Land_LFP,  Av_BV_Land_LFP, BV_Emissions_LFP, Av_BV_Emissions_LFP, \
                                                                     BV_Sea_NMC, Av_BV_Sea_NMC, BV_Land_NMC,  Av_BV_Land_NMC, BV_Emissions_NMC, Av_BV_Emissions_NMC, \
                                                                         VM_Sea_HN, Av_VM_Sea_HN , VM_Land_HN, Av_VM_Land_HN, VM_Emissions_HN, Av_VM_Emissions_HN, \
                                                                             VM_Sea_LFP, Av_VM_Sea_LFP, VM_Land_LFP, Av_VM_Land_LFP, VM_Emissions_LFP, Av_VM_Emissions_LFP, \
                                                                                 VM_Sea_NMC, Av_VM_Sea_NMC , VM_Land_NMC, Av_VM_Land_NMC, VM_Emissions_NMC, Av_VM_Emissions_NMC, \
                                                                         
                                                                             
                     
    Simulation_results.append(results)
    
    pbar.update(1)  # Increment the progress bar by one
    
pbar.close()

sumulation_table = pd.DataFrame(Simulation_results)
column_headers = ['High_Ni_Supply_Emissions_Total', 'Average_High_Ni_Emissions_Bt', \
    'LFP_Supply_Emissions_Total' , 'Average_LFP_Supply_Emissions_Bt', \
    'NMC_Supply_Emissions_Total' , 'Average_NMCSupply_Emissions_Bt', \
        'Selected_Li_index', 'Selected_PLi_index' , 'Selected_Co_index', 'Selected_PCo_index',\
            'Selected_Cu_index', 'Selected_PCu_index', 'Selected_Ni_index', 'Selected_PNi_index',\
            'Selected_C_index', 'Selected_PC_index', 'Selected_Mn_index', 'Selected_Al_index', \
                      'Selected_Fe_index',  'Selected_Si_index', 'Selected_P_index', 'Selected_B_index',\
                          'Selected_V_index', 'Selected_M_index', 'Average_Sea_Distance_HNI', 'Average_Land_HNI', \
                              'Average_Sea_Distance_LFP', 'Average_Land_LFP', 'Average_Sea_Distance_NMC', 'Average_Land_NMC', \
                                 'EP_Sea_HN' , 'Av_EP_Sea_HN', 'EP_Land_HN', 'Av_EP_Land_HN','EP_Emissions_HN', 'Av_EP_Emissions_HN', \
                                     'EP_Sea_LFP' , 'Av_EP_Sea_LFP', 'EP_Land_LFP', 'Av_EP_Land_LFP', 'EP_Emissions_LFP', 'Av_EP_Emissions_LFP', \
                                         'EP_Sea_NMC' ,'Av_EP_Sea_NMC', 'EP_Land_NMC', 'Av_EP_Land_NMC', 'EP_Emissions_NMC', 'Av_EP_Emissions_NMC', \
                                             'PB_Sea_HN' , 'Av_PB_Sea_HN', 'PB_Land_HN','Av_PB_Land_HN', 'PB_Emissions_HN', 'Av_PB_Emissions_HN', \
                                                 'PB_Sea_LFP' , 'Av_PB_Sea_LFP', 'PB_Land_LFP', 'Av_PB_Land_LFP', 'PB_Emissions_LFP', 'Av_PB_Emissions_LFP', \
                                                    'PB_Sea_NMC' , 'Av_PB_Sea_NMC', 'PB_Land_NMC', 'Av_PB_Land_NMC', 'PB_Emissions_NMC', 'Av_PB_Emissions_NMC', \
                                                         'BV_Sea_HN', 'Av_BV_Sea_HN', 'BV_Land_HN',  'Av_BV_Land_HN', 'BV_Emissions_HN', 'Av_BV_Emissions_HN', \
                                                             'BV_Sea_LFP', 'Av_BV_Sea_LFP','BV_Land_LFP',  'Av_BV_Land_LFP', 'BV_Emissions_LFP', 'Av_BV_Emissions_LFP', \
                                                                 'BV_Sea_NMC', 'Av_BV_Sea_NMC', 'BV_Land_NMC',  'Av_BV_Land_NMC', 'BV_Emissions_NMC', 'Av_BV_Emissions_NMC', \
                                                                     'VM_Sea_HN', 'Av_VM_Sea_HN' , 'VM_Land_HN', 'Av_VM_Land_HN', 'VM_Emissions_HN','Av_VM_Emissions_HN',\
                                                                         'VM_Sea_LFP', 'Av_VM_Sea_LFP' , 'VM_Land_LFP', 'Av_VM_Land_LFP', 'VM_Emissions_LFP','Av_VM_Emissions_LFP',\
                                                                             'VM_Sea_NMC', 'Av_VM_Sea_NMC' , 'VM_Land_NMC', 'Av_VM_Land_NMC', 'VM_Emissions_NMC','Av_VM_Emissions_NMC']
                                                                         

sumulation_table.columns = column_headers
csv_Simulation = "SCEV_Sim_V2_Future.csv"
sumulation_table.to_csv(csv_Simulation, index = False)
