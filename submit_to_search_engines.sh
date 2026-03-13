#!/bin/bash

# 搜索引擎提交脚本
# 作者：阿爪
# 日期：2026-03-13

echo "🚀 开始提交网站到搜索引擎..."
echo "网站URL: https://qinzhengzhanghao-oss.github.io/medical-tourism-website/"
echo ""

# 检查必要文件
echo "📁 检查网站文件..."
if [ -f "sitemap.xml" ]; then
    echo "✅ sitemap.xml 存在"
else
    echo "❌ sitemap.xml 不存在"
    exit 1
fi

if [ -f "robots.txt" ]; then
    echo "✅ robots.txt 存在"
else
    echo "❌ robots.txt 不存在"
    exit 1
fi

echo ""
echo "🔍 网站状态检查..."
curl -I "https://qinzhengzhanghao-oss.github.io/medical-tourism-website/" 2>/dev/null | head -1

echo ""
echo "📊 网站页面统计:"
find . -name "*.html" | wc -l | xargs echo "HTML文件数量:"

echo ""
echo "🎯 需要手动操作的步骤:"
echo ""
echo "1. Google Search Console 提交"
echo "   访问: https://search.google.com/search-console"
echo "   步骤:"
echo "   a. 点击'添加资源'"
echo "   b. 输入URL: https://qinzhengzhanghao-oss.github.io/medical-tourism-website/"
echo "   c. 选择'HTML文件'验证方式"
echo "   d. 下载验证文件并替换 google-site-verification.html"
echo "   e. 提交sitemap: https://qinzhengzhanghao-oss.github.io/medical-tourism-website/sitemap.xml"
echo ""
echo "2. Bing Webmaster Tools 提交"
echo "   访问: https://www.bing.com/webmasters"
echo "   步骤:"
echo "   a. 添加网站"
echo "   b. 选择'XML文件'验证方式"
echo "   c. 下载BingSiteAuth.xml并替换现有文件"
echo "   d. 提交sitemap"
echo ""
echo "3. 提交到其他搜索引擎"
echo "   - 百度站长平台: https://ziyuan.baidu.com (需要中国手机号)"
echo "   - Yandex Webmaster: https://webmaster.yandex.com"
echo ""
echo "4. 监控提交状态"
echo "   - Google Search Console: 查看索引状态"
echo "   - Bing Webmaster Tools: 查看爬取报告"
echo ""
echo "📅 预计时间线:"
echo "   - 24小时内: Google开始收录"
echo "   - 3-7天内: 出现在搜索结果中"
echo "   - 14-30天内: 稳定排名建立"
echo ""
echo "✅ 脚本执行完成！请按照上述步骤手动操作。"