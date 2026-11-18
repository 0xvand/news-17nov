// Entry for make.fun's news-image-20261117: "Sum up 17 November's world
// news in one image."
//
// The image is a newspaper front page for Tuesday 17 November 2026,
// drawn with Pillow by make_image.py (kept in this repository) from the
// day's reporting - SOURCES.md lists the reporting behind every
// headline. Its bytes travel with this repository as text: the single
// line of entry.png.b64.txt is the base64 of the PNG (sha256
// 2ef8358e5b89b6dc3e79508d32bc531694ba064eed0e93911d36509d73a553ae).
// This program's whole job is to decode those bytes and put them in
// the output, unchanged, on every run:
//
//   entry.png.b64.txt  ->  /output/entry.png
//
// Node 22, standard library only, no network. Outside the grader's
// container, MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const encodedBesideThisFile = new URL("./entry.png.b64.txt", import.meta.url);

const base64 = readFileSync(encodedBesideThisFile, "utf8").trim();
const imageBytes = Buffer.from(base64, "base64");

writeFileSync(join(outputDir, "entry.png"), imageBytes);
