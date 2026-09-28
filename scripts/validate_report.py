from pathlib import Path
import re,sys
EXPECTED_HEADS=[f"## {i}. {t}" for i,t in enumerate(['Executive Decision State','Module Execution Matrix','Decision Profile','Decision Map','Material Findings','Evidence Audit','Assumption Registry','Dependency / Sensitivity','Uncertainty Structure','Failure Mode Analysis','Red-Team Challenge','Scenario Analysis','Alternative Analysis','Feasibility / Stakeholder / Agency','Second-Order Effects','Reversibility / Optionality','Decision Robustness','Decision Boundaries','Reassessment Triggers','Next Best Information / Action','Decision Ledger','Audit Integrity Check','Final Decision Debug'],1)]
def main():
 p=Path(sys.argv[1]) if len(sys.argv)>1 else None
 if not p or not p.is_file(): print('usage: python scripts/validate_report.py REPORT.md'); return 2
 t=p.read_text(encoding='utf-8'); heads=re.findall(r'^## \d+\. .+$',t,re.M); errs=[]
 if heads!=EXPECTED_HEADS: errs.append('exact 23-section heading contract failed')
 if t.count('## 22. Audit Integrity Check')!=1: errs.append('integrity section count != 1')
 findings=t.split('## 5. Material Findings',1)[1].split('## 6. Evidence Audit',1)[0] if '## 5. Material Findings' in t and '## 6. Evidence Audit' in t else ''
 fields=['ID:','Severity:','Type:','Primary Module:','Related Modules:','Decision-Changing:','Decision Link:','Location:','Problem:','Evidence:','Reasoning:','Impact:','Recommended Action:','Provenance:','Verification:']
 blocks=re.split(r'(?m)^ID:\s*',findings)[1:] if 'ID:' in findings else []
 for i,b in enumerate(blocks,1):
  for f in fields[1:]:
   if not re.search(r'(?m)^'+re.escape(f),b): errs.append(f'finding {i} missing {f}')
 if errs: print('FAIL'); print('\n'.join(errs)); return 1
 print('PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
