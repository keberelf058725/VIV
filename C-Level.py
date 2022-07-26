import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
#inclusive
Month_Start = pd.to_datetime(input())
#exclusive
Month_End = pd.to_datetime(input())
#Read LOS file
ALOS = pd.read_csv(r"***")
#Read DC File
DC = pd.read_csv(r"****")
#Change DC Date to Date/Time
DC.loc[:, ('Discharge Date')] = pd.to_datetime(DC.loc[:,('Discharge Date')])
#Filter Rows to April DCs
DC2 = DC[(DC['Discharge Date'] >= Month_Start) & (DC['Discharge Date'] < Month_End)]
#Replace ADMIN DC TYPES
DC2['Discharge Type'] = DC2['Discharge Type'].replace(['ADMINISTRATIVE – NO SHOW',"ADMINISTRATIVE – BEHAVIORAL " ,'ADMINISTRATIVE – LEGAL'],'ADMIN DC')
#REPLACE DETOX/STAB ONLY TYPES
DC2['Discharge Type'] = DC2['Discharge Type'].replace(['DETOX COMPLETE','STABILIZATION ONLY'],'DETOX/STAB ONLY')
#DROP ALL PRE-ADMISSION RECORDS
DC3 = DC2[DC2['Discharge Type'].str.contains('PRE-ADMISSION')==False]
#Grab only needed Columns
ALOS1 = ALOS[['MR#', 'Admission Date', 'Discharge Date','Detox Actual', 'Residential Actual','PHP/Day-Night Actual','IOP Actual', 'IIP Actual','PHP/Day-Night Treatment with Community Housing Actual','Length of Stay']]
#drop rows with null values
ALOS2 = ALOS1.dropna()
#Change DC Date to Date/Time
ALOS2.loc[:, ('Discharge Date')] = pd.to_datetime(ALOS2['Discharge Date'])
#Verify D/T
#ALOS2.info()
#Filter Rows to April DCs
ALOS3 = ALOS2[(ALOS2['Discharge Date'] >= Month_Start) & (ALOS2['Discharge Date'] < Month_End)]
ALOS4 = ALOS3.rename(columns = {'Length of Stay': 'UR LOS' })
#Merge Both Files
MRG = pd.merge(DC3, ALOS4, how="left", left_on = ["MR"], right_on = ["MR#"], suffixes = ("",".ALOS"))
#Create STAGE 1 LOS
MRG['Stage 1 LOS'] = MRG.loc[:,['Detox Actual', 'Residential Actual','IIP Actual']].sum(axis=1)
#SUM PHP COLUMNS
MRG['PHP Actual'] = MRG.loc[:,['PHP/Day-Night Actual', 'PHP/Day-Night Treatment with Community Housing Actual']].sum(axis=1)
#CREATE STAGE 2 COLUMNS
MRG['Stage 2 LOS'] = MRG.loc[:,['PHP Actual', 'IOP Actual']].sum(axis=1)
#CREATE TOTAL LOS COLUMN
MRG['TOTAL LOS'] = MRG.loc[:,['Stage 1 LOS','Stage 2 LOS']].sum(axis=1)
MRG['Stage 2 Conversion'] = np.where(MRG['Stage 2 LOS'] > 0, 'Converted', 'Unconverted')
MRG['PHP Conversion'] = np.where(MRG['PHP Actual'] > 0, 'Converted', 'Unconverted')
MRG['IOP Conversion'] = np.where(MRG['IOP Actual'] > 0, 'Converted', 'Unconverted')
MRG['Stage 1 to PHP Conversion'] = np.where((MRG['Stage 1 LOS'] > 0) & (MRG['PHP Actual'] > 0), 'Converted', 'Unconverted')
MRG['HELPER'] = MRG.loc[:,['Stage 1 LOS','PHP Actual']].sum(axis=1)
MRG['Stage 1 to IOP Conversion'] = np.where((MRG['IOP Actual'] > 0) & (MRG['HELPER'] > 0), 'Converted', 'Unconverted')
MRG['PHP into IOP Conversion'] = np.where((MRG['IOP Actual'] > 0) & (MRG['PHP Actual'] > 0), 'Converted', 'Unconverted')
MRG[['Statuses_1','Statuses_2']]=MRG.Statuses.str.split(';',n=1,expand=True)
MRG['Stage_1_Therapist'] = np.where(MRG.loc[:, ('Statuses_2')].str.contains("Campus Therapist"), MRG.loc[:, ('Statuses_2')], MRG.loc[:,('Statuses_1')])
MRG[['Stage_1_Therapist_1','Stage_1_Therapist_2']]=MRG.Stage_1_Therapist.str.split(': ',n=1,expand=True)
MRG[['Stage_1','Stage_1_Therapist_4']]=MRG.Stage_1_Therapist_2.str.split(',',n=1,expand=True)
MRG[['Stage_2','Stage_2_Eronious']]=MRG['Primary Therapist'].str.split(',',n=1,expand=True)
MRG['DCDATE_COPY'] = MRG['Discharge Date'].astype(str)
MRG[['DCYEAR','DCM', 'DCD']] = MRG.DCDATE_COPY.str.split('-',expand=True)
MRG['DCYT'] = MRG['DCYEAR'].str.slice(start=2)
MRG['DC_Month'] = MRG.loc[:,('DCM')].astype(str) + MRG.loc[:,('DCYT')].astype(str)
MRG['Admit_Yr'] = MRG.loc[:, ('DCYEAR')]
MRG['Admit_Yr_Filter'] = MRG.loc[:, ('DCYEAR')]
MRG['RELAPSE'] = np.where((MRG['PHP Actual'] > 0) & ((MRG['Program'].str.contains("4 - Residential")) | (MRG['Program'].str.contains("4 - Residential"))), "True", "False")
MRG['Include_on_Campus1'] = np.where(MRG['Stage 2 Conversion'].str.contains("Unconverted"), "Y","N")
MRG['Include_on_Campus'] = np.where(MRG['RELAPSE'].str.contains("True"), "Y", MRG.loc[:,('Include_on_Campus1')])
MRG1 = MRG[['First Name', 'Last Name', 'MR', 'Insurance 1   Insurance Company','Discharge Type', 'Admission Date', 'Discharge Date','DC_Month', 'Length Of Stay','Detox Actual','IIP Actual', 'Residential Actual','Stage 1 LOS','PHP Actual', 'IOP Actual','Stage 2 LOS','TOTAL LOS','Stage 2 Conversion','PHP Conversion','IOP Conversion', 'Stage 1 to PHP Conversion','Stage 1 to IOP Conversion','PHP into IOP Conversion','UR LOS','Stage_1','Stage_2', 'Program','Payment Method','Admit_Yr','Admit_Yr_Filter', 'RELAPSE', 'Include_on_Campus']]
TR = pd.read_excel(r"Current Therapist List.xlsx")
MRG2 = pd.merge(MRG1, TR, how="left", left_on = ["Stage_1"], right_on = ["Full Name"], suffixes = ("","_TR"))
MRG3 = pd.merge(MRG2, TR, how="left", left_on = ["Stage_2"], right_on = ["Full Name"], suffixes = ("","_TR"))
MRG3.rename(columns = {'Therapist':'S1 Therapist','Therapist_TR':'S2 Therapist'}, inplace = True)
MRG3[['S1 Therapist', 'S2 Therapist']] = MRG3[['S1 Therapist', 'S2 Therapist']].fillna('Former Employee')
Final_Preped_Data = MRG3[['First Name', 'Last Name', 'MR', 'Insurance 1   Insurance Company','Discharge Type', 'Admission Date', 'Discharge Date', 'DC_Month','Length Of Stay', 'Detox Actual', 'IIP Actual', 'Residential Actual','Stage 1 LOS', 'PHP Actual', 'IOP Actual', 'Stage 2 LOS', 'TOTAL LOS','Stage 2 Conversion', 'PHP Conversion', 'IOP Conversion','Stage 1 to PHP Conversion', 'Stage 1 to IOP Conversion','PHP into IOP Conversion', 'UR LOS', 'S1 Therapist', 'S2 Therapist', 'Program','Payment Method', 'Admit_Yr', 'Admit_Yr_Filter', 'RELAPSE','Include_on_Campus']]
#Final_Preped_Data.to_csv(r"***", index = False)
Final_Preped_Data
