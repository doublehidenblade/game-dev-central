from pathlib import Path
from xml.sax.saxutils import escape
import json, hashlib, subprocess
P=Path(__file__).resolve().parent
O=P/'sheets'; O.mkdir(exist_ok=True)
SPEC=json.loads((P/'interfaces.json').read_text())
C={'bg':'#f4f0e5','ink':'#28343a','muted':'#606b70','line':'#bfc5c1','D':'#aa6324','Df':'#f1dec1','M':'#236675','Mf':'#d9e9e8','U':'#9b4440','Uf':'#f1dcda','green':'#64785e','pad':'#819188','steel':'#78878b','white':'#fffdf8'}
def tx(x,y,s,size=22,fill='ink',weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}" fill="{C.get(fill,fill)}" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill='white',stroke='ink',sw=2,rx=0,dash=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def line(x1,y1,x2,y2,color='ink',w=3,dash=None):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C.get(color,color)}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def circ(x,y,r,fill='D',stroke='ink',sw=2):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" stroke-width="{sw}"/>'
def dim(x1,y1,x2,y2,label,vertical=False):
 a=line(x1,y1,x2,y2,'D',2)
 if vertical:
  a+=line(x1-7,y1,x1+7,y1,'D',2)+line(x2-7,y2,x2+7,y2,'D',2)
  a+=tx(x1+15,(y1+y2)/2,label,20,'D')
 else:
  a+=line(x1,y1-7,x1,y1+7,'D',2)+line(x2,y2-7,x2,y2+7,'D',2)
  a+=tx((x1+x2)/2,y1-13,label,20,'D',500,'middle')
 return a
def para(x,y,lines,size=21,color='ink',gap=31):
 return ''.join(tx(x,y+i*gap,v,size,color) for i,v in enumerate(lines))
def panel(x,y,w,h,title):return rect(x,y,w,h,'white','line',1.5,12)+tx(x+24,y+39,title,23,'ink',700)
def head(n,title,sub):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100">'+rect(0,0,1600,1100,'bg','bg',0)+tx(48,50,'GARAGE MVP / INTERFACE PROPOSAL',19,'muted',700)+tx(48,99,title,38,'ink',700)+tx(48,138,sub,21,'muted')+rect(1260,30,292,48,'Df','D',1.5,6)+tx(1406,61,'DRAFT - NOT ACCEPTED',17,'D',700,'middle')+line(48,158,1552,158,'line',2)+tx(48,1060,'D = chosen design target   |   M = measured current-game fact   |   U = unresolved',20,'muted')+tx(48,1090,'2D schematic only. Not recovered r3 art, CAD, an engine capture or a runtime acceptance.',17,'muted')+tx(1546,1085,f'{n:02d} / 06',18,'muted',500,'end')
def save(n,name,s):
 (O/f'{n:02d}-{name}.svg').write_text(s+'</svg>')
 subprocess.run(['inkscape',str(O/f'{n:02d}-{name}.svg'),'--export-type=png','--export-filename='+str(O/f'{n:02d}-{name}.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

# 1: plan in a chosen design coordinate frame, 200 pixels/metre.
s=head(1,'One bed, one floor-mount contract','D option A: compact work-truck proportions; every dimension here is a proposal, not a measured asset')
s+=panel(48,184,756,822,'TOP PLAN / +Z FORWARD / +X LEFT')+panel(830,184,722,822,'PROPOSED INTERFACES AND OPEN QUESTIONS')
s+='<g transform="translate(48 140) scale(0.82)">'
def px(x):return 380-200*x
def py(z):return 510-200*z
s+=rect(px(.75),py(1.70),300,680,'Df','D',3,12)
s+=rect(px(.75),py(1.70),300,300,'white','ink',3,18)
s+=rect(px(.57),py(1.46),228,150,'Mf','ink',2,8)
s+=tx(380,450,'CAB',25,'ink',700,'middle')
s+=rect(px(.65),py(.10),260,340,'bg','ink',3)
s+=tx(380,658,'BED',24,'muted',700,'middle')
s+=rect(px(.86),py(1.05),26,38,'steel')+rect(px(-.73),py(1.05),26,38,'steel')
s+=rect(px(.75),py(-1.60),300,90,'Uf','U',2,0,'8 6')
s+=tx(380,908,'TAILGATE RESERVE',18,'U',700,'middle')
for k,x,z in [('A',.50,-.075),('B',-.50,-.075),('C',.50,-1.425),('D',-.50,-1.425)]:
 s+=rect(px(x)-10,py(z)-10,20,20,'D','ink',2)+circ(px(x),py(z),4,'white')+tx(px(x)+18,py(z)+7,k,23,'D',700)
s+=line(px(.50),py(-.075),px(-.50),py(-.075),'D',2,'6 4')+line(px(.50),py(-1.425),px(-.50),py(-1.425),'D',2,'6 4')
s+=dim(120,170,120,850,'3.40 m',True)+dim(px(.75),952,px(-.75),952,'1.50 m body')
s+=tx(80,980,'Schematic metric plan; no tire or light geometry implied',18,'muted')
s+='</g>'
s+=para(858,267,['Body L 3.40 m / W 1.50 m / H 1.85 m','Mirror envelope W 1.72 m (chosen budget)','Bed clear W 1.30 m × L 1.70 m','Bed-floor height 0.72 m above design ground'],22,'D')
s+=tx(858,423,'D: one shared bed-local coordinate frame',23,'ink',700)
s+=para(858,463,['Origin: center of usable bed floor','Axes: +X left, +Y up, +Z cab/front','A (+0.500, 0, +0.675) m  front-left','B (−0.500, 0, +0.675) m  front-right','C (+0.500, 0, −0.675) m  rear-left','D (−0.500, 0, −0.675) m  rear-right'],21,'D')
s+=para(858,675,['D: 0.10 × 0.10 m footplate allowance','Socket centers are 0.15 m from bed sides','and 0.175 m from each bed end.','Both modules contact the bed FLOOR.','Drop-side rail tops are not supports.'],21)
s+=para(858,853,['U: actual root transform, brackets, fasteners,','wheel/light envelopes, collider and payload.','No-build targets and formulas: interfaces.json','Owner must measure the selected 3D blockout.'],21,'U')
s+=tx(858,979,'The four floor mounts are a new option, not recovered r3 coordinates.',17,'U')
save(1,'shared-bed-sockets',s)

# 2: floor-mounted rack
s=head(2,'Utility rack / one removable fitting','Open skeletal frame; preserve the cab-back window, bed visibility, lamps and tailgate access')
s+=panel(48,184,920,822,'D: SEPARATE VIEWS OF THE SAME PROPOSED RACK')+panel(994,184,558,822,'FIT AND CAPABILITY CONTRACT')
# rear elevation 300px/m, rack top at340 floor700
s+=tx(110,290,'REAR ELEVATION',20,'muted',700)
s+=rect(180,340,360,12,'steel')+rect(204,340,12,360,'steel')+rect(504,340,12,360,'steel')
s+=rect(195,685,30,15,'D')+rect(495,685,30,15,'D')
s+=line(155,700,566,700,'ink',4)+tx(170,735,'BED FLOOR / +0.72 m',19,'D')
s+=rect(248,410,224,236,'Mf','M',1,0,'6 5')+tx(360,495,'OPEN',28,'M',700,'middle')+tx(360,530,'NEGATIVE SPACE',17,'M',700,'middle')
s+=dim(180,320,540,320,'1.20 m overall')+dim(589,340,589,700,'1.20 m',True)
s+=tx(90,797,'TOP PLAN / floor feet A–D',20,'muted',700)
s+=rect(260,815,120,160,'bg','steel',4)
for k,x,y in [('A',270,827.5),('B',370,827.5),('C',270,962.5),('D',370,962.5)]:s+=rect(x-5,y-5,10,10,'D')+tx(x+(12 if x<300 else -25),y+7,k,16,'D',700)
s+=tx(430,865,'W 1.20 × L 1.60 m',21,'D')+tx(430,901,'Cab/front is at top',18)+tx(430,935,'Same floor feet A–D',18)
s+=para(1020,271,['D: outer W 1.20 × L 1.60 m','D: H 1.20 m above bed floor','D: total top = 1.92 m','D: nominal frame members 0.04 m','D: shared A/B/C/D floor mounts'],21,'D')
s+=tx(1020,455,'READABLE AT CHASE DISTANCE',20,'ink',700)
s+=para(1020,497,['Two hoops, broad flat paint,','few chunky connection plates.','No tiny bolt texture requirement.','Cream/ochre steel; muted dark trim.','No copied badge or real branding.'],20)
s+=tx(1020,680,'MVP RULES',21,'ink',700)
s+=para(1020,723,['Only one equipped fitting.','Do not add over-cab arms or cargo','overhang to make the drawing fit.','No capacity or stat bonus is set here.','Mass, cargo volume, legal load and','bracket fit remain U.'],20)
s+=para(1020,926,['U: rear access, drop-side operation,','loaded envelope and real service fit.'],20,'U')
save(2,'utility-rack',s)

#3 padded
s=head(3,'Padded carrier / distinct low silhouette','One floor-mounted cassette, using the same four mounts as the rack; no second chassis or socket grid')
s+=panel(48,184,920,822,'D: TOP PLAN AND REAR ELEVATION')+panel(994,184,558,822,'FIT AND CAPABILITY CONTRACT')
s+=tx(98,253,'TOP PLAN / CAB AT TOP',20,'muted',700)
# Draw all padded extents and mount locations directly from the same JSON interface.
pad=SPEC['padded_design']; pw,ph,pl=pad['overall_WHL_bed_local']; pe=pad['combined_perimeter_allowance_including_frame_pad']
ps=300.0; pleft=222.0; ptop=310.0; pcx=pleft+pw*ps/2; pcy=ptop+pl*ps/2
s+=rect(pleft,ptop,pw*ps,pl*ps,'steel','ink',3).replace('<rect ','<rect id="padded-top-outer" data-px-per-m="300" ')
s+=rect(pleft+pe*ps,ptop+pe*ps,(pw-2*pe)*ps,(pl-2*pe)*ps,'Df','ink',2)
s+=rect(pleft,ptop,pw*ps,pe*ps,'pad')+rect(pleft,ptop,pe*ps,pl*ps,'pad')+rect(pleft+(pw-pe)*ps,ptop,pe*ps,pl*ps,'pad')+rect(pleft,ptop+(pl-pe)*ps,pw*ps,pe*ps,'pad')
s+=tx(pcx,536,'PADDED WELL',24,'ink',700,'middle')+tx(pcx,574,'1.08 × 1.48 m',24,'D',700,'middle')
for key,(x,y,z) in SPEC['shared_floor_sockets']['coordinates_bed_local_xyz'].items():
 s+=circ(pcx-ps*x,pcy-ps*z,8,'D').replace('<circle ',f'<circle id="padded-mount-{key}" ')
s+=dim(pleft,297,pleft+pw*ps,297,'1.20 m overall')+dim(635,ptop,635,ptop+pl*ps,'1.60 m',True)
s+=tx(100,824,'REAR ELEVATION',20,'muted',700)
s+=rect(pleft,841,pw*ps,ph*ps,'pad','ink',3).replace('<rect ','<rect id="padded-rear-body" data-px-per-m="300" ')
s+=rect(pleft,966,pw*ps,10,'steel').replace('<rect ','<rect id="padded-rear-base" data-px-per-m="300" ')
s+=tx(635,922,'H = 0.45 m',21,'D')+tx(635,958,'Top = 1.17 m',21,'D')
s+=para(1020,270,['D: outer W 1.20 × L 1.60 m','D: H 0.45 m above bed floor','D: total top = 1.17 m','D: edge allowance incl. pad 0.06 m','D: base allowance incl. pad 0.06 m'],21,'D')
s+=para(1020,460,['D: clear inside W 1.08 × L 1.48 m','D: depth above pad = 0.39 m','These are geometry targets only.','They do not establish cargo units','or a protection modifier.'],20,'D')
s+=tx(1020,655,'DISTINCT FROM THE RACK',20,'ink',700)
s+=para(1020,696,['Low olive/canvas pads, broad seams,','dark straps and a simple steel base.','No refrigeration, springs or free-','swinging cargo simulation implied.','Visible soft sides versus open rack.'],20)
s+=para(1020,883,['U: rear access/lip detail, mass, cargo','shape compatibility, protection value','and actual loading animation.'],20,'U')
save(3,'padded-carrier',s)

#4workshop uses inherited proposed positions only; 53px/m
s=head(4,'Roomy workshop / fixed service positions','Retain the existing provisional 12 × 10 m room. No actual site is reserved and no interior exists yet')
s+=panel(48,184,936,822,'D: ROOM-LOCAL PLAN / ALL RESERVATIONS PROVISIONAL')+panel(1010,184,542,822,'MVP EQUIPMENT AND STORAGE')
# depth u east left-to-right, v north bottom-to-top; room 10x12
ox,oy,sc=158,935,53
q=lambda u,v:(ox+u*sc,oy-v*sc)
s+=rect(ox,oy-12*sc,10*sc,12*sc,'bg','ink',5)
# entrance left centered v6
s+=line(ox,oy-8.1*sc,ox,oy-3.9*sc,'bg',9)
s+=line(ox-9,oy-8.1*sc,ox-9,oy-3.9*sc,'D',5)
def rz(u,v,w,h,fill,label,fs=16):
 x,y=q(u,v+h);return rect(x,y,w*sc,h*sc,fill,'ink',2)+tx(x+w*sc/2,y+h*sc/2+6,label,fs,'ink',600,'middle')
s+=rz(1,4.4,6.5,3.2,'Df','PARK / UNLOAD',20)
s+=rz(.5,.5,3,.8,'steel','BENCH',17)+rz(7.5,.5,2,2,'Mf','SUPPLIES',16)
s+=rz(7.5,9.5,2,2,'Mf','MODULE',16)+rz(.5,10,3,1.5,'white','RIG RESERVE',16)
s+=rz(2,5,4.5,2,'white','CLEARANCE BUDGET',15)
s+=tx(160,275,'Rear/deeper interior →',20,'muted')
s+=tx(98,600,'IN',18,'D',700)+line(95,623,158,623,'D',4)
s+=dim(158,969,688,969,'10.00 m room depth')+dim(723,299,723,935,'12.00 m',True)
s+=tx(60,991,'1.90 m between park rectangle and the supply/module reservations (D-derived)',17,'muted')
s+=para(1036,273,['D: bench footprint 3.00 × 0.80 m','D: bench height 0.90 m','D: shelf asset 1.60 × 0.60 × 1.90 m','D: supply zone 2.00 × 2.00 m','D: stored-module zone 2.00 × 2.00 m'],20,'D')
s+=para(1036,465,['One unequipped fitting at a time','fits the proposed 1.20 × 1.60 m','bounding box with 0.40 / 0.20 m','gross centered floor margins.','D: fixed-slot swap / presentation cut.'],20)
s+=tx(1036,660,'12 UNITS: UNPROVEN CAPACITY',19,'U',700)
s+=para(1036,701,['The brief requests an initial 12-unit','shelf. Actual pack sizes are U.','Do not turn this empty reservation','into a measured capacity claim.','No 24-unit or second-bay capacity.'],20)
s+=para(1036,892,['U: real pack packing, access aisle,','service-view readability, moving','parts and obstruction clearance.'],20,'U')
save(4,'workshop-reservations',s)

#5 shutter state diagrams
s=head(5,'Shutter and threshold / state reference','Stylized roll-up curtain; its retracted volume is shown on sheet 06. No automatic exposure on menu close')
s+=panel(48,184,1504,388,'D: THE SAME OPENING IN THREE STATES')
for i,(title,bottom,status) in enumerate([('OPEN',314,'No shelter claim'),('CLOSING',423,'Obstructed → stop/reopen'),('CLOSED',523,'Shelter only after all checks')]):
 x=115+i*485
 s+=tx(x,276,title,22,'ink',700)+rect(x,302,350,221,'bg','ink',5)+rect(x,302,350,bottom-302,'steel','ink',2)
 for y in range(316,bottom,14):s+=line(x+4,y,x+346,y,'muted',1)
 if i<2:s+=rect(x+65,472,220,52,'Df','D',2)+tx(x+175,507,'VEHICLE / LOAD',15,'D',700,'middle')
 else:s+=tx(x+175,458,'VEHICLE FULLY INSIDE',16,'white',700,'middle')+tx(x+175,487,'OCCLUDED BY DOOR',15,'white',500,'middle')
 if i==1:s+=line(x+175,435,x+175,464,'U',5)+tx(x+366,453,'!',30,'U',700)
 s+=tx(x+175,551,status,17,'U',500,'middle')
s+=panel(48,596,714,410,'D: CLEARANCE TARGETS')+panel(788,596,764,410,'M / U: WHAT THIS DOES NOT PROVE')
s+=para(76,680,['Opening 4.20 W × 3.20 H m','Curtain collision allowance 0.22 m deep','Complete vehicle + fitting + cargo budget:','2.00 W × 4.50 L × 2.20 H m','D-derived square-entry margin: 1.10 m / side','D-derived height margin: 1.00 m','D: full-inside margin 0.20 m; mechanism 0.45 m'],22,'D')
s+=para(816,680,['M: current coupe has a 2.00 × 4.50 m plan union.','M: low-speed measured-pose sweep = 10.1477 m.','A 10 m-deep room is not a proven U-turn space.','M: lot 4472 still has a solid collision wall.','U: loaded future-truck sweep and transient entry.','U: closure detection against the chosen margin,','police sight/occlusion, fast drive-past and reload.'],21)
s+=tx(816,945,'These illustrations specify intended states, not implemented behavior.',17,'U')
save(5,'shutter-threshold-states',s)

# 6: metric shutter side section from the declared JSON casing/roll.
s=head(6,'Roll-up curtain / retraction section','D: a stylized flexible curtain winds inside a fixed casing; no full-height rigid leaf travels above the opening')
s+=panel(48,184,860,822,'SIDE SECTION / +d INSIDE / ALL SHUTTER GEOMETRY D')+panel(934,184,618,822,'SIMPLE GAME-ASSET MOTION CONTRACT')
ss=150.0; dx=lambda d:365+ss*d; hy=lambda h:925-ss*h
case=SPEC['shutter_design']['casing']; c0=case['min_dh']; c1=case['max_dh']; roll=SPEC['shutter_design']['retracted_curtain_volume']; rc=roll['section_center_dh']; rr=roll['diameter']/2
s+=line(112,hy(0),842,hy(0),'ink',4)+tx(114,hy(0)+29,'FLOOR h = 0',18,'muted')
s+=line(112,hy(4.3),842,hy(4.3),'M',3,'9 6')+tx(114,hy(4.3)-15,'M: nominal soffit h = 4.30 m',20,'M')
s+=rect(dx(c0[0]),hy(c1[1]),(c1[0]-c0[0])*ss,(c1[1]-c0[1])*ss,'Df','D',3).replace('<rect ','<rect id="shutter-casing-section" data-px-per-m="150" ')
s+=circ(dx(rc[0]),hy(rc[1]),rr*ss,'steel','ink',2).replace('<circle ','<circle id="shutter-roll-section" data-px-per-m="150" ')
s+=circ(dx(rc[0]),hy(rc[1]),rr*ss*.55,'Df','ink',1)
s+=rect(dx(-.11),hy(3.2),.22*ss,3.2*ss,'none','D',2,0,'8 6').replace('<rect ','<rect id="shutter-free-curtain-section" data-px-per-m="150" ')
s+=line(dx(0),hy(0),dx(0),hy(3.2),'steel',5)
s+=line(dx(.31),hy(0),dx(.31),hy(2.2),'U',3,'8 6')
s+=line(dx(.31),hy(1.1),dx(2.2),hy(1.1),'U',3)+tx(dx(.48),hy(1.1)-16,'Full vehicle/load stays deeper →',17,'U')
s+=tx(443,hy(2.65),'D: nearest union point d ≥ +0.31 m',18,'D')
s+=tx(443,hy(2.42),'0.20 m behind inner face d = +0.11',17,'muted')
s+=dim(197,hy(3.2),197,hy(0),'3.20 m',True)
s+=dim(770,hy(3.65),770,hy(3.2),'0.45 m',True)
s+=line(dx(.35),hy(3.65),765,hy(3.65),'D',1)+line(dx(.35),hy(3.2),765,hy(3.2),'D',1)
s+=dim(dx(-.15),hy(3.65)-26,dx(.35),hy(3.65)-26,'0.50 m depth')
s+=tx(443,hy(4.07),'0.65 m nominal remainder before roof/lights',17,'M')
s+=tx(448,hy(3.39),'0.40 m roll diameter',18,'D')
s+=tx(112,978,'Dashed curtain box: CLOSED extent. OPEN: no curtain below h = 3.20 m.',17,'muted')
s+=para(960,270,['D: casing W 4.40 × D 0.50 × H 0.45 m','D: opening W 4.20 × H 3.20 m','D: roll diameter 0.40 m / width 4.20 m','D: curtain guard thickness 0.22 m'],20,'D')
s+=tx(960,439,'CLOSED / MOVING',21,'ink',700)
s+=para(960,480,['Visual lower edge, collision and sight','occlusion follow the same unrolled extent.','The roll/casing is a simple stylized asset.','No individual slat or spring simulation.'],20)
s+=tx(960,644,'FULLY OPEN',21,'ink',700)
s+=para(960,685,['No free-curtain collision or occluder','remains below the 3.20 m clear opening.','The roll is contained inside the casing.','Static casing collision stays overhead.'],20)
s+=para(960,885,['U: actual roof/light fit, obstruction logic,','crossing checks and police integration.','This section specifies geometry, not tests.'],20,'U')
save(6,'roll-up-retraction-section',s)

print('Generated six original SVG sheets and PNG renders')
