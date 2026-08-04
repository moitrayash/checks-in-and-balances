const crypto = require('crypto'), fs = require('fs');
const SEED = "20260621", AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const H = (...p) => crypto.createHash('sha256').update(p.join('|')).digest('hex');
const canon = (vals, fam) => [...vals].sort((a,b) => {
  const ha = H(SEED,fam,a), hb = H(SEED,fam,b);
  return ha < hb ? -1 : ha > hb ? 1 : (a < b ? -1 : a > b ? 1 : 0);
});
const base26 = n => [2,1,0].map(i => AB[Math.floor(n / 26**i) % 26]).join('');
const pad2 = n => String(n).padStart(2,'0');

// parse the real source
const lines = fs.readFileSync('../asimplied.csv','utf8').replace(/^﻿/,'').trim().split('\n');
const hdr = lines[0].split(','), rows = lines.slice(1).map(l => {
  const v = l.split(','); return Object.fromEntries(hdr.map((h,i) => [h, v[i]]));
});
const excl = new Set(fs.readFileSync('excluded_iata_codes.txt','utf8').split('\n')
  .map(s=>s.trim()).filter(s=>s && !s.startsWith('#')));

const airports = new Set();
rows.forEach(r => { r.Routing.split('-').forEach(s=>airports.add(s.trim())); airports.add(r.dest_iata.trim()); });

// airports: rejection sampling, BigInt for the 8-hex-char slice
const apMap = {}, taken = new Set();
for (const real of canon(airports,'airport')) {
  for (let k = 0; ; k++) {
    const c = base26(Number(BigInt('0x'+H(SEED,'airport',real,k).slice(0,8)) % 17576n));
    if (!excl.has(c) && !taken.has(c)) { apMap[real]=c; taken.add(c); break; }
  }
}
const indexed = (vals, fam, tpl) => Object.fromEntries(
  canon(vals, fam).map((v,i) => [v, tpl.replace('NN', pad2(i+1))]));
const alMap = indexed(new Set(rows.map(r=>r['Airline code'].trim())),'airline','AirlineNN');
const ghMap = indexed(new Set(rows.map(r=>r.GHA.trim())),'gha','GHANN');
const ctMap = indexed(new Set(rows.map(r=>r.dest_city.trim())),'city','CityNN');
const cnMap = indexed(new Set([...rows.map(r=>r.dest_country.trim()),...rows.map(r=>r.airline_country.trim())]),'country','CountryNN');
const byAl = {};
rows.forEach(r => (byAl[r['Airline code'].trim()] ??= []).push(r['Flight Designator'].trim()));
const fdMap = {};
Object.keys(byAl).sort().forEach(c =>
  canon(byAl[c],'flight').forEach((d,i) => fdMap[d] = `${alMap[c]} ${pad2(i+1)}`));

console.log(JSON.stringify({airport:apMap, airline:alMap, gha:ghMap, city:ctMap, country:cnMap, flight:fdMap}));
