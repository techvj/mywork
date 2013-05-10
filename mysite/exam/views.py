from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
import lxml
import urllib2
from bs4 import BeautifulSoup

def index(request):
	""" sample test page which accepts the input """
	template = loader.get_template('exam/index.html')
	context = Context({'img':'a',})
	return HttpResponse(template.render(context))

def extract_url(itext):
	""" checks if the input is a url 
		Not checking for http://http kind of scenarios for now
	"""
	if itext.strip().startswith("http://"):
		return itext
	elif "http" in itext:
		input_text = itext.split()
		page_url = [item for item in input_text if item.startswith("http")]
		return page_url[0]
	else:
		return False

def fetch_first_image(itext):
	""" fetches the images from the given url and returns first image
		Right now it works only for .com urls 
		it does not work if the image is embedded like below
		<div title="Google" align="left" id="hplogo" onload="window.lol&amp;&amp;lol()" style="background:url(images/srpr/logo4w.png) no-repeat;background-size:275px 95px;height			
		if the page have absolute url simply return, otherwise construct the full url
	 """
	page_url = extract_url(itext)
	print "extracted url", page_url
	if page_url:
		http_response = urllib2.urlopen(page_url)
		if http_response.code == 200:
			content = http_response.read()
			bs = BeautifulSoup(content)
			# checking only for html tag img src
			all_images = bs.find_all('img')
			print all_images
			# In  most of the sites first image is logo, including gaglers
			if len(all_images) >= 2:
				first_image = all_images[1]['src'].strip()
				print "image url", first_image
				if first_image.startswith("http://"):
					return first_image
				elif ".com" in first_image and "http://" not in first_image:
					# example  http://news.google.com have //ssl.gstatic.com/ui/v1/button/search-white.png
					return "http:" + first_image
				else:
					url_name = http_response.url
					url_name = url_name.split(".com")
					first_image =  url_name[0]+".com"+first_image
					return first_image
	

@csrf_exempt		
def show_first_image(request):
	""" display the first image in the test page """
	if request.method == "POST":
		itext = request.POST["iurl"]
		print itext
		fimage = fetch_first_image(itext)
		print "first image", fimage
	return render_to_response('exam/index.html',{"foo":fimage})	
