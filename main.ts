// main.ts -- make.fun runner for the news-image-20261120 entry.
//
// The entry is a single pre-rendered front page, entry.png, which sits
// next to this file (regenerate it any time with `python3 compose.py`).
// This program copies it into $MAKEFUN_OUTPUT_DIR (default /output)
// and then proves the copy is a sane PNG before declaring success.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ONE_MIB = 1024 * 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47]; // \x89 P N G

function fail(message: string): never {
  throw new Error(`news-image-20261120: ${message}`);
}

function checkPng(file: string): void {
  const info = statSync(file);
  if (info.size === 0) fail(`${file} is empty`);
  if (info.size > ONE_MIB) {
    fail(`${file} is ${info.size} bytes, over the 1 MiB limit`);
  }
  const head = readFileSync(file).subarray(0, PNG_SIGNATURE.length);
  const looksPng = PNG_SIGNATURE.every((byte, i) => head[i] === byte);
  if (!looksPng) fail(`${file} does not start with the PNG signature`);
}

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

checkPng(source); // never ship a broken source file
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
checkPng(target); // and never trust the copy blindly either

console.log(`entry.png -> ${target} (${statSync(target).size} bytes, PNG ok)`);
