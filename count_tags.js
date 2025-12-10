const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'data/judgments.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const tagCounts = {};
data.forEach(item => {
    item.tags.forEach(tag => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    });
});

console.log('Tag Frequencies:');
const sortedTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]);
sortedTags.forEach(([tag, count]) => {
    console.log(`${tag}: ${count}`);
});

const over20 = sortedTags.filter(([tag, count]) => count >= 20);
console.log('\nTags with count >= 20:', over20.length);
console.log(over20.map(t => t[0]));
