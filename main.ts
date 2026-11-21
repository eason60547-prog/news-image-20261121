// News-image entry: copies the front page drawn for 21 November 2026
// (entry.png beside this file) to /output/entry.png. Node 22, stdlib only,
// no network, deterministic: the same bytes every run.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(out, 'entry.png'));
