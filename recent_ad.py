import pandas
from datetime import datetime, timedelta
import numpy
t = datetime.today() - timedelta(days=3)
df = pandas.read_csv(r'census_info_beachhouse.csv')
df[['Therapist','trash']] = df.primarycareteam_primarytherapist.str.split(' ',n=1,expand=True)
df[['DOC','trash.1']] = df.diagcodename_list.str.split(' ',n=1,expand=True)
df['LNF3'] = df['last_name'].str.slice(stop=3)
df['Name'] = df.loc[:,'first_name'] + ' ' + df.loc[:,'LNF3']
df = df[['Name', 'mr', 'admission_date', 'program_name', 'length_of_stay','age','sex','DOC','Therapist','paymentmethod']]
df['Therapist'] = df['Therapist'].replace(['Did'],'No Assigned Therapist')
df['admission_date_1'] = df['admission_date']
df.loc[:, ('admission_date_1')] = pandas.to_datetime(df.loc[:,('admission_date_1')])
new_admissions = df[(df['admission_date_1'] >= t)].sort_values(by='admission_date_1',ascending=False)
new_admissions[['admission_date','trash.2']] = df.admission_date.str.split(' ',n=1,expand=True)
new_admissions[['Y', 'M','D']] = new_admissions.admission_date.str.split('-', n=2, expand=True)
new_admissions['admission_date'] = new_admissions.loc[:,('M')] + "-" + new_admissions.loc[:,('D')] + "-" + new_admissions.loc[:,('Y')]
new_admissions = new_admissions[['Name', 'mr', 'admission_date', 'program_name', 'length_of_stay','age','sex','DOC','Therapist','paymentmethod']]
#df_graphs = df
