#!/usr/bin/env node
/**
 * Prove that every path `exports` promises is actually inside the tarball.
 *
 * `files` and `exports` are two lists that must agree and are edited
 * separately. When they drift, nothing fails locally -- the working tree has
 * every file -- and the break only appears once a consumer installs the
 * published package and a documented entry point 404s. `npm pack --dry-run`
 * gives the real file list, so this compares against that rather than the
 * working tree.
 *
 *     node scripts/check-exports.mjs
 */

import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));

/** Every literal path an exports entry can resolve to, wildcards expanded later. */
function targets(node, out = []) {
	if (typeof node === 'string') {
		out.push(node);
	} else if (node && typeof node === 'object') {
		for (const value of Object.values(node)) targets(value, out);
	}
	return out;
}

const packed = JSON.parse(
	execFileSync('npm', ['pack', '--dry-run', '--json'], { encoding: 'utf8' })
);
const shipped = new Set(packed[0].files.map((f) => `./${f.path}`));

const declared = [...new Set(targets(pkg.exports))];
const missing = [];

for (const target of declared) {
	if (target.includes('*')) {
		// A wildcard export is satisfied by at least one match; an empty one is
		// still a bug, because it means the directory never made it in.
		const pattern = new RegExp(`^${target.replace(/[.]/g, '\\.').replace('*', '.+')}$`);
		if (![...shipped].some((f) => pattern.test(f))) missing.push(`${target} (no matches)`);
		continue;
	}
	if (!shipped.has(target)) missing.push(target);
}

if (missing.length) {
	console.error('exports point at files the tarball does not contain:\n');
	for (const target of missing) console.error(`  ${target}`);
	console.error('\nCheck the `files` array in package.json.');
	process.exit(1);
}

console.log(`${declared.length} export targets, all present in the tarball`);
