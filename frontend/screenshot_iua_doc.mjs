import { chromium } from 'playwright-core';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 1400 } });
const logs = [];
page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));
page.on('pageerror', err => logs.push(`[pageerror] ${err.message}`));

await page.goto('http://localhost:5173/', { waitUntil: 'networkidle' });
await page.click('text=Doc. IUA');
await page.waitForTimeout(500);
await page.screenshot({ path: '/tmp/iua_doc.png', fullPage: true });

console.log('CONSOLE LOGS:', JSON.stringify(logs, null, 2));
await browser.close();
