import urllib2,string
import simplejson

def searchImg(query):
	## reference: https://developers.google.com/image-search/v1/jsondevguide#json_snippets_python
	query = string.replace(query," ","%20")
	url = ("https://ajax.googleapis.com/ajax/services/search/images?" + "v=1.0&q=" + query + "&rsz=8")
	request = urllib2.Request(url, None, {'Referer':"www.github.com/gradiuscypher/Neo"})
	response = urllib2.urlopen(request)
	results = simplejson.load(response)

	## list of result pages, used for &start query
	pagelist = results['responseData']['cursor']['pages']
	pages = []
	for i in pagelist:
		pages.append(i['start'])

	##return all results, save them to a dictionary, append that dictionary to a list
	resultList = []
	for i in pages:
		query = string.replace(query," ","%20")
		url = ("https://ajax.googleapis.com/ajax/services/search/images?" + "v=1.0&q=" + query + "&rsz=8&start=" + i)
		request = urllib2.Request(url, None, {'Referer':"www.github.com/gradiuscypher/Neo"})
		response = urllib2.urlopen(request)
		results = simplejson.load(response)
		anslist = results['responseData']['results']
		for i in anslist:
			resultList.append({'name':i['visibleUrl'],'url':i['url'],'titleNoFormatting':i['titleNoFormatting']})

	return resultList
