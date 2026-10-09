from __future__ import annotations
import re
from urllib.parse import urljoin

class CommandInterpretationError(ValueError): pass
class CommandWorkflowInterpreter:
    def interpret(self, command: str, base_url: str, default_url: str='/fixture.html') -> dict:
        if not isinstance(command,str) or not command.strip(): raise CommandInterpretationError('empty_ai_command')
        text=command.strip(); start=urljoin(base_url+'/', default_url.lstrip('/')); steps=[]
        nav=re.search(r'navigate\s+(?:to\s+)?(https?://[^\s,]+|/[^\s,]+)',text,re.I)
        if nav: start=urljoin(base_url+'/',nav.group(1).lstrip('/')) if nav.group(1).startswith('/') else nav.group(1)
        if re.search(r'\binspect\b',text,re.I): steps.append({'op':'inspect'})
        click=re.search(r'click\s+(?:on\s+)?([#\.][\w-]+)',text,re.I)
        if click: steps.append({'op':'click','selector':click.group(1)})
        typed=re.search(r'type\s+["\']?([^"\']+?)["\']?\s+(?:into|in)\s+([#\.][\w-]+)',text,re.I)
        if typed: steps.append({'op':'type','selector':typed.group(2),'text':typed.group(1).strip()})
        elif re.search(r'\btype\b',text,re.I): steps.append({'op':'type','selector':'#q','text':'ai-command'})
        if re.search(r'\bwait\b',text,re.I): steps.append({'op':'wait','ms':500})
        if re.search(r'\bextract\b',text,re.I): steps.append({'op':'extract','selectors':{'heading':'h1','result':'#result'}})
        if re.search(r'\bscreenshot\b',text,re.I): steps.append({'op':'screenshot','name':'ai-command.png'})
        if re.search(r'\bdownload\b',text,re.I): steps.append({'op':'download','selector':'a'})
        if re.search(r'\bclose\b',text,re.I): steps.append({'op':'close'})
        if not steps: raise CommandInterpretationError('no_supported_workflow_intent')
        return {'work_id':'14','task':text,'start_url':start,'steps':steps,'retry':{'default':1},'evidence':{'screenshot_on_failure':True},'command_interpretation':{'source':text,'step_count':len(steps)}}
