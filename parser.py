#!/usr/bin/python3
import re
from datetime import date

    
def parse(bib_file,html_file,**meta):
	bib=open(bib_file).read()

	papers=[]
	for x in re.finditer("""@(?P<type>\w+)\{(.+\n)+\},\n""",bib):
		paper={"type":x.group("type"),"bib":x.group(0)}
		paper_bib=x.group(0)
		#print(paper_bib)
		for y in re.finditer(r"\t(?P<key>\w+)\ =\ \{(?P<value>[^\t]+)\},?\n",paper_bib):
			#print('key >>',y.group("key"))
			#print('    value >>',y.group("value"))
			paper[y.group("key")]=y.group("value")
		if ('title' not in paper):
			input()
		papers.append(paper)

	papers.sort(key=lambda x:int(x.get("year","0")),reverse=True)


	
	content=[]
	last_year=None
	for paper_id,paper in enumerate(papers):
		#print(paper)
		#print(paper['title'])
		assert('title' in paper)
		if paper['year']!=last_year:
			if last_year:
				content.append("</div>")
			last_year=paper['year']
			content.append("""<div class="year">
	<div class="year_number">{0}</div><br/>""".format(last_year))
		paper.setdefault("annote","")
		JF=paper['booktitle'] if 'booktitle' in paper else paper['journal'] if 'journal' in paper else ''
		paper_html="""<div class="paper">
		<div class="bib">
			<div class="title" onclick="turn_note({0})">{title}</div>
			<div class="authors">{author}</div>
			<div class="JF">{JF}</div>
		</div>
		<div class="note" id="note_{0}" style="display:none">
		{annote}
		</div>
	</div>
	""".format(paper_id,JF=JF,**paper)
		content.append(paper_html)
		

	content.append("</div>")#end of div of year
	content='\n'.join(content)
	content="""<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<link href="css.css" rel="stylesheet" type="text/css" />
<script src="js.js"></script>
<title>{title}</title>
<body>
<div class="header"><div class="pic"></div>
{title}<br/>
由<a href="{collector_url}">{collector}</a>维护<br/>
如有意见与建议，欢迎联系作者:)<br/>
【其它链接】：<a href="http://zhangkaixu.github.com/isan/">中文分词实验环境<br/>
页面生成日期： {date}， 由<a href="http://zhangkaixu.github.com/bibpage/">bibpage</a>工具自动生成自bib格式文献列表。
</div>

{0}
</body>
	""".format(content,date="{0}年{1}月{2}日".format(*str(date.today()).split('-')),**meta)


	out_file=open(html_file,"w")
	print(content,file=out_file)
if __name__=='__main__':
	parse('cws.bib','cws.html',collector="张开旭",collector_url="http://weibo.com/zhangkaixu",title="中文分词文献列表 Bibliography of Chinese Word Segmentation")
