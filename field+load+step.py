import math
model_name = 'Model-1'
set_name='Weld-1.Weld-Solu'
L_handao_mm = 100.0#mm
L_handao_m = L_handao_mm/1000#m
L_QG_mm = 0.0#mm
L_QG_m = L_QG_mm/1000#m
Roller_R = 36.0E-3
v_mm_min=187.0#mm/min
v_m_s=v_mm_min/1000/60
v_vr = v_m_s/Roller_R
time_Cold = 300
time_step=0.4
time_step_cold = 5
step_num_heat = int(math.ceil(L_handao_m/v_m_s/time_step))
step_num_Rolled = int(math.ceil((L_handao_m+L_QG_m)/v_m_s/time_step))
step_num_cold = int(math.ceil(time_Cold/time_step_cold))
step_num_all = step_num_Rolled+step_num_cold
reyuan_a=0.002
reyuan_b=0.0110
reyuan_c=0.0015
U=13
I=178
pi=3.14159
Q=U*I*0.7
xtemp=round(math.sqrt(3)*6*Q/reyuan_a/reyuan_b/reyuan_c/pi/(math.sqrt(pi)),1)
substitution = xtemp
##Step
mdb.models[model_name].TempDisplacementDynamicsStep(name='Step-1',
	previous='Initial', timePeriod=time_step, massScaling=((SEMI_AUTOMATIC,
	MODEL, AT_BEGINNING, 800000.0, 0.0, None, 0, 0, 0.0, 0.0, 0, None), ))
step_sum = 0
#heat and rolled
for num in range(0,step_num_Rolled):
	step_sum+=1
	step_pre = "Step-%d" %(step_sum)
	step_now = "Step-%d" %(step_sum+1)
	mdb.models[model_name].TempDisplacementDynamicsStep(name=step_now,previous=step_pre, timePeriod=time_step)


for num in range(0,step_num_cold):
    step_sum+=1
    step_pre = "Step-%d" %(step_sum)
    step_now = "Step-%d" %(step_sum+1)
    mdb.models[model_name].TempDisplacementDynamicsStep(name=step_now,previous=step_pre, timePeriod=time_step_cold)

##Field

coordinate_num = 43
a = mdb.models[model_name].rootAssembly
#a.DatumCsysByThreePoints(name='Datum csys_Field', coordSysType=CARTESIAN, origin=(0.0, 1.4E-3, 25E-3), point1=(0.0, 1.4E-3, 50E-3), point2=(0.0, 5E-3, 25E-3))
datum = mdb.models[model_name].rootAssembly.datums[coordinate_num]
X_increment = 0
Y_increment = 0
Z_increment = 0
for num in range(0,step_num_heat):
	ExpressionField_name = "AnalyticalField-%d" %(num+1)
	pos =round( v_m_s*time_step*num,6)
	X_increment = pos
	expression_for = 'exp(-3*(Y-(%f))**2/%f**2)*exp(-3*(Z-(%f))**2/%f**2)*exp(-3*(X-(%f))**2/%f**2)'%(Y_increment,reyuan_b,Z_increment,reyuan_c,X_increment,reyuan_a)
	mdb.models[model_name].ExpressionField(name=ExpressionField_name,localCsys=datum,expression=expression_for)

##Load
region = mdb.models[model_name].rootAssembly.sets[set_name]
for num in range(0,step_num_heat):
	Load_name = "Load-%d" %(num+1)
	Step_firname = "Step-%d" %(num+1)
	Step_secname = "Step-%d" %(num+2)
	ExpressionField_name = "AnalyticalField-%d" %(num+1)
	mdb.models[model_name].BodyHeatFlux(name=Load_name, createStepName=Step_firname,
	region=region, magnitude=substitution, distributionType=FIELD,
	field=ExpressionField_name)
	mdb.models[model_name].loads[Load_name].deactivate(Step_secname)


	