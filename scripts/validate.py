from pathlib import Path
import re,json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
EXPECTED='1.9.1'
errors=[]
required=['SKILL.md','README.md','PRD.md','CHANGELOG.md','CONTRIBUTING.md','QUALITY-GATES.md','VERSION','manifest.json','RELEASE-MANIFEST.json','references/output-schema.md','templates/deep-debug.md','evals/schema.json','scripts/run_spec_eval.py']
for f in required:
    if not (ROOT/f).is_file(): errors.append('missing '+f)
sk= (ROOT/'SKILL.md').read_text(encoding='utf-8')
for q in ['Non-negotiable rendering contract','Primary Module:','Related Modules:','Decision Link:','Provenance:','Verification:','Human / machine finding parity: PASS / FAIL / NOT APPLICABLE']:
    if q not in sk: errors.append('SKILL missing '+q)
if (ROOT/'VERSION').read_text().strip()!=EXPECTED: errors.append('VERSION mismatch')
m=json.loads((ROOT/'manifest.json').read_text());
if m.get('version')!=EXPECTED: errors.append('manifest version mismatch')
rm=json.loads((ROOT/'RELEASE-MANIFEST.json').read_text());
if rm.get('version')!=EXPECTED: errors.append('release manifest version mismatch')
front=re.search(r'^version:\s*([0-9.]+)$', sk, re.M)
if not front or front.group(1)!=EXPECTED: errors.append('SKILL version mismatch')
if f'### v{EXPECTED}' not in (ROOT/'README.md').read_text(encoding='utf-8'): errors.append('README current version missing')
if f'**Version:** {EXPECTED}' not in (ROOT/'PRD.md').read_text(encoding='utf-8'): errors.append('PRD version mismatch')
if not (ROOT/'CHANGELOG.md').read_text().startswith(f'# Changelog\n\n## {EXPECTED} '): errors.append('CHANGELOG current version missing')
# exact deep template headings
expected=[f'## {i}. {title}' for i,title in enumerate(['Executive Decision State','Module Execution Matrix','Decision Profile','Decision Map','Material Findings','Evidence Audit','Assumption Registry','Dependency / Sensitivity','Uncertainty Structure','Failure Mode Analysis','Red-Team Challenge','Scenario Analysis','Alternative Analysis','Feasibility / Stakeholder / Agency','Second-Order Effects','Reversibility / Optionality','Decision Robustness','Decision Boundaries','Reassessment Triggers','Next Best Information / Action','Decision Ledger','Audit Integrity Check','Final Decision Debug'],1)]
dt=(ROOT/'templates/deep-debug.md').read_text(encoding='utf-8')
heads=re.findall(r'^## \d+\. .+$',dt,re.M)
if heads!=expected: errors.append('deep-debug exact headings mismatch')
# schema checks
schema=json.loads((ROOT/'evals/schema.json').read_text())
if schema.get('required') != ['decision','executive_state','findings','module_execution_matrix','audit_integrity']: errors.append('schema top-level required mismatch')
f=schema['properties']['findings']['items']; req=['id','severity','type','primary_module','related_modules','decision_changing','decision_link','location','problem','evidence','reasoning','impact','recommended_action','provenance','verification']
if f.get('required')!=req: errors.append('finding schema required mismatch')
me=schema['properties']['module_execution_matrix']['items']
if len(me.get('allOf',[]))!=2: errors.append('module class/status conditional missing')
ai=schema['properties']['audit_integrity']
if ai['properties']['human_machine_parity'].get('enum') != ['PASS','FAIL','NOT APPLICABLE']: errors.append('human_machine_parity enum mismatch')
for bad in ROOT.rglob('*'):
    if bad.is_file() and (bad.suffix in {'.pyc', '.pyo'} or '__pycache__' in bad.parts):
        errors.append(f'build artifact present: {bad.relative_to(ROOT)}')
if errors:
    print('FAIL'); print('\n'.join(errors)); raise SystemExit(1)
print('PASS'); print('version',EXPECTED); print('render_contract PASS'); print('schema_contract PASS'); print('status_contract PASS'); print('integrity_contract PASS')
