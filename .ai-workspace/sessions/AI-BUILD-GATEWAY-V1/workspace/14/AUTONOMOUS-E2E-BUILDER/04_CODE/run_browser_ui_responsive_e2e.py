from __future__ import annotations
import json
from playwright.sync_api import sync_playwright
URL='https://8766-i25zqohw3i0yid281ucdc-41ebdf56.sg2.manus.computer/'
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for name,width,height in [('desktop',1280,720),('tablet',768,1024),('mobile',375,812)]:
        page=browser.new_page(viewport={'width':width,'height':height}); page.goto(URL,wait_until='domcontentloaded'); page.wait_for_timeout(300); overflow=page.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth'); item={'viewport':name,'width':width,'height':height,'horizontal_overflow':overflow,'ai_command_visible':page.locator('#command').is_visible(),'diff_tab_visible':page.get_by_text('DIFF',exact=True).is_visible(),'preview_tab_visible':page.get_by_text('PREVIEW',exact=True).is_visible()}; results.append(item); assert not overflow and item['ai_command_visible'] and item['diff_tab_visible'] and item['preview_tab_visible']; page.close()
    browser.close()
print(json.dumps({'status':'PASS','viewports':results},indent=2))
