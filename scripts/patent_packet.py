"""Support-checked application scaffold; semantic/legal review remains with the agent."""
import json
from pathlib import Path
from urllib.parse import urlparse


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be nonempty text")


def validate(packet, features):
    active = {f['id'] for f in features['features']
              if f['support'] in ('explicit', 'inherent') and f['activation'] == 'active'}
    for key in ('title', 'abstract', 'field', 'background', 'problem', 'embodiment'):
        nonempty(packet.get(key), key)
    if len(packet['abstract']) > 300:
        raise ValueError('Abstract exceeds the workflow style limit of 300 characters')

    def supported(item, label):
        refs = item.get('features')
        if not isinstance(refs, list) or not refs or any(r not in active for r in refs):
            raise ValueError(label + ' must reference supported active features')
        nonempty(item.get('text'), label + ' text')

    claims = packet.get('claims')
    if not isinstance(claims, list) or not claims:
        raise ValueError('Application needs at least one independent claim')
    prior = set()
    independent = False
    for index, claim in enumerate(claims, 1):
        if type(claim.get('id')) is not int or claim['id'] != index:
            raise ValueError('Claim IDs must be consecutive integers from 1')
        supported(claim, 'Claim')
        dependencies = claim.get('depends_on', [])
        if not isinstance(dependencies, list) or any(type(d) is not int or d not in prior for d in dependencies):
            raise ValueError('Claims may depend only on preceding claims')
        independent |= not dependencies
        prior.add(index)
    if not independent:
        raise ValueError('Application needs an independent claim')
    steps = packet.get('steps')
    if not isinstance(steps, list) or not steps:
        raise ValueError('Application needs concrete implementation steps')
    for index, step in enumerate(steps, 1):
        if step.get('id') != f'S{index}':
            raise ValueError('Steps must be consecutive S1, S2, ...')
        supported(step, 'Step')
    step_refs = {ref for step in steps for ref in step['features']}
    if any(ref not in step_refs for claim in claims for ref in claim['features']):
        raise ValueError('Each claimed feature needs an implementation step')
    formula_ids = set()
    for formula in packet.get('formulas', []):
        nonempty(formula.get('id'), 'Formula ID')
        if formula['id'] in formula_ids:
            raise ValueError('Duplicate formula ID')
        formula_ids.add(formula['id'])
        nonempty(formula.get('latex'), 'Formula LaTeX')
        if not formula.get('features') or any(r not in active for r in formula['features']):
            raise ValueError('Formula must reference supported active features')
        if not isinstance(formula.get('variables'), list) or not formula['variables']:
            raise ValueError('Formula needs symbol definitions')
        for variable in formula['variables']:
            nonempty(variable.get('symbol'), 'Symbol')
            nonempty(variable.get('meaning'), 'Symbol meaning')
    known_steps = {s['id'] for s in steps}
    for index, figure in enumerate(packet.get('figures', []), 1):
        if figure.get('id') != index:
            raise ValueError('Figure IDs must be consecutive integers from 1')
        nonempty(figure.get('caption'), 'Figure caption')
        if not figure.get('steps') or any(s not in known_steps for s in figure['steps']):
            raise ValueError('Figure references unknown implementation steps')
    search = packet.get('prior_art', {'status': 'not-searched', 'sources': [], 'differences': []})
    if search.get('status') not in ('not-searched', 'partial', 'compared'):
        raise ValueError('Unknown prior-art search status')
    sources = {}
    for source in search.get('sources', []):
        for key in ('id', 'title', 'url', 'accessed_at', 'locator'):
            nonempty(source.get(key), 'Prior-art ' + key)
        url = urlparse(source['url'])
        if url.scheme not in ('http', 'https') or not url.netloc:
            raise ValueError('Prior art needs a public source URL')
        if source['id'] in sources:
            raise ValueError('Duplicate prior-art source ID')
        if source.get('scope') not in ('abstract', 'full-text'):
            raise ValueError('Prior-art evidence scope must be abstract or full-text')
        sources[source['id']] = source
    differences = search.get('differences', [])
    for difference in differences:
        if difference.get('feature') not in active or difference.get('source') not in sources:
            raise ValueError('Difference needs a supported feature and known prior-art source')
        nonempty(difference.get('comparison'), 'Difference comparison')
    if search['status'] == 'not-searched' and (sources or differences):
        raise ValueError('Unsearched status cannot contain comparison evidence')
    if search['status'] == 'compared' and (not sources or not differences):
        raise ValueError('Compared status needs sources and feature comparisons')
    # These checks prove identifiers/structure, not entailment, search completeness or novelty.


def render(packet, features):
    claims = '\n\n'.join(f"{c['id']}. {c['text']}" for c in packet['claims']) + '\n'
    steps = '\n\n'.join(f"{s['id']}：{s['text']}" for s in packet['steps'])
    formulas = []
    for number, formula in enumerate(packet.get('formulas', []), 1):
        formulas += [f"式（{number}）：\n\n$$\n{formula['latex']}\n$$",
                     '；'.join(f"{v['symbol']}：{v['meaning']}" for v in formula['variables'])]
    effects = []
    active = [f for f in features['features'] if f['support'] in ('explicit', 'inherent') and f['activation'] == 'active']
    for f in active:
        e = f.get('effect', {})
        status = e.get('status', 'expected')
        if status == 'validated':
            effects.append(e.get('text', '') + '；验证条件：' + e['protocol'])
        elif status == 'observed':
            effects.append('探索记录，尚未证明稳定收益：' + e.get('text', ''))
        elif status == 'expected':
            effects.append('预期目标，尚待实验验证：' + e.get('text', '待补充'))
    figures = packet.get('figures', [])
    descriptions = '\n\n'.join(f"图{f['id']}为{f['caption']}，对应{'、'.join(f['steps'])}。" for f in figures)
    specification = '\n\n'.join([
        '# 说明书', '## 技术领域', packet['field'], '## 背景技术', packet['background'],
        '## 发明内容', '### 要解决的技术问题', packet['problem'], '### 技术方案', steps,
        '### 有益效果及验证边界', '\n\n'.join(effects) or '未提供技术效果验证材料。',
        '## 附图说明', descriptions or '尚未提供附图；需发明人补充。',
        '## 具体实施方式', packet['embodiment'], steps, '\n\n'.join(formulas)]) + '\n'
    abstract = packet['abstract'] + ('\n\n摘要附图：图1。' if figures else '\n\n摘要附图待补充。') + '\n'
    drawings = ['# 说明书附图（待渲染的流程草图）', '']
    extras = {}
    step_map = {s['id']: s for s in packet['steps']}
    for figure in figures:
        nodes = []
        for sid in figure['steps']:
            text = step_map[sid]['text'].replace('"', '＂').replace('\n', ' ').replace('`', '｀')
            nodes.append(f'  {sid}["{sid} {text}"]')
        nodes += [f'  {a} --> {b}' for a, b in zip(figure['steps'], figure['steps'][1:])]
        graph = 'flowchart TD\n' + '\n'.join(nodes) + '\n'
        extras[f"figure-{figure['id']}.mmd"] = graph
        drawings += [f"图{figure['id']} {figure['caption']}", '', '```mermaid', graph.rstrip(), '```', '']
    mapping = {'claims': [{**c, 'code_evidence': sorted({e for f in active if f['id'] in c['features'] for e in f['evidence']})}
                          for c in packet['claims']],
               'steps': packet['steps'], 'formulas': packet.get('formulas', []),
               'figures': figures, 'prior_art': packet.get('prior_art', {'status': 'not-searched'}),
               'limits': 'Feature links require semantic review; no legal or novelty conclusion.'}
    combined = '\n\n'.join(['# ' + packet['title'], '## 说明书摘要', abstract, '## 权利要求书', claims, specification,
                             '\n'.join(drawings), '本稿用于技术核对及专业审阅，尚未作为申请文件提交。'])
    return {'application.md': combined, '权利要求书.md': claims, '说明书.md': specification,
            '说明书摘要.md': abstract, '说明书附图.md': '\n'.join(drawings),
            'application-support.json': json.dumps(mapping, ensure_ascii=False, indent=2) + '\n', **extras}
