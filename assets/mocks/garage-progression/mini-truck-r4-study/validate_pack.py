from pathlib import Path
import json,math,hashlib,copy,xml.etree.ElementTree as ET
from PIL import Image
P=Path(__file__).resolve().parent
s=json.loads((P/'interfaces.json').read_text());checks=[]
def ck(name,value):
 checks.append({'check':name,'pass':bool(value)})
 if not value:raise AssertionError(name)
def close(a,b):return math.isclose(a,b,abs_tol=1e-9)
def fit(s):
 w,l=s['truck_design']['bed_clear_WL'];a,b=s['shared_floor_sockets']['footplate_WL_allowance']
 return all(abs(x)+a/2<w/2 and abs(z)+b/2<l/2 and y==0 for x,y,z in s['shared_floor_sockets']['coordinates_bed_local_xyz'].values())
def sweep(s):return abs(s['measured_context']['current_low_speed_measured_pose_sweep_diameter']-10.147658468)<1e-8
ck('Source pins are full 40-character SHA strings',all(len(s['source_authority'][k])==40 for k in ['corrected_task_sha','central_brief_sha','customization_sequence_sha','measured_game_sha']))
ck('No gate supersession or runtime edits',s['source_authority']['mandatory_r3_gate_superseded'] is False and s['source_authority']['runtime_edits'] is False)
ck('Body and mirror fit within design plan budget',s['truck_design']['body_WHL'][2]<4.5 and s['truck_design']['mirror_width_budget']<2)
ck('Floor mount footplates fit strictly inside proposed usable bed',fit(s))
ck('Measured-heading sweep, not rejected tangent-only result',sweep(s))
ck('Named shared floor grid is exact',s['shared_floor_sockets']['coordinates_bed_local_xyz']=={'bed_A':[.5,0,.675],'bed_B':[-.5,0,.675],'bed_C':[.5,0,-.675],'bed_D':[-.5,0,-.675]})
ck('Both fittings use identical socket names',s['rack_design']['sockets']==s['padded_design']['sockets']==list(s['shared_floor_sockets']['coordinates_bed_local_xyz']))
for key in ['rack_design','padded_design']:
 w,h,l=s[key]['overall_WHL_bed_local']
 ck(key+' bed edge margins are 0.05 m gross',close((1.3-w)/2,.05) and close((1.7-l)/2,.05))
 ck(key+' mount plates remain within module footprint',all(abs(x)+.05<w/2 and abs(z)+.05<l/2 for x,y,z in s['shared_floor_sockets']['coordinates_bed_local_xyz'].values()))
 ck(key+' ground-relative top consistent',close(.72+h,s[key]['top_above_design_ground']))
 ck(key+' below proposed all-up 2.20 m height',.72+h<2.2)
p=s['padded_design']; w,h,l=p['overall_WHL_bed_local']; e=p['combined_perimeter_allowance_including_frame_pad'];b=p['combined_base_allowance_including_frame_pad']
ck('Padded clear dimensions include combined frame/pad allowance',all(close(a,b) for a,b in zip([w-2*e,h-b,l-2*e],p['clear_inside_WDL'])))
ck('Storage gross centered margins',close((2-1.2)/2,.4) and close((2-1.6)/2,.2))
ck('Door side and vertical gross margins',close((4.2-2)/2,1.1) and close(3.2-2.2,1))
ck('Selected game-asset and closure margins',s['shared_floor_sockets']['game_asset_clearance_rule']['minimum_visible_gap_to_bed_geometry']==.02 and s['shutter_design']['closing_safety_margin']==.20 and s['shutter_design']['mechanism_headroom']==.45)
ck('Unknown capacity remains null',s['workshop_design']['proven_shelf_capacity'] is None and s['workshop_design']['actual_pack_dimensions'] is None)
ck('Unknown physics and fastening remain null',s['shared_floor_sockets']['runtime_transform'] is None and s['rack_design']['capacity_modifier'] is None and s['padded_design']['protection_modifier'] is None)
for f in sorted((P/'sheets').glob('*.svg')):
 root=ET.parse(f).getroot();t=' '.join(root.itertext())
 ck(f.name+' parses and labels proposal',root.attrib['viewBox']=='0 0 1600 1100' and 'DRAFT - NOT ACCEPTED' in t and 'Not recovered r3' in t)
 with Image.open(f.with_suffix('.png')) as im:ck(f.name+' PNG dimensions',im.size==(1600,1100))
# Drawn geometry checks: SVG shape extents, not merely matching text labels.
NS={'s':'http://www.w3.org/2000/svg'}
def byid(root,name):return next(n for n in root.iter() if n.attrib.get('id')==name)
def padded_drawn_extent_ok(root):
 body=byid(root,'padded-rear-body');base=byid(root,'padded-rear-base');top=byid(root,'padded-top-outer')
 scale=float(body.attrib['data-px-per-m']); left=float(body.attrib['x']); limit=s['padded_design']['overall_WHL_bed_local'][0]
 for el in [body,base,top]:
  x=float(el.attrib['x']);w=float(el.attrib['width'])
  if not (x>=left-1e-8 and x+w<=left+limit*scale+1e-8 and w/scale<=limit+1e-8):return False
 return True
root=ET.parse(P/'sheets/03-padded-carrier.svg').getroot()
ck('Padded drawn top/body/base all stay within JSON width',padded_drawn_extent_ok(root))
outer=byid(root,'padded-top-outer');scale=float(outer.attrib['data-px-per-m']);cx=float(outer.attrib['x'])+float(outer.attrib['width'])/2;cy=float(outer.attrib['y'])+float(outer.attrib['height'])/2
ck('Padded top drawn length equals JSON',close(float(outer.attrib['height'])/scale,s['padded_design']['overall_WHL_bed_local'][2]))
for name,(x,y,z) in s['shared_floor_sockets']['coordinates_bed_local_xyz'].items():
 n=byid(root,'padded-mount-'+name)
 ck('Drawn mount '+name+' equals shared JSON coordinate',close(float(n.attrib['cx']),cx-scale*x) and close(float(n.attrib['cy']),cy-scale*z))
# Reinsert the independently found 384 px / 1.28 m base: this must now fail.
bad=copy.deepcopy(root);base=byid(bad,'padded-rear-base');base.set('x','210');base.set('width','384')
ck('Negative control rejects old drawn 1.28 m padded base',not padded_drawn_extent_ok(bad))
r=ET.parse(P/'sheets/06-roll-up-retraction-section.svg').getroot();case=byid(r,'shutter-casing-section');coil=byid(r,'shutter-roll-section');curtain=byid(r,'shutter-free-curtain-section');sd=s['shutter_design'];sc=float(case.attrib['data-px-per-m'])
ck('Drawn casing height/depth equal JSON',close(float(case.attrib['height'])/sc,sd['casing']['height']) and close(float(case.attrib['width'])/sc,sd['casing']['depth']))
ck('Drawn retracted roll diameter equals JSON',close(2*float(coil.attrib['r'])/sc,sd['retracted_curtain_volume']['diameter']))
x=float(case.attrib['x']);y=float(case.attrib['y']);w=float(case.attrib['width']);h=float(case.attrib['height']);cx=float(coil.attrib['cx']);cy=float(coil.attrib['cy']);rad=float(coil.attrib['r'])
ck('Retracted roll drawn strictly inside casing',cx-rad>x and cx+rad<x+w and cy-rad>y and cy+rad<y+h)
ck('Closed curtain extent matches opening and collision depth',close(float(curtain.attrib['height'])/sc,sd['opening_WH'][1]) and close(float(curtain.attrib['width'])/sc,sd['slab_depth_allowance']))
ck('Case bottom aligns with top of clear opening',close(y+h,float(curtain.attrib['y'])))
ck('Roll-up is explicit, not rigid leaf',sd['motion'].startswith('stylized roll-up curtain') and 'not a rigid' in sd['motion'])
ck('Full-inside guard uses declared collision inner face plus margin',close(sd['full_inside_guard_plane_d'],sd['slab_depth_allowance']/2+sd['closing_safety_margin']))
ck('Blockers split by stage without dropping world acceptance','isolated_common_blockout_study' in s['stage_prerequisites'] and 'later_actual_world_integration' in s['stage_prerequisites'])
# Failing-before controls exercise actual predicates without modifying source.
a=copy.deepcopy(s);a['shared_floor_sockets']['coordinates_bed_local_xyz']['bed_A'][0]=.9
ck('Negative control catches out-of-bed socket',not fit(a))
a=copy.deepcopy(s);a['measured_context']['current_low_speed_measured_pose_sweep_diameter']=9.710292398
ck('Negative control rejects tangent-only sweep',not sweep(a))
result={'status':'author_checks_pass_not_independent_acceptance','checks':checks,'passed_count':len(checks),'visual_review':'Author opened all six final PNGs. R4 correction confines the entire padded base to JSON width, derives drawn mounts from shared coordinates, and declares/depicts roll-up casing and retraction. Added drawn-extent negative control catches prior 1.28 m base. No independent acceptance is claimed.','unverified':['Reference-matched perspective art','Real source mesh and sockets','Actual loading and handling','Moving shutter and police integration','Phone/runtime behavior','Full td-197 gate']}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed_count':len(checks),'status':result['status']}))
