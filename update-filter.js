const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'judgments.html');
let content = fs.readFileSync(filePath, 'utf8');

const oldFunc = `        function generateFilters(data) {
            const container = document.getElementById('dynamic-filters');
            container.innerHTML = '';
            container.innerHTML += createDateRangeFilter();

            const allTags = new Set();
            data.forEach(item => item.tags.forEach(tag => allTags.add(tag)));

            for (const [categoryName, definedTags] of Object.entries(tagCategories)) {
                const existingTags = definedTags.filter(tag => allTags.has(tag));
                if (existingTags.length > 0) {
                    container.innerHTML += createFilterGroupHtml(categoryName, existingTags);
                    existingTags.forEach(tag => allTags.delete(tag));
                }
            }

            if (allTags.size > 0) {
                container.innerHTML += createFilterGroupHtml("✨ その他・新着タグ", Array.from(allTags));
            }
        }`;

const newFunc = `        function generateFilters(data) {
            const container = document.getElementById('dynamic-filters');
            container.innerHTML = '';
            container.innerHTML += createDateRangeFilter();

            // タグの出現回数をカウント
            const tagCounts = {};
            data.forEach(item => item.tags.forEach(tag => {
                tagCounts[tag] = (tagCounts[tag] || 0) + 1;
            }));

            // 20件以上のタグだけをフィルターに表示
            const MIN_TAG_COUNT = 20;
            const frequentTags = new Set(
                Object.entries(tagCounts)
                    .filter(([tag, count]) => count >= MIN_TAG_COUNT)
                    .map(([tag]) => tag)
            );

            for (const [categoryName, definedTags] of Object.entries(tagCategories)) {
                const existingTags = definedTags.filter(tag => frequentTags.has(tag));
                if (existingTags.length > 0) {
                    container.innerHTML += createFilterGroupHtml(categoryName, existingTags);
                    existingTags.forEach(tag => frequentTags.delete(tag));
                }
            }

            if (frequentTags.size > 0) {
                container.innerHTML += createFilterGroupHtml("✨ その他・新着タグ", Array.from(frequentTags));
            }
        }`;

if (content.includes(oldFunc)) {
    content = content.replace(oldFunc, newFunc);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('✅ generateFilters function updated successfully!');
} else {
    console.log('❌ Old function not found. Trying with normalized line endings...');
    const normalizedOld = oldFunc.replace(/\r\n/g, '\n');
    const normalizedContent = content.replace(/\r\n/g, '\n');
    if (normalizedContent.includes(normalizedOld)) {
        const newContent = normalizedContent.replace(normalizedOld, newFunc);
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log('✅ generateFilters function updated (normalized line endings)!');
    } else {
        console.log('❌ Still not found. Check the file manually.');
    }
}
