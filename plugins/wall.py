from userge import userge, Message , Config
from bs4 import BeautifulSoup as soup
import requests
from random import randint,choice
import os


async def dlimg(link):
	e = requests.get(link).content
	path_i = os.path.join(Config.DOWN_PATH,'donno.{}'.format(link.split('.')[-1]))
	k = open(path_i,'wb')
	k.write(e)
	k.close()
	return path_i

async def wall(strin : str):
	if len(strin.split(' ')) > 1:
		strin = '+'.join(strin.split(' '))
	url = 'https://wall.alphacoders.com/search.php?search='
	none_got = 'https://wall.alphacoders.com/finding_wallpapers.php'
	page_link = 'https://wall.alphacoders.com/search.php?search={}&page={}'
	resp = requests.get(f'{url}{strin}')
	if resp.url == none_got:
		return False
	if 'by_category.php' in resp.url:
		page_link = str(resp.url).replace('&amp;','')+'&page={}'
		check_link = True
	else:
		check_link = False
	if True:
		resp = soup(resp.content , 'lxml')
		wall_num = list(resp.find('h1',{'class':'center title'}).text.split(' '))
		for i in wall_num:
			try:
				wall_num = int(i)
			except ValueError:
				pass
		try:
			page_num = int(resp.find('div',{'class':'visible-xs'}).find('input',{'class':'form-control'})['placeholder'].split(' ')[3])
		except:
			page_num = 1
		links = []
		n = randint(1,page_num)
		if True:
			if page_num != 1:
				if check_link:
					resp = requests.get(page_link.format(n))
				else:
					resp = requests.get(page_link.format(strin,n))
				
				resp = soup(resp.content , 'lxml')
			
			a_s = resp.find_all('a')
			list_a_s = []
			tit_links = []
			
			r = ['thumb','350','img','big.php?i','data-src','title']
			for l in a_s:
				if all(d in str(l) for d in r):
					list_a_s.append(l)
			try:
				for df in list_a_s:
					imgi = df.find('img')
					li = str(imgi['data-src']).replace('thumb-350-','')
					titl = str(df['title']).replace('|','').replace('  ','').replace('Image','').replace('HD','').replace('Wallpaper','').replace('Background','')
					p = (li,titl)
					tit_links.append(p)
			except Exception as erro:
				print(erro)
			del list_a_s
			tit_link = choice(tit_links)
			return tit_link
@userge.on_cmd("wall", about={
	'header': "Search Wallpaper",
	'description': '''Search and Download Hd Wallpaper from
alphacoders and upload to Telegram''',
	'usage': "{tr}wall [Query]",
	'examples': "{tr}wall luffy"})
async def idk_sir(message : Message):
	
	if not os.path.isdir(Config.DOWN_PATH):
		os.makedirs(Config.DOWN_PATH)

	if message.input_str:
		qu = message.input_str
		logmesys = '''**logger** : #wall

Search Query : {}'''.format(message.input_str)
		await userge.send_message(Config.LOG_CHANNEL_ID,logmesys)
		try:
			link = await wall(str(qu))
		except Exception as e:
			await message.edit(e)
			return
		if link:
			await message.edit('**Processing...**')
			idl = await dlimg(link[0])
			
			await message.edit('**Uploading...**')
			if not len(link[1].split()) < 11:
				capo = '**'+' '.join(link[1].split()[:11])+'**'
			else:
				capo = '**'+link[1]+'**'
			try:
				await userge.send_photo(chat_id=message.chat.id,
							photo=idl,
							caption=capo)
				await userge.send_document(message.chat.id,idl)
			except Exception as e:
				await message.edit(e)
				return
			await message.delete()
			os.system('rm {}'.format(idl))
		else:
			await message.edit('**Result Not Found**')
			await message.reply_sticker('CAADBAADIQEAAl_GARknbPJaYsVA2xYE')
	else:
		await message.edit('**Give me Something to search.**')
		await message.reply_sticker('CAADAQADmQADTusQR6fPCVZ3EhDoFgQ')
		