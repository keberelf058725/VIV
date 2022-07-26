import pandas
import numpy

Actual_Flash = pandas.read_excel(r"Flash 7.23.2022.xlsx", header=None)
DL_Flash = pandas.read_csv(r"599-flash-automation-do-not-use-Patients-JUL_24_2022_0120.csv")
Actual_Flash['Patient'] = Actual_Flash[0]
Actual_Flash['MRN'] = Actual_Flash[1]
Actual_Flash = Actual_Flash[['Patient','MRN']]
Actual_Flash = Actual_Flash.dropna()
Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('Name')==False]
Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('ON CAMPUS')==False]
Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('OFF CAMPUS')==False]
Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('Residential')==False]
Actual_Flash = Actual_Flash.reset_index()
Actual_Flash = Actual_Flash[['Patient','MRN']]
DL_Flash['LNF3'] = DL_Flash['Last Name'].str.slice(stop=3)
DL_Flash['LNF2'] = DL_Flash['Last Name'].str.slice(stop=2)
DL_Flash['Name_3'] = DL_Flash.loc[:,'First Name'] + ' ' + DL_Flash.loc[:,'LNF3']
DL_Flash['Name_2'] = DL_Flash.loc[:,'First Name'] + ' ' + DL_Flash.loc[:,'LNF2']
DL_Flash['Name'] = DL_Flash.loc[:,'First Name'] + ' ' + DL_Flash.loc[:,'Last Name']
DL_Flash = DL_Flash[['Name', 'MR', 'Sex','Insurance 1   Insurance Company', 'Admission Date','Length Of Stay', 'Program', 'Payment Method','LNF3', 'LNF2', 'Name_3', 'Name_2']]
M_D = pandas.merge(DL_Flash, Actual_Flash, how="left", left_on = ["Name_3"], right_on = ["Patient"], suffixes = ("",".Flash"))
M_D = pandas.merge(M_D, Actual_Flash, how="left", left_on = ["Name_2"], right_on = ["Patient"], suffixes = ("",".Match2"))
M_D = pandas.merge(M_D, Actual_Flash, how="left", left_on = ["MR"], right_on = ["MRN"], suffixes = ("",".MRN_MATCH"))
M_D['Boolean'] = numpy.where((M_D['Patient'].isnull()) & (M_D['Patient.Match2'].isnull()) & (M_D['Patient.MRN_MATCH'].isnull()),True,False)
M_D = M_D[M_D['Boolean'] == True]
M_D = M_D.rename(columns = {'Insurance 1   Insurance Company':'Insurance'})
M_D = M_D[['Name', 'MR', 'Sex', 'Insurance','Admission Date', 'Length Of Stay', 'Program', 'Payment Method']]
