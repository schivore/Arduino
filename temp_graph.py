import pandas as pd,numpy as np
from dateutil.parser import parse


def isfloat(value):
	try:
		float(value)
		return True
	except:
		return False

temp=pd.read_csv(r'temp_log.html',lineterminator='Z',header=None,date_parser=True,infer_datetime_format=True)
#temp.iloc[:,0].apply(lambda x: str(x).replace('\r','').replace('\n',''))
#temp.apply(lambda x: str(x).replace('\r','').replace('\n',''),axis=0)
temp.apply(lambda x: str(x).strip().strip('\r').strip('\n'),axis=0)
temp.dropna(inplace=True)
temp.columns=['date','temperature']
temp['float']=temp['temperature'].apply(lambda x: isfloat(x))
temp=temp.loc[temp['float']]
temp['temperature']=temp['temperature'].apply(lambda x:float(x))
temp=temp.loc[temp['temperature']!=-1]
temp['string']=temp.apply(lambda x: "{date:%s,value:%s},\n" % (parse(x['date'].strip()).strftime("%Y%m%d%H%M"),x['temperature']),axis=1)
print(temp)
date_temp_string=temp['string'].sum()
HTML_source=r'''
<html>
<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.min.js"></script>
	<title>Welcome to The Pi</title>
	<meta name="robots" content="noindex">
</head>
<body>
<div id="myfirstchart" style="height: 250px;"></div>
<script>
new Morris.Line({
element:'myfirstchart',
data:[
%s
],
xkey:'date',
ykeys:['value'],
labels: ['Temperature'],
parseTime: false
});
</script>
</body>
</html>
'''
with open(r"temp_graph.html","w") as text_file:
	text_file.write(HTML_source % date_temp_string)

#print(date_temp_string)
