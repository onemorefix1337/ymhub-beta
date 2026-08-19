const fs = require('fs');
const s = fs.readFileSync('src/dll/dllmain.cpp', 'utf-8');

// The JS string starts at L"(function(){" and ends at })()";
let start = s.indexOf('L"(function(){');
if (start === -1) {
    console.log("Start not found");
    process.exit(1);
}
let end = s.indexOf('})()";', start);
if (end === -1) {
    console.log("End not found");
    process.exit(1);
}

let str = s.substring(start, end + 6);
// Now we parse the C++ string literals
let parts = str.split('\n');
let jsCode = "";
for (let part of parts) {
    let m = part.match(/L"(.*)"/);
    if (m) {
        jsCode += m[1];
    }
}

// Write the reconstructed JS string to a file to syntax check
fs.writeFileSync('test.js', jsCode);
console.log("Extracted JS, length:", jsCode.length);
